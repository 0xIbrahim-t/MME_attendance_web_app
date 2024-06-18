# load_users.py
import mysql.connector
from werkzeug.security import generate_password_hash

def load_users(filename, table, user_type):
    conn = mysql.connector.connect(
        host='localhost',
        user='attendance_user',
        password='securepassword',
        database='attendance_app'
    )
    cursor = conn.cursor()

    with open(filename, 'r') as file:
        for line in file:
            name, username, password = line.strip().split()
            hashed_password = generate_password_hash(password)
            if user_type == 'student':
                cursor.execute("INSERT IGNORE INTO students (name, rollnumber, password) VALUES (%s, %s)", (name, username, hashed_password))
            elif user_type == 'professor':
                cursor.execute("INSERT IGNORE INTO professors (name, subject, password) VALUES (%s, %s)", (name, username, hashed_password))

    conn.commit()
    cursor.close()
    conn.close()

load_users('students.txt', 'students', 'student')
load_users('professors.txt', 'professors', 'professor')
