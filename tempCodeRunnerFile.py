from flask import Flask, render_template, abort, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

app.secret_key = "placement_analytics_admin_secret_key"

ADMIN_USERNAME = "lithikportal@gmail.com"
ADMIN_PASSWORD = "lithik@123"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="bornl2006",
        database="placement_analytics"
    )


# =========================================================
# ADMIN LOGIN
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
            error="Invalid Login ID or Password."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)

    return redirect(url_for("home"))


def admin_required():
    return session.get("admin_logged_in", False)


# =========================================================
# HOME / MAIN DASHBOARD
# =========================================================

@app.route("/")
def home():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:

        cursor.execute(
            "SELECT COUNT(*) AS total FROM students"
        )
        total_students = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total FROM placements"
        )
        total_placements = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total FROM companies"
        )
        total_companies = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total FROM skills"
        )
        total_skills = cursor.fetchone()["total"]

        unplaced_students = total_students - total_placements

        if total_students > 0:
            placement_percentage = round(
                (total_placements / total_students) * 100,
                2
            )
        else:
            placement_percentage = 0

        cursor.execute("""
            SELECT
                student_id,
                name,
                department
            FROM students
            ORDER BY student_id
        """)

        students = cursor.fetchall()

        cursor.execute("""
            SELECT
                s.department,
                COUNT(DISTINCT s.student_id) AS total_students,
                COUNT(DISTINCT p.student_id) AS placed_students
            FROM students s
            LEFT JOIN placements p
                ON s.student_id = p.student_id
            GROUP BY s.department
            ORDER BY placed_students DESC
        """)

        department_data = cursor.fetchall()

        return render_template(
            "index.html",
            total_students=total_students,
            total_placements=total_placements,
            total_companies=total_companies,
            total_skills=total_skills,
            unplaced_students=unplaced_students,
            placement_percentage=placement_percentage,
            students=students,
            department_data=department_data
        )

    finally:

        cursor.close()
        db.close()


# =========================================================
# STUDENT DASHBOARD DATA
# =========================================================

