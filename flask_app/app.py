import os

from flask import Flask, render_template, request
import sqlite3 as sql
import pdb

app = Flask(__name__)


@app.route('/homepage/<user>')
def hello(user):
    return render_template('home.html', name=user)


@app.route('/students')
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

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
