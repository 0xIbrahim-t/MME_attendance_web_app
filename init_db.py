# init_db.py
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='attendance_user',
    password='securepassword'
)

cursor = conn.cursor()

# Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_app")
cursor.execute("USE attendance_app")

# Create the students table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        name VARCHAR(50),
        rollnumber VARCHAR(20) PRIMARY KEY,
        password VARCHAR(255)
    )
""")

# Create the professors table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS professors (
        name VARCHAR(50),
        subject VARCHAR(50) PRIMARY KEY,
        password VARCHAR(255)
    )
""")

# Create the attendance table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rollnumber VARCHAR(20),
        subject VARCHAR(50),
        date DATE,
        FOREIGN KEY (rollnumber) REFERENCES students(rollnumber),
        FOREIGN KEY (subject) REFERENCES professors(subject)
    )
""")

conn.commit()
cursor.close()
conn.close()

