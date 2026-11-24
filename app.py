from flask import Flask, render_template, request, redirect, session 
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app=Flask(__name__)
app.secret_key="skdnsidn@121323o0@*@(@*@@_!_@(#))" 

def create_table(): 
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username text unique,password text)""")
    conn.commit()
    conn.close()

@app.route("/register",methods=["GET","POST"])
def register(): 
    if request.method=="POST": 
        username=request.form["username"]
        password=request.form["password"]
        hashed_password=generate_password_hash(password)
        conn=sqlite3.connect("users.db")
        cursor=conn.cursor()
        try: 
            cursor.execute("INSERT INTO users (username,password) VALUES(?,?)", (username,hashed_password))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError: 
            return("Username already exists")
        finally: 
            conn.close()
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login(): 
    if request.method=="POST": 
        username=request.form['username']
        password=request.form['password']
        conn=sqlite3.connect("users.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users where username = ?",(username,))
        user=user.fetchone()
        conn.close()
        if user and check_password_hash(user[2],password): 
            session["username"]=username
            return redirect("/dashboard")
        else:
            return "Invalid username and password"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard(): 
    if "username" in session: 
        return render_template("dashboard.html",username=session["username"])
    return redirect("/login")

@app.route("/logout")
def logout(): 
    session.pop("username",None)
    return redirect("/login")

create_table()
app.run(debug=True)