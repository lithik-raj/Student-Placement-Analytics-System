import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
         password="bornl2006",
        database="placement_analytics"
    )

    if db.is_connected():
        print("✅ Python is connected to MySQL successfully!")

except Exception as e:
    print("❌ Connection failed!")
    print("Error:", e)

finally:
    try:
        db.close()
    except:
        pass