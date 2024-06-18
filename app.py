# app.py
import mysql.connector
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='attendance_user',
        password='securepassword',
        database='attendance_app'
    )

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        if user_type == 'student':
            cursor.execute("SELECT password FROM students WHERE rollnumber = %s", (username,))
        elif user_type == 'professor':
            cursor.execute("SELECT password FROM professors WHERE subject = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user[0], password):
            session['user_type'] = user_type
            session['username'] = username
            if user_type == 'student':
                return redirect(url_for('student_dashboard'))
            elif user_type == 'professor':
                return redirect(url_for('professor_dashboard'))
    return redirect(url_for('index'))

@app.route('/student')
def student_dashboard():
    if 'user_type' in session and session['user_type'] == 'student':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students WHERE rollnumber = %s", (session['username'],))
        result = cursor.fetchone()
        name = result[0]
        cursor.execute("SELECT subject FROM professors")
        subjects = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('student.html', rollnumber=session['username'], subjects=subjects, name=name)
    return redirect(url_for('index'))

@app.route('/student/<subject>')
def view_attendance(subject):
    if 'user_type' in session and session['user_type'] == 'student':
        rollnumber = session['username']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE subject = %s", (rollnumber))
        total_classes = cursor.fetchone()[0]
        cursor.execute("SELECT date FROM attendance WHERE rollnumber = %s AND subject = %s", (rollnumber, subject))
        absent_dates = cursor.fetchall()
        cursor.close()
        conn.close()
        attendance_percentage = ((total_classes - len(absent_dates)) / total_classes) * 100 if total_classes > 0 else 0
        return render_template('attendance.html', subject=subject, total_classes=total_classes, absent_dates=[d[0] for d in absent_dates], attendance_percentage=attendance_percentage)
    return redirect(url_for('index'))

@app.route('/professor')
def professor_dashboard():
    if 'user_type' in session and session['user_type'] == 'professor':
        cursor.execute("SELECT name FROM professors WHERE subject = ?", (session['username'],))
        result = cursor.fetchone()
        name = result[0]
        return render_template('professor.html', subject=session['username'], name=name)
    return redirect(url_for('index'))

@app.route('/professor/mark_attendance', methods=['POST'])
def mark_attendance():
    if 'user_type' in session and session['user_type'] == 'professor':
        date = request.form['date']
        absentees = request.form['absentees'].split(',')
        subject = session['username']
        conn = get_db_connection()
        cursor = conn.cursor()
        for absentee in absentees:
            rollnumber = f"1121230{absentee.strip()}"
            cursor.execute("INSERT INTO attendance (rollnumber, subject, date) VALUES (%s, %s, %s)", (rollnumber, subject, date))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('professor_dashboard'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
