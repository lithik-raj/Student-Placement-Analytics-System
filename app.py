import os
import sys
import json
from flask import Flask, render_template, abort, request, redirect, url_for, session, jsonify

# Import robust database manager
from db import get_db_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)

# WSGI Middleware to handle Vercel serverless proxy routing and rewrites
class PrefixMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')

        # 1. Strip /api/index prefix if present from rewrite
        for prefix in ['/api/index.py', '/api/index']:
            if path == prefix or path == prefix + '/':
                path = '/'
                break
            elif path.startswith(prefix + '/'):
                path = path[len(prefix):]
                break

        # 2. Check proxy headers if path is still root or empty
        if path in ('', '/'):
            for key in [
                'HTTP_X_MATCHED_PATH',
                'HTTP_X_VERCEL_MATCHED_PATH',
                'REQUEST_URI',
                'HTTP_X_FORWARDED_URI',
                'HTTP_X_NOW_PATHNAME',
                'HTTP_X_REWRITE_URL',
                'RAW_URI',
            ]:
                val = environ.get(key)
                if val and not val.startswith('/api/index'):
                    clean_val = val.split('?')[0]
                    if clean_val and clean_val != '/':
                        path = clean_val
                        break

        environ['PATH_INFO'] = path or '/'
        return self.wsgi_app(environ, start_response)

app.wsgi_app = PrefixMiddleware(app.wsgi_app)

app.secret_key = os.environ.get("SECRET_KEY", "placement_analytics_admin_secret_key")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "lithikportal@gmail.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "lithik@123")


# =========================================================
# ADMIN LOGIN / LOGOUT
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid Administrator Login ID or Security Key."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    return redirect(url_for("login"))


def admin_required():
    return session.get("admin_logged_in", False)


# =========================================================
# HOME / MAIN DASHBOARD (Protected - Admin Authenticated First)
# =========================================================

