from flask import Flask, render_template, redirect, request, url_for, session
import sqlite3
app = Flask (__name__)
import os
conn = sqlite3.connect("user.db", timeout=5, check_same_thread=False)
cur = conn.cursor()

cmd = "CREATE TABLE IF NOT EXISTS users( id INTEGER PRIMARY KEY, username TEXT UNIQUE, passcode INTEGER)"

cur.execute (cmd)

conn.commit()
conn.close()

messages = []
app.secret_key = "1234"

@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')


@app.route ('/')
def index ():
    return render_template ('index.html')

@app.route ('/profile', methods = ["GET", "POST"])
def editprofile ():
    pass

@app.route('/commonroom', methods = ["GET", "POST"])
def commonroom ():
    if request.method == "POST":
        new_message = request.form ['message']
        user = session["username"]
        messages.append ({"user":user, "text" : new_message})
        return redirect(url_for ("commonroom"))
    return render_template ('commonroom.html', messages = messages)

@app.route ('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form ['username']
        passcode = request.form ['passcode']
        cmd = "SELECT passcode FROM users WHERE username = ?"
        conn = sqlite3.connect ("user.db", timeout=5, check_same_thread=False)
        cur = conn.cursor ()
        cur.execute (cmd, (username,))
        row = cur.fetchone()
        conn.close ()
        if row:
            if row[0] == int (passcode):
                session["username"] = username
                print ("access granted")
                return redirect (url_for ('commonroom'))
    return render_template ('login.html')

@app.route ('/register', methods = ["GET", "POST"])
def register ():
    if request.method == "POST":
        username = request.form ["username"]
        passcode = request.form ["passcode"]
        conn = sqlite3.connect ("user.db", timeout=5, check_same_thread=False)
        cur = conn.cursor()
        cmd = "INSERT INTO users (username, passcode) values (? , ?)"
        cur.execute (cmd, (username, passcode))
        conn.commit ()
        conn.close ()
        return redirect (url_for('login'))
    return render_template ("register.html")

from flask import send_file

@app.route("/download_db")
def download_db():
    return send_file("user.db", as_attachment=True)

if __name__ == "__main__":
    app.run (debug=True, host="0.0.0.0")



