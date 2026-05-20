from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Student Management-secret-key'

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Radhey@447",
        database="student_db"
    )

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("index.html", students=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name   = request.form['name'].strip()
        age    = request.form['age'].strip()
        course = request.form['course'].strip()

        if not name or not age or not course:
            flash('All fields are required.', 'error')
            return render_template("add.html")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
            (name, age, course)
        )
        db.commit()
        cursor.close()
        db.close()
        flash(f'{name} has been enrolled successfully!', 'success')
        return redirect('/')
    return render_template("add.html")

@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM students WHERE id=%s", (id,))
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM attendance WHERE student_id=%s", (id,))
        cursor.execute("DELETE FROM students WHERE id=%s", (id,))
        db.commit()
        flash(f'{row[0]} has been removed.', 'success')
    cursor.close()
    db.close()
    return redirect('/')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        student_id = request.form['student_id']
        attendance_date = request.form['attendance_date']
        status = request.form['status']
        query = "INSERT INTO attendance (student_id, attendance_date, status) VALUES (%s, %s, %s)"
        cursor.execute(query, (student_id, attendance_date, status))
        db.commit()
        cursor.close()
        db.close()
        flash('Attendance marked successfully!', 'success')
        return redirect('/view_attendance')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students ORDER BY name ASC")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('attendance.html', students=students)

@app.route('/view_attendance')
def view_attendance():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attendance")
    attendance_list = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('view_attendance.html', attendance_list=attendance_list)

if __name__ == '__main__':
    app.run(debug=True)