@app.route("/")
def home():
    # Admin portal comes first for authentication
    if not admin_required():
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # 1. Total Metrics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_students,
                ROUND(AVG(cgpa), 2) as avg_cgpa,
                SUM(CASE WHEN readiness_status = 'Elite Ready' THEN 1 ELSE 0 END) as elite_count,
                SUM(CASE WHEN readiness_status = 'Job Ready' THEN 1 ELSE 0 END) as job_ready_count
            FROM students
        """)
        m_students = cursor.fetchone() or {}
        total_students = m_students.get("total_students", 0)
        avg_cgpa = m_students.get("avg_cgpa", 0.0)
        elite_count = m_students.get("elite_count", 0)
        job_ready_count = m_students.get("job_ready_count", 0)

        cursor.execute("""
            SELECT 
                COUNT(*) as total_placements,
                ROUND(MAX(c.package_lpa), 1) as max_pkg,
                ROUND(AVG(c.package_lpa), 2) as avg_pkg
            FROM placements p
            JOIN companies c ON p.company_id = c.company_id
            WHERE p.placement_status = 'PLACED'
        """)
        m_placed = cursor.fetchone() or {}
        total_placements = m_placed.get("total_placements", 0)
        max_package = m_placed.get("max_pkg", 0.0)
        avg_package = m_placed.get("avg_pkg", 0.0)

        cursor.execute("SELECT COUNT(*) AS total FROM companies")
        total_companies_res = cursor.fetchone()
        total_companies = total_companies_res["total"] if total_companies_res else 0

        cursor.execute("SELECT COUNT(*) AS total FROM skills")
        total_skills_res = cursor.fetchone()
        total_skills = total_skills_res["total"] if total_skills_res else 0

        unplaced_students = max(0, total_students - total_placements)
        placement_percentage = round((total_placements / total_students) * 100, 1) if total_students > 0 else 0

        # 2. Department Analytics
        cursor.execute("""
            SELECT 
                s.department,
                COUNT(DISTINCT s.student_id) as total_students,
                COUNT(DISTINCT p.student_id) as placed_students,
                ROUND(AVG(s.cgpa), 2) as dept_avg_cgpa,
                ROUND(AVG(c.package_lpa), 2) as dept_avg_pkg
            FROM students s
            LEFT JOIN placements p ON s.student_id = p.student_id AND p.placement_status = 'PLACED'
            LEFT JOIN companies c ON p.company_id = c.company_id
            GROUP BY s.department
            ORDER BY total_students DESC
        """)
        department_data = cursor.fetchall()

        for dept in department_data:
            t = dept["total_students"]
            p = dept["placed_students"]
            dept["placement_rate"] = round((p / t) * 100, 1) if t > 0 else 0

        # 3. Chart 1: Department Comparison
        dept_labels = [d["department"] for d in department_data]
        dept_totals = [d["total_students"] for d in department_data]
        dept_placed = [d["placed_students"] for d in department_data]

        # 4. Chart 2: Salary Package Tiers
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN c.package_lpa >= 20.0 THEN 1 ELSE 0 END) as super_dream,
                SUM(CASE WHEN c.package_lpa >= 10.0 AND c.package_lpa < 20.0 THEN 1 ELSE 0 END) as dream,
                SUM(CASE WHEN c.package_lpa >= 6.0 AND c.package_lpa < 10.0 THEN 1 ELSE 0 END) as regular,
                SUM(CASE WHEN c.package_lpa < 6.0 THEN 1 ELSE 0 END) as mass
            FROM placements p
            JOIN companies c ON p.company_id = c.company_id
            WHERE p.placement_status = 'PLACED'
        """)
        tier_row = cursor.fetchone() or {}
        tier_labels = ["Super Dream (>20 LPA)", "Dream (10-20 LPA)", "Regular (6-10 LPA)", "Core / Mass (<6 LPA)"]
        tier_counts = [
            tier_row.get("super_dream", 0) or 0,
            tier_row.get("dream", 0) or 0,
            tier_row.get("regular", 0) or 0,
            tier_row.get("mass", 0) or 0
        ]

        # 5. Chart 3: Top Recruiting Companies
        cursor.execute("""
            SELECT c.company_name, COUNT(p.placement_id) as hires, c.package_lpa
            FROM placements p
            JOIN companies c ON p.company_id = c.company_id
            WHERE p.placement_status = 'PLACED'
            GROUP BY c.company_name
            ORDER BY hires DESC
            LIMIT 8
        """)
        top_companies = cursor.fetchall()
        company_labels = [c["company_name"] for c in top_companies]
        company_hires = [c["hires"] for c in top_companies]
        company_pkgs = [c["package_lpa"] for c in top_companies]

        # 6. Chart 4: CGPA Academic Distribution
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN cgpa >= 9.0 THEN 1 ELSE 0 END) as g9,
                SUM(CASE WHEN cgpa >= 8.0 AND cgpa < 9.0 THEN 1 ELSE 0 END) as g8,
                SUM(CASE WHEN cgpa >= 7.0 AND cgpa < 8.0 THEN 1 ELSE 0 END) as g7,
                SUM(CASE WHEN cgpa < 7.0 THEN 1 ELSE 0 END) as g6
            FROM students
        """)
        cgpa_row = cursor.fetchone() or {}
        cgpa_dist_labels = ["9.0 - 10.0 (Outstanding)", "8.0 - 8.9 (Distinction)", "7.0 - 7.9 (First Class)", "6.0 - 6.9 (Second Class)"]
        cgpa_dist_counts = [
            cgpa_row.get("g9", 0) or 0,
            cgpa_row.get("g8", 0) or 0,
            cgpa_row.get("g7", 0) or 0,
            cgpa_row.get("g6", 0) or 0
        ]

        # 7. Chart 5: Top Technical Skills Demand
        cursor.execute("""
            SELECT sk.skill_name, COUNT(ss.student_id) as count
            FROM student_skills ss
            JOIN skills sk ON ss.skill_id = sk.skill_id
            GROUP BY sk.skill_name
            ORDER BY count DESC
            LIMIT 10
        """)
        top_skills = cursor.fetchall()
        skill_labels = [s["skill_name"] for s in top_skills]
        skill_counts = [s["count"] for s in top_skills]

        # 8. Initial First Page of Students (24 records with skills_list subquery)
        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                s.department,
                s.year,
                s.cgpa,
                s.gender,
                s.readiness_score,
                s.readiness_status,
                CASE WHEN p.placement_id IS NOT NULL THEN 'PLACED' ELSE 'NOT PLACED' END as placement_status,
                c.company_name,
                c.package_lpa,
                (
                    SELECT GROUP_CONCAT(sk.skill_name, ', ')
                    FROM student_skills ss
                    JOIN skills sk ON ss.skill_id = sk.skill_id
                    WHERE ss.student_id = s.student_id
                ) as skills_list
            FROM students s
            LEFT JOIN placements p ON s.student_id = p.student_id AND p.placement_status = 'PLACED'
            LEFT JOIN companies c ON p.company_id = c.company_id
            ORDER BY s.student_id ASC
            LIMIT 24
        """)
        initial_students = cursor.fetchall()

        departments_list = [d["department"] for d in department_data]

        chart_data = {
            "dept_labels": dept_labels,
            "dept_totals": dept_totals,
            "dept_placed": dept_placed,
            "status_labels": ["Placed", "Not Placed"],
            "status_counts": [total_placements, unplaced_students],
            "tier_labels": tier_labels,
            "tier_counts": tier_counts,
            "company_labels": company_labels,
            "company_hires": company_hires,
            "company_pkgs": company_pkgs,
            "cgpa_dist_labels": cgpa_dist_labels,
            "cgpa_dist_counts": cgpa_dist_counts,
            "skill_labels": skill_labels,
            "skill_counts": skill_counts
        }

        return render_template(
            "index.html",
            total_students=total_students,
            total_placements=total_placements,
            total_companies=total_companies,
            total_skills=total_skills,
            unplaced_students=unplaced_students,
            placement_percentage=placement_percentage,
            avg_cgpa=avg_cgpa,
            max_package=max_package,
            avg_package=avg_package,
            elite_count=elite_count,
            job_ready_count=job_ready_count,
            department_data=department_data,
            departments_list=departments_list,
            initial_students=initial_students,
            chart_data_json=json.dumps(chart_data)
        )

    finally:
        cursor.close()
        db.close()


