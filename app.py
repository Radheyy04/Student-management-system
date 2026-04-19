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
        cursor.execute("DELETE FROM students WHERE id=%s", (id,))
        db.commit()
        flash(f'{row[0]} has been removed.', 'success')
    cursor.close()
    db.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
