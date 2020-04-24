import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import secrets
import requests
import pprint
import psycopg2

app = Flask(__name__)
"""
Set environment for Flask in PS
$env:FLASK_APP = "application.py"
$env:FLASK_ENV = "development"
$env:DATABASE_URL = "postgres://ggzvnyybarupid:7c8053cbd4563994056b27c2a076ed862ac94beb57fea449e03325e7f7f73709@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d5hbh8gkn06142"
"""

# Set database environment
# os.environ["DATABASE_URL"] = secrets.DATABASE_URL

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
Session(app)
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

db.execute("SELECT * FROM Users")
db.commit()
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={
    "key": secrets.key, "isbns": "9781632168146"})
# pprint.pprint(res.json())


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/registration", methods=["POST"])
def reg():
    if request.method == "POST":
        u_name = request.form.get("reg_username")
        pw = request.form.get("reg_password")
        email = request.form.get("reg_email")
        #db.execute("INSERT INTO Users (username, password, email) VALUES (:name, :pw, :email)", 
        #{"name":u_name, "pw":pw , "email":email})
        #db.commit()
        return render_template("reg.html")
    else:
        return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")
