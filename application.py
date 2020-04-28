import os

from flask import Flask, session, render_template, request, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import secrets
import requests
import pprint
import psycopg2
from extra import RegistrationForm, LoginForm
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from werkzeug import generate_password_hash

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
s = scoped_session(sessionmaker(bind=engine))
db = s()

# Session
# session["logged_in"] = True/False
# session["user_id"] = user_id
# session["user_name"] = username


@app.route("/", methods=["GET"])
def start():
    print(request.form)
    print(request.method)
    form = RegistrationForm(request.form)
    if session.get("logged_user") is None:
        # No stored session needs to log in
        return render_template("welcome.html", form=form)
    else:
        #User already logged in should be directed to homepage
        return render_template("index.html", username=session.get("user_name"))

@app.route("/registration", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        form = RegistrationForm(request.form)
        if form.validate():
            if not db.execute("SELECT name FROM users WHERE name=:name", {"name":form.name.data}):
                return render_template("login_error.html", error_msg="Sorry username taken")
            elif not db.execute("SELECT email FROM users WHERE email=:email", {"email":form.email.data}):
                return render_template("login_error.html", error_msg="Email already assign to an account")
            else: 
                db.execute("INSERT INTO users (name, password, email) VALUES (:name, :pw, :email)", 
                {"name":form.name.data, "pw":generate_password_hash(form.password.data),
                "email":form.email.data})
                db.commit()
                flash("SUCCESS!")
                return redirect(url_for('login'))
        else:
            return render_template("login_error.html", error_msg = "Form isn't validated, contact page-admin.")
    else: 
        form = RegistrationForm(request.form)
        return render_template("welcome.html", form=form)



        
@app.route("/login", methods=["POST", "GET"])
def login():
    form=LoginForm(request.form)
    if request.method == "POST" and form.validate:
        users = db.execute("SELECT name, password FROM users WHERE name=:name", {"name":form.name.data})
        if users is None:
            return redirect(url_for('login'))
        #if check_password_hash(users.password): 
            #session["logged_in"] = True
           # session["user_id"] = users.id
           #  session["user_name"] = users.name
           # return redirect(url_for('start')
    else: 
        return render_template("login.html", form=form)

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")