# =========================================================
# FAST API - PAGINATED SEARCH & FILTER (1,200 Students with Skills)
# =========================================================

@app.route("/api/students")
def api_students():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 24))
    search = request.args.get("search", "").strip()
    department = request.args.get("department", "").strip()
    status = request.args.get("status", "ALL").strip().upper()
    readiness = request.args.get("readiness", "ALL").strip()
    sort = request.args.get("sort", "id_asc").strip().lower()

    offset = (page - 1) * limit

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        where_clauses = ["1=1"]
        params = []

        if search:
            where_clauses.append("(s.name LIKE %s OR s.email LIKE %s OR CAST(s.student_id AS TEXT) LIKE %s)")
            wild = f"%{search}%"
            params.extend([wild, wild, wild])

        if department and department != "ALL":
            where_clauses.append("s.department = %s")
            params.append(department)

        if status == "PLACED":
            where_clauses.append("p.placement_id IS NOT NULL")
        elif status == "NOT PLACED":
            where_clauses.append("p.placement_id IS NULL")

        if readiness and readiness != "ALL":
            where_clauses.append("s.readiness_status = %s")
            params.append(readiness)

        where_sql = " AND ".join(where_clauses)

        sort_map = {
            "id_asc": "s.student_id ASC",
            "id_desc": "s.student_id DESC",
            "name_asc": "s.name ASC",
            "name_desc": "s.name DESC",
            "cgpa_desc": "s.cgpa DESC",
            "cgpa_asc": "s.cgpa ASC",
            "readiness_desc": "s.readiness_score DESC",
            "pkg_desc": "COALESCE(c.package_lpa, 0) DESC"
        }
        order_by = sort_map.get(sort, "s.student_id ASC")

        # Count total matching
        count_query = f"""
            SELECT COUNT(DISTINCT s.student_id) as total
            FROM students s
            LEFT JOIN placements p ON s.student_id = p.student_id AND p.placement_status = 'PLACED'
            WHERE {where_sql}
        """
        cursor.execute(count_query, params)
        total_res = cursor.fetchone()
        total_records = total_res["total"] if total_res else 0

        # Query paginated results with skills_list subquery
        data_query = f"""
            SELECT
                s.student_id,
                s.name,
                s.email,
                s.department,
                s.year,
                s.cgpa,
                s.gender,
                s.readiness_score,
                s.readiness_status,
                CASE WHEN p.placement_id IS NOT NULL THEN 'PLACED' ELSE 'NOT PLACED' END as placement_status,
                c.company_name,
                c.package_lpa,
                (
                    SELECT GROUP_CONCAT(sk.skill_name, ', ')
                    FROM student_skills ss
                    JOIN skills sk ON ss.skill_id = sk.skill_id
                    WHERE ss.student_id = s.student_id
                ) as skills_list
            FROM students s
            LEFT JOIN placements p ON s.student_id = p.student_id AND p.placement_status = 'PLACED'
            LEFT JOIN companies c ON p.company_id = c.company_id
            WHERE {where_sql}
            ORDER BY {order_by}
            LIMIT %s OFFSET %s
        """
        query_params = list(params) + [limit, offset]
        cursor.execute(data_query, query_params)
        students = cursor.fetchall()

        total_pages = max(1, (total_records + limit - 1) // limit)

        return jsonify({
            "students": students,
            "total": total_records,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        })

    finally:
        cursor.close()
        db.close()


# =========================================================
# STUDENT DASHBOARD DATA HELPER
# =========================================================

def get_student_dashboard_data(student_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # STUDENT INFORMATION
        cursor.execute("""
            SELECT
                student_id,
                name,
                email,
                department,
                year,
                cgpa,
                gender,
                readiness_score,
                readiness_status
            FROM students
            WHERE student_id = %s
        """, (student_id,))
        student = cursor.fetchone()

        if not student:
            return None

        # PLACEMENT INFORMATION
        cursor.execute("""
            SELECT
                p.placement_id,
                p.student_id,
                p.company_id,
                p.placement_status,
                p.placement_date,
                c.company_name,
                c.industry,
                c.package_lpa
            FROM placements p
            LEFT JOIN companies c
                ON p.company_id = c.company_id
            WHERE p.student_id = %s
            ORDER BY p.placement_id DESC
        """, (student_id,))
        placements = cursor.fetchall()

        # STUDENT SKILLS
        cursor.execute("""
            SELECT
                ss.student_id,
                ss.skill_id,
                ss.proficiency,
                s.skill_name
            FROM student_skills ss
            INNER JOIN skills s
                ON ss.skill_id = s.skill_id
            WHERE ss.student_id = %s
            ORDER BY s.skill_name
        """, (student_id,))
        skills = cursor.fetchall()

        placement_status = "PLACED" if placements else "NOT PLACED"

        cursor.execute("SELECT ROUND(AVG(cgpa), 2) as college_avg FROM students")
        col_avg_row = cursor.fetchone()
        college_avg_cgpa = col_avg_row["college_avg"] if col_avg_row else 8.19

        cursor.execute("""
            SELECT ROUND(AVG(cgpa), 2) as dept_avg 
            FROM students 
            WHERE department = %s
        """, (student["department"],))
        dept_avg_row = cursor.fetchone()
        dept_avg_cgpa = dept_avg_row["dept_avg"] if dept_avg_row else 8.19

        prof_val_map = {"Expert": 100, "Advanced": 80, "Intermediate": 55, "Beginner": 30}
        skill_names = [s["skill_name"] for s in skills]
        skill_scores = [prof_val_map.get(s["proficiency"], 40) for s in skills]

        student_radar_json = json.dumps({
            "labels": skill_names,
            "scores": skill_scores
        })

        return {
            "student": student,
            "placements": placements,
            "skills": skills,
            "placement_status": placement_status,
            "placement_count": len(placements),
            "skill_count": len(skills),
            "college_avg_cgpa": college_avg_cgpa,
            "dept_avg_cgpa": dept_avg_cgpa,
            "student_radar_json": student_radar_json
        }

    finally:
        cursor.close()
        db.close()


# =========================================================
# STUDENT DASHBOARD ROUTE
# =========================================================

@app.route("/student/<int:student_id>")
def student_dashboard(student_id):
    data = get_student_dashboard_data(student_id)
    if not data:
        abort(404)
    return render_template("result.html", **data)


# =========================================================
# PERFORMANCE COMPLETION CERTIFICATE ROUTE
# =========================================================

@app.route("/student/<int:student_id>/certificate")
def student_certificate(student_id):
    data = get_student_dashboard_data(student_id)
    if not data:
        abort(404)
    return render_template("certificate.html", **data)


# =========================================================
# ADD NEW STUDENT (Admin Protected)
# =========================================================

@app.route("/student/add", methods=["GET", "POST"])
def add_student():
    if not admin_required():
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT company_id, company_name, package_lpa FROM companies ORDER BY company_name")
        companies = cursor.fetchall()

        cursor.execute("SELECT skill_id, skill_name FROM skills ORDER BY skill_name")
        all_skills = cursor.fetchall()

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            department = request.form.get("department", "").strip()
            year = request.form.get("year", "4th Year").strip()
            cgpa_str = request.form.get("cgpa", "8.0").strip()
            gender = request.form.get("gender", "Male").strip()
            placement_status = request.form.get("placement_status", "NOT PLACED").strip()
            company_id_val = request.form.get("company_id", "").strip()
            placement_date = request.form.get("placement_date", "").strip()

            if not name or not email:
                return render_template("add_student.html", companies=companies, all_skills=all_skills, error="Student Name and Email are mandatory.")

            try:
                cgpa = float(cgpa_str)
            except ValueError:
                return render_template("add_student.html", companies=companies, all_skills=all_skills, error="CGPA must be a valid number.")

            is_placed = (placement_status.upper() == "PLACED")
            selected_skill_ids = request.form.getlist("skill_ids")
            prof_map = {"Beginner": 3, "Intermediate": 5, "Advanced": 8, "Expert": 10}
            skill_points = 0

            for sid_val in selected_skill_ids:
                try:
                    sid = int(sid_val)
                    prof = request.form.get(f"proficiency_{sid}", "Intermediate").strip()
                    skill_points += prof_map.get(prof, 5)
                except ValueError:
                    pass

            cgpa_score = (cgpa / 10.0) * 40.0
            norm_skill_score = min(40.0, (skill_points / 45.0) * 40.0)
            status_score = 20.0 if is_placed else 10.0
            readiness_score = round(min(100.0, cgpa_score + norm_skill_score + status_score), 1)

            if readiness_score >= 85.0:
                readiness_status = "Elite Ready"
            elif readiness_score >= 72.0:
                readiness_status = "Job Ready"
            elif readiness_score >= 55.0:
                readiness_status = "Developing"
            else:
                readiness_status = "Needs Upskilling"

            cursor.execute("""
                INSERT INTO students (name, email, department, year, cgpa, gender, readiness_score, readiness_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, department, year, cgpa, gender, readiness_score, readiness_status))

            new_student_id = cursor.lastrowid

            if is_placed and company_id_val:
                try:
                    comp_id = int(company_id_val)
                    cursor.execute("""
                        INSERT INTO placements (student_id, company_id, placement_status, placement_date)
                        VALUES (%s, %s, %s, %s)
                    """, (new_student_id, comp_id, "PLACED", placement_date or None))
                except ValueError:
                    pass

            for sid_val in selected_skill_ids:
                try:
                    sid = int(sid_val)
                    prof = request.form.get(f"proficiency_{sid}", "Intermediate").strip()
                    cursor.execute("""
                        INSERT INTO student_skills (student_id, skill_id, proficiency)
                        VALUES (%s, %s, %s)
                    """, (new_student_id, sid, prof))
                except ValueError:
                    pass

            db.commit()
            return redirect(url_for("student_dashboard", student_id=new_student_id))

        return render_template("add_student.html", companies=companies, all_skills=all_skills)

    finally:
        cursor.close()
        db.close()


# =========================================================
# ADMIN - EDIT STUDENT
# =========================================================

@app.route("/student/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    if not admin_required():
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                student_id,
                name,
                email,
                department,
                year,
                cgpa,
                gender,
                readiness_score,
                readiness_status
            FROM students
            WHERE student_id = %s
        """, (student_id,))
        student = cursor.fetchone()

        if not student:
            abort(404)

        cursor.execute("""
            SELECT
                p.placement_id,
                p.company_id,
                p.placement_status,
                p.placement_date,
                c.company_name,
                c.package_lpa
            FROM placements p
            LEFT JOIN companies c
                ON p.company_id = c.company_id
            WHERE p.student_id = %s
            ORDER BY p.placement_id DESC
            LIMIT 1
        """, (student_id,))
        placement = cursor.fetchone()

        cursor.execute("""
            SELECT
                company_id,
                company_name,
                package_lpa
            FROM companies
            ORDER BY company_name
        """)
        companies = cursor.fetchall()

        cursor.execute("""
            SELECT
                skill_id,
                skill_name
            FROM skills
            ORDER BY skill_name
        """)
        all_skills = cursor.fetchall()

        cursor.execute("""
            SELECT
                skill_id,
                proficiency
            FROM student_skills
            WHERE student_id = %s
        """, (student_id,))
        current_skills = cursor.fetchall()

        current_skill_map = {
            int(skill["skill_id"]): (skill["proficiency"] or "")
            for skill in current_skills
        }

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip() or None
            department = request.form.get("department", "").strip() or None
            year_value = request.form.get("year", "4th Year").strip()
            cgpa_value = request.form.get("cgpa", "").strip()
            gender = request.form.get("gender", "Male").strip() or None

            placement_status = request.form.get("placement_status", "NOT PLACED").strip()
            company_id_value = request.form.get("company_id", "").strip()
            placement_date = request.form.get("placement_date", "").strip()

            if not name:
                return render_template(
                    "edit_student.html",
                    student=student,
                    placement=placement,
                    companies=companies,
                    all_skills=all_skills,
                    current_skill_map=current_skill_map,
                    error="Student name cannot be empty."
                )

            year = year_value or "4th Year"

            cgpa = student["cgpa"]
            if cgpa_value:
                try:
                    cgpa = float(cgpa_value)
                except ValueError:
                    return render_template(
                        "edit_student.html",
                        student=student,
                        placement=placement,
                        companies=companies,
                        all_skills=all_skills,
                        current_skill_map=current_skill_map,
                        error="CGPA must be a valid number."
                    )

            is_placed = (placement_status.upper() == "PLACED")
            if not is_placed:
                cursor.execute("""
                    DELETE FROM placements
                    WHERE student_id = %s
                """, (student_id,))
            else:
                if not company_id_value:
                    return render_template(
                        "edit_student.html",
                        student=student,
                        placement=placement,
                        companies=companies,
                        all_skills=all_skills,
                        current_skill_map=current_skill_map,
                        error="Please select a company for a placed student."
                    )

                try:
                    company_id = int(company_id_value)
                except ValueError:
                    return render_template(
                        "edit_student.html",
                        student=student,
                        placement=placement,
                        companies=companies,
                        all_skills=all_skills,
                        current_skill_map=current_skill_map,
                        error="Invalid company selected."
                    )

                if placement:
                    cursor.execute("""
                        UPDATE placements
                        SET
                            company_id = %s,
                            placement_status = %s,
                            placement_date = %s
                        WHERE placement_id = %s
                    """, (
                        company_id,
                        placement_status,
                        placement_date if placement_date else None,
                        placement["placement_id"]
                    ))
                else:
                    cursor.execute("""
                        INSERT INTO placements
                        (
                            student_id,
                            company_id,
                            placement_status,
                            placement_date
                        )
                        VALUES (%s, %s, %s, %s)
                    """, (
                        student_id,
                        company_id,
                        placement_status,
                        placement_date if placement_date else None
                    ))

            cursor.execute("""
                DELETE FROM student_skills
                WHERE student_id = %s
            """, (student_id,))

            selected_skill_ids = request.form.getlist("skill_ids")
            skill_points = 0
            prof_map = {"Beginner": 3, "Intermediate": 5, "Advanced": 8, "Expert": 10}

            for skill_id_value in selected_skill_ids:
                try:
                    skill_id = int(skill_id_value)
                except ValueError:
                    continue

                proficiency = request.form.get(f"proficiency_{skill_id}", "").strip() or "Beginner"
                skill_points += prof_map.get(proficiency, 4)

                cursor.execute("""
                    INSERT INTO student_skills
                    (
                        student_id,
                        skill_id,
                        proficiency
                    )
                    VALUES (%s, %s, %s)
                """, (student_id, skill_id, proficiency))

            cgpa_score = (cgpa / 10.0) * 40.0
            norm_skill_score = min(40.0, (skill_points / 45.0) * 40.0)
            status_score = 20.0 if is_placed else 10.0
            new_readiness = round(min(100.0, cgpa_score + norm_skill_score + status_score), 1)

            if new_readiness >= 85.0:
                new_status = "Elite Ready"
            elif new_readiness >= 72.0:
                new_status = "Job Ready"
            elif new_readiness >= 55.0:
                new_status = "Developing"
            else:
                new_status = "Needs Upskilling"

            cursor.execute("""
                UPDATE students
                SET
                    name = %s,
                    email = %s,
                    department = %s,
                    year = %s,
                    cgpa = %s,
                    gender = %s,
                    readiness_score = %s,
                    readiness_status = %s
                WHERE student_id = %s
            """, (name, email, department, year, cgpa, gender, new_readiness, new_status, student_id))

            db.commit()
            return redirect(url_for("student_dashboard", student_id=student_id))

        return render_template(
            "edit_student.html",
            student=student,
            placement=placement,
            companies=companies,
            all_skills=all_skills,
            current_skill_map=current_skill_map
        )

    except Exception as e:
        db.rollback()
        return render_template(
            "edit_student.html",
            student=student,
            placement=placement if "placement" in locals() else None,
            companies=companies if "companies" in locals() else [],
            all_skills=all_skills if "all_skills" in locals() else [],
            current_skill_map=current_skill_map if "current_skill_map" in locals() else {},
            error="Update failed: " + str(e)
        )

    finally:
        cursor.close()
        db.close()


# =========================================================
# RUN APPLICATION LOCALLY
# =========================================================

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
