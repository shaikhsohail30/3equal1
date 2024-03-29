import os

from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
from flask_login import LoginManager
import sqlite3 as sql
import pdb



app = Flask(__name__)

login = LoginManager(app)

@app.route('/homepage/<user>')
def hello(user):
    return render_template('home.html', name=user)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/upload')
def upload_page():
    return render_template('uploader.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        dir = os.path.dirname(__file__)
        filename = secure_filename(f.filename)
        f.save(os.path.join(dir, 'upload_folder', filename))
        return 'file uploaded successfully'

@app.route('/sign-in', methods =['POST'] )
def sign_in():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            with sql.connect("database.db") as con:
                cur = con.cursor()

                con.commit()
        except:
            pass

    return render_template('login.html')


@app.route('/stud')
def new_student():
   return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO students (name,addr,city,pin)
                VALUES(?, ?, ?, ?)''', (nm, addr, city, pin))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("bootstrap-list.html", rows=rows)


@app.route('/students/api/v1.0/list', methods=['GET'])
def get_students():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    students_list = []
    for student in rows:
        students_list.append(
            {
                "name": student['name'],
                "address": student['addr'],
                "city": student['city'],
                "pincode": student['pin']
            }
        )
    return jsonify({'students': students_list})


@app.route('/student-post', methods=['POST'])
def post_students():
    if request.method == 'POST':
        try:
            nm = request.json['name']
            addr = request.json['addr']
            city = request.json['city']
            pin = request.json['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO students (name,addr,city,pin)
                VALUES(?, ?, ?, ?)''', (nm, addr, city, pin))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            cur = con.cursor()
            cur.execute("select * from students")

            rows = cur.fetchall()
            students_list = []
            for student in rows:
                students_list.append(
                    {
                        "name": student[0],
                        "address": student[1],
                        "city": student[2],
                        "pincode": student[3]
                    }
                )
            con.close()
    return jsonify({'students': students_list})




if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
