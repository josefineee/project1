import os

from flask import Flask, session, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import secrets
import requests
import pprint
import psycopg2

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

table = db.execute("SELECT * FROM users")
db.commit() 

pprint.pprint(table)

@app.route("/")
def start():
    if not session.get("logged_in"):
        return render_template("welcome.html")
    else:
        return render_template("index.html", username=session["user_name"])

@app.route("/registration", methods=["POST"])
def reg():
    if request.method == "POST":
        users = db.execute("SELECT name, email FROM users")
        for user in users:
            if user.name == request.form.get("reg_username"):
                return "Sorry username taken"
            elif user.email == request.form.get("reg_email"):
                return "Email already assign to an account"
            else: 
                u_name = request.form.get("reg_username")
                pw = request.form.get("reg_password")
                email = request.form.get("reg_email")
                db.execute("INSERT INTO users (name, password, email) VALUES (:name, :pw, :email)", 
                {"name":u_name, "pw":pw , "email":email})
                db.commit()
                return render_template("reg.html")
    else:
        return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        users = db.execute("SELECT name, password FROM users WHERE ")
        return start()
    else: 
        return render_template("login.html")

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")