import os
import sys
import sqlite3

# Try importing mysql.connector
try:
    import mysql.connector
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Vercel serverless environment check: /tmp is the only writable directory on Vercel
IS_VERCEL = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
DEFAULT_SQLITE_PATH = "/tmp/placement_analytics.db" if IS_VERCEL else os.path.join(BASE_DIR, "placement_analytics.db")
SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH", DEFAULT_SQLITE_PATH)


class SQLiteCursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        # Convert MySQL %s parameter placeholders to SQLite ? placeholders
        converted_query = query.replace("%s", "?")
        if params is not None:
            return self._cursor.execute(converted_query, params)
        return self._cursor.execute(converted_query)

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def fetchall(self):
        rows = self._cursor.fetchall()
        return [dict(r) for r in rows]

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    def close(self):
        try:
            self._cursor.close()
        except Exception:
            pass


class SQLiteConnectionWrapper:
    def __init__(self, conn):
        self._conn = conn

    def cursor(self, dictionary=True):
        return SQLiteCursorWrapper(self._conn.cursor())

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass


def init_sqlite_db(db_path=SQLITE_DB_PATH):
    """Initializes SQLite schema and inserts initial sample data if tables don't exist."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        department TEXT NOT NULL,
        year TEXT NOT NULL,
        cgpa REAL NOT NULL,
        gender TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        industry TEXT NOT NULL,
        package_lpa REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS placements (
        placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        company_id INTEGER,
        placement_status TEXT NOT NULL,
        placement_date TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT NOT NULL UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_skills (
        student_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        proficiency TEXT NOT NULL,
        PRIMARY KEY (student_id, skill_id),
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
    )
    """)

    # Check if data already seeded
    cur.execute("SELECT COUNT(*) FROM students")
    count = cur.fetchone()[0]

    if count == 0:
        # Seed Students
        students_data = [
            (1, "Lithik Raj B G", "lithikportal@gmail.com", "Artificial Intelligence & Data Science", "4th Year", 9.15, "Male"),
            (2, "Priya Sharma", "priya.sharma@example.com", "Computer Science & Engineering", "4th Year", 9.25, "Female"),
            (3, "Rahul Verma", "rahul.verma@example.com", "Information Technology", "4th Year", 8.45, "Male"),
            (4, "Ananya Iyer", "ananya.iyer@example.com", "Artificial Intelligence & Data Science", "4th Year", 9.38, "Female"),
            (5, "Karthik Raman", "karthik.r@example.com", "Electronics & Communication", "4th Year", 7.85, "Male"),
            (6, "Sneha Patel", "sneha.p@example.com", "Computer Science & Engineering", "4th Year", 8.70, "Female"),
            (7, "Arjun Das", "arjun.das@example.com", "Information Technology", "4th Year", 7.60, "Male"),
            (8, "Divya Krishnan", "divya.k@example.com", "Artificial Intelligence & Data Science", "4th Year", 9.05, "Female")
        ]
        cur.executemany("INSERT INTO students (student_id, name, email, department, year, cgpa, gender) VALUES (?, ?, ?, ?, ?, ?, ?)", students_data)

        # Seed Companies
        companies_data = [
            (1, "Google", "Technology & Cloud", 32.5),
            (2, "Microsoft", "Software & Cloud Services", 28.0),
            (3, "Amazon", "E-Commerce & AWS", 24.0),
            (4, "Zoho Corporation", "SaaS & Enterprise", 12.0),
            (5, "Tata Consultancy Services (TCS)", "IT Consulting", 7.5),
            (6, "Infosys", "Digital Services", 6.5)
        ]
        cur.executemany("INSERT INTO companies (company_id, company_name, industry, package_lpa) VALUES (?, ?, ?, ?)", companies_data)

        # Seed Skills
        skills_data = [
            (1, "Python"),
            (2, "Machine Learning"),
            (3, "SQL & Database Design"),
            (4, "Deep Learning"),
            (5, "Data Structures & Algorithms"),
            (6, "React & Frontend"),
            (7, "Flask & REST APIs"),
            (8, "Cloud Computing (AWS/GCP)"),
            (9, "Computer Vision"),
            (10, "Natural Language Processing (NLP)")
        ]
        cur.executemany("INSERT INTO skills (skill_id, skill_name) VALUES (?, ?)", skills_data)

        # Seed Placements
        placements_data = [
            (1, 1, 1, "PLACED", "2026-10-15"),  # Lithik -> Google
            (2, 2, 2, "PLACED", "2026-09-20"),  # Priya -> Microsoft
            (3, 4, 3, "PLACED", "2026-10-02"),  # Ananya -> Amazon
            (4, 6, 4, "PLACED", "2026-10-10"),  # Sneha -> Zoho
            (5, 3, 5, "PLACED", "2026-11-01"),  # Rahul -> TCS
            (6, 8, 6, "PLACED", "2026-11-05")   # Divya -> Infosys
        ]
        cur.executemany("INSERT INTO placements (placement_id, student_id, company_id, placement_status, placement_date) VALUES (?, ?, ?, ?, ?)", placements_data)

        # Seed Student Skills
        student_skills_data = [
            # Lithik Raj B G
            (1, 1, "Expert"),
            (1, 2, "Expert"),
            (1, 3, "Advanced"),
            (1, 4, "Advanced"),
            (1, 7, "Expert"),
            # Priya Sharma
            (2, 1, "Advanced"),
            (2, 5, "Expert"),
            (2, 6, "Advanced"),
            (2, 3, "Advanced"),
            # Rahul Verma
            (3, 1, "Intermediate"),
            (3, 3, "Advanced"),
            (3, 5, "Intermediate"),
            # Ananya Iyer
            (4, 1, "Expert"),
            (4, 2, "Expert"),
            (4, 9, "Advanced"),
            (4, 10, "Expert"),
            # Karthik Raman
            (5, 1, "Intermediate"),
            (5, 3, "Beginner"),
            # Sneha Patel
            (6, 1, "Advanced"),
            (6, 6, "Expert"),
            (6, 7, "Advanced"),
            # Arjun Das
            (7, 3, "Intermediate"),
            (7, 5, "Intermediate"),
            # Divya Krishnan
            (8, 1, "Advanced"),
            (8, 2, "Advanced"),
            (8, 4, "Intermediate")
        ]
        cur.executemany("INSERT INTO student_skills (student_id, skill_id, proficiency) VALUES (?, ?, ?)", student_skills_data)

        conn.commit()

    conn.close()


def get_db_connection():
    """
    Connects to MySQL if host is specified and accessible,
    otherwise seamlessly connects to SQLite with pre-seeded demo data.
    """
    # Check if external MySQL host is provided in environment
    mysql_host = os.environ.get("MYSQL_HOST")
    use_sqlite = os.environ.get("USE_SQLITE", "").lower() in ("1", "true", "yes")

    if HAS_MYSQL and mysql_host and not use_sqlite:
        try:
            conn = mysql.connector.connect(
                host=mysql_host,
                user=os.environ.get("MYSQL_USER", "root"),
                password=os.environ.get("MYSQL_PASSWORD", "bornl2006"),
                database=os.environ.get("MYSQL_DATABASE", "placement_analytics"),
                port=int(os.environ.get("MYSQL_PORT", 3306)),
                connection_timeout=3
            )
            return conn
        except Exception as e:
            print(f"[DB] MySQL connection failed ({e}), falling back to SQLite.")

    # SQLite fallback (default on Vercel & demo environment)
    init_sqlite_db(SQLITE_DB_PATH)
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return SQLiteConnectionWrapper(conn)
