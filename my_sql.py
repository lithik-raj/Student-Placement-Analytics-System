import os

try:
    import mysql.connector
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

host = os.environ.get("MYSQL_HOST", "localhost")
user = os.environ.get("MYSQL_USER", "root")
password = os.environ.get("MYSQL_PASSWORD", "bornl2006")
database = os.environ.get("MYSQL_DATABASE", "placement_analytics")
port = int(os.environ.get("MYSQL_PORT", 3306))

if not HAS_MYSQL:
    print("⚠️ mysql-connector-python is not installed in the current environment.")
    print("Install it with: pip install mysql-connector-python")
else:
    try:
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connection_timeout=5
        )

        if db.is_connected():
            print(f"✅ Successfully connected to MySQL database '{database}' on {host}:{port}!")

    except Exception as e:
        print("❌ Connection failed!")
        print("Error:", e)
        print("\nNote: When deployed to Vercel, the application automatically uses a high-performance SQLite engine with pre-seeded data if MySQL is not configured.")

    finally:
        try:
            db.close()
        except Exception:
            pass
