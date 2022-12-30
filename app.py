import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user = "postgres",
                        password = "111",
                        host = "localhost",
                        port = "5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get("username")
            password = request.form.get("password")
            if username == "" or password == "":
                return render_template('gg.html')
            else:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
                records = list(cursor.fetchall())
                if records == []:
                    return render_template('wrong.html')
                else:
                    return render_template('account.html', full_name=records[0][1], log= str(username), passw=str(password))
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if login == "" or password == "" or name == "":
            return render_template('gg.html')
        else:
            cursor.execute("SELECT login FROM service.users WHERE login =%s OR password=%s", (str(login), str(password)))
            records = list(cursor.fetchall())
            print(records)
            rec = (login,)
            print (rec)
            if (login,) in records:
                 return render_template('useralreadyregistered.html')
            else:
                 cursor.execute("INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);", (str(name), str(login), str(password)))
                 conn.commit()
                 return redirect('/login/')
    return render_template('registration.html')

