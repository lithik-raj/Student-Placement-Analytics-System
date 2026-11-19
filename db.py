import os
import sys
import sqlite3
import shutil
from generate_data import generate_1200_database

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
    """
    Initializes the SQLite database with 1,200 students.
    If a bundled pre-generated database exists, copies it instantly.
    Otherwise, generates the full 1,200 student dataset on the fly.
    """
    bundled_db = os.path.join(BASE_DIR, "placement_analytics.db")

    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        if os.path.exists(bundled_db) and os.path.abspath(bundled_db) != os.path.abspath(db_path):
            shutil.copy2(bundled_db, db_path)
            return

        generate_1200_database(db_path)
    else:
        # Check if table exists and has students
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM students")
            cnt = cur.fetchone()[0]
            conn.close()
            if cnt < 1200:
                if os.path.exists(bundled_db) and os.path.abspath(bundled_db) != os.path.abspath(db_path):
                    shutil.copy2(bundled_db, db_path)
                else:
                    generate_1200_database(db_path)
        except Exception:
            generate_1200_database(db_path)


def get_db_connection():
    """
    Connects to MySQL if host is specified and accessible,
    otherwise seamlessly connects to SQLite with the 1,200 student dataset.
    """
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