def get_student_dashboard_data(student_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:

        # -------------------------------------------------
        # STUDENT INFORMATION
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                student_id,
                name,
                email,
                department,
                year,
                cgpa,
                gender
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        student = cursor.fetchone()

        if not student:
            return None


        # -------------------------------------------------
        # PLACEMENT INFORMATION
        # -------------------------------------------------

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


        # -------------------------------------------------
        # STUDENT SKILLS
        # -------------------------------------------------

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


        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        placement_status = (
            "PLACED"
            if placements
            else "NOT PLACED"
        )


        return {
            "student": student,
            "placements": placements,
            "skills": skills,
            "placement_status": placement_status,
            "placement_count": len(placements),
            "skill_count": len(skills)
        }

    finally:

        cursor.close()
        db.close()


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@app.route("/student/<int:student_id>")
def student_dashboard(student_id):

    data = get_student_dashboard_data(student_id)

    if not data:
        abort(404)

    return render_template(
        "result.html",
        **data
    )


# =========================================================
# ADMIN - EDIT STUDENT
# =========================================================

@app.route(
    "/student/<int:student_id>/edit",
    methods=["GET", "POST"]
)
def edit_student(student_id):

    # -----------------------------------------------------
    # ADMIN ONLY
    # -----------------------------------------------------

    if not admin_required():
        return redirect(url_for("login"))


    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:

        # =================================================
        # GET STUDENT
        # =================================================

        cursor.execute("""
            SELECT
                student_id,
                name,
                email,
                department,
                year,
                cgpa,
                gender
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        student = cursor.fetchone()

        if not student:
            abort(404)


        # =================================================
        # GET CURRENT PLACEMENT
        # =================================================

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


        # =================================================
        # GET ALL COMPANIES
        # =================================================

        cursor.execute("""
            SELECT
                company_id,
                company_name,
                package_lpa
            FROM companies
            ORDER BY company_name
        """)

        companies = cursor.fetchall()


        # =================================================
        # GET ALL AVAILABLE SKILLS
        # =================================================

        cursor.execute("""
            SELECT
                skill_id,
                skill_name
            FROM skills
            ORDER BY skill_name
        """)

        all_skills = cursor.fetchall()


        # =================================================
        # GET STUDENT'S CURRENT SKILLS
        # =================================================

        cursor.execute("""
            SELECT
                skill_id,
                proficiency
            FROM student_skills
            WHERE student_id = %s
        """, (student_id,))

        current_skills = cursor.fetchall()


        # Create dictionary:
        # skill_id -> proficiency

        current_skill_map = {}

        for skill in current_skills:

            current_skill_map[
                int(skill["skill_id"])
            ] = skill["proficiency"] or ""


        # =================================================
        # POST - SAVE CHANGES
        # =================================================

        if request.method == "POST":

            # -------------------------------------------------
            # STUDENT INFORMATION
            # -------------------------------------------------

            name = request.form.get(
                "name",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip()

            department = request.form.get(
                "department",
                ""
            ).strip()

            year_value = request.form.get(
                "year",
                ""
            ).strip()

            cgpa_value = request.form.get(
                "cgpa",
                ""
            ).strip()

            gender = request.form.get(
                "gender",
                ""
            ).strip()


            # -------------------------------------------------
            # PLACEMENT INFORMATION
            # -------------------------------------------------

            placement_status = request.form.get(
                "placement_status",
                "NOT PLACED"
            ).strip()

            company_id_value = request.form.get(
                "company_id",
                ""
            ).strip()

            placement_date = request.form.get(
                "placement_date",
                ""
            ).strip()


            # -------------------------------------------------
            # VALIDATE NAME
            # -------------------------------------------------

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


            # -------------------------------------------------
            # YEAR
            # -------------------------------------------------

            if year_value:

                try:
                    year = int(year_value)

                except ValueError:

                    return render_template(
                        "edit_student.html",
                        student=student,
                        placement=placement,
                        companies=companies,
                        all_skills=all_skills,
                        current_skill_map=current_skill_map,
                        error="Year must be a valid number."
                    )

            else:

                year = None


            # -------------------------------------------------
            # CGPA
            # -------------------------------------------------

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

            else:

                cgpa = None


            # -------------------------------------------------
            # EMPTY OPTIONAL VALUES
            # -------------------------------------------------

            if not email:
                email = None

            if not department:
                department = None

            if not gender:
                gender = None


            # =================================================
            # UPDATE STUDENT
            # =================================================

            cursor.execute("""
                UPDATE students
                SET
                    name = %s,
                    email = %s,
                    department = %s,
                    year = %s,
                    cgpa = %s,
                    gender = %s
                WHERE student_id = %s
            """, (
                name,
                email,
                department,
                year,
                cgpa,
                gender,
                student_id
            ))


            # =================================================
            # UPDATE PLACEMENT
            # =================================================

            if placement_status.upper() == "NOT PLACED":

                cursor.execute("""
                    DELETE FROM placements
                    WHERE student_id = %s
                """, (student_id,))


            else:

                # ---------------------------------------------
                # COMPANY REQUIRED
                # ---------------------------------------------

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

                    company_id = int(
                        company_id_value
                    )

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


                # ---------------------------------------------
                # UPDATE EXISTING PLACEMENT
                # ---------------------------------------------

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
                        placement_date
                        if placement_date
                        else None,
                        placement["placement_id"]
                    ))


                # ---------------------------------------------
                # CREATE NEW PLACEMENT
                # ---------------------------------------------

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
                        placement_date
                        if placement_date
                        else None
                    ))


            # =================================================
            # UPDATE STUDENT SKILLS
            # =================================================

            # First remove existing skill records
            # for this student.

            cursor.execute("""
                DELETE FROM student_skills
                WHERE student_id = %s
            """, (student_id,))


            # -------------------------------------------------
            # Read selected skills
            #
            # edit_student.html should send:
            #
            # skill_ids = selected skill IDs
            # proficiency_<skill_id> = proficiency
            # -------------------------------------------------

            selected_skill_ids = request.form.getlist(
                "skill_ids"
            )


            # -------------------------------------------------
            # Insert selected skills
            # -------------------------------------------------

            for skill_id_value in selected_skill_ids:

                try:

                    skill_id = int(
                        skill_id_value
                    )

                except ValueError:

                    continue


                proficiency = request.form.get(
                    f"proficiency_{skill_id}",
                    ""
                ).strip()


                # Default proficiency
                if not proficiency:
                    proficiency = "Beginner"


                cursor.execute("""
                    INSERT INTO student_skills
                    (
                        student_id,
                        skill_id,
                        proficiency
                    )
                    VALUES (%s, %s, %s)
                """, (
                    student_id,
                    skill_id,
                    proficiency
                ))


            # =================================================
            # SAVE EVERYTHING
            # =================================================

            db.commit()


            # =================================================
            # RETURN TO STUDENT DASHBOARD
            # =================================================

            return redirect(
                url_for(
                    "student_dashboard",
                    student_id=student_id
                )
            )


        # =================================================
        # GET REQUEST - SHOW EDIT PAGE
        # =================================================

        return render_template(
            "edit_student.html",
            student=student,
            placement=placement,
            companies=companies,
            all_skills=all_skills,
            current_skill_map=current_skill_map
        )


    # =====================================================
    # ERROR HANDLING
    # =================================================

    except Exception as e:

        db.rollback()

        return render_template(
            "edit_student.html",
            student=student,
            placement=placement
            if "placement" in locals()
            else None,
            companies=companies
            if "companies" in locals()
            else [],
            all_skills=all_skills
            if "all_skills" in locals()
            else [],
            current_skill_map=current_skill_map
            if "current_skill_map" in locals()
            else {},
            error="Update failed: " + str(e)
        )


    finally:

        cursor.close()
        db.close()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)

