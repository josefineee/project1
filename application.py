import os
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import secrets
import requests
import pprint
import psycopg2
from extra import RegistrationForm, LoginForm
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CSRF 
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# db = s()

# Session
# session["logged_in"] = True/False
# session["user_id"] = user_id
# session["user_name"] = username


@app.route("/", methods=["GET"])
def start():
    form = RegistrationForm(request.form)
    if session.get("logged_in") is not True:
        # No stored session needs to log in
        return render_template("welcome.html", form=form)
    else:
        #User already logged in should be directed to homepage
        return render_template("index.html", username=session.get("user_name"))

@app.route("/registration", methods=["GET", "POST"])
def reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        if db.execute("SELECT name FROM users WHERE name=:name", {"name":form.name.data}).fetchone() is not None:
            flash("The username is already in use")
            return redirect(url_for('reg'))
        elif db.execute("SELECT email FROM users WHERE email=:email", {"email":form.email.data}).fetchone() is not None:
            flash("Email already assign to an account")
            return redirect(url_for('reg'))
        else: 
            db.execute("INSERT INTO users (name, password, email) VALUES (:name, :pw, :email)", 
            {"name":form.name.data, "pw":generate_password_hash(form.password.data),
            "email":form.email.data})
            db.commit()
            flash("New account registred please log in to access BookReads.")
            return redirect(url_for('login'))
    else: 
        return render_template("welcome.html", form=form)

        
@app.route("/login", methods=["POST", "GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        res = db.execute("SELECT password,id FROM users WHERE name=:name", {"name":form.name.data}).fetchone()
        # check_pw = check_password_hash(res("password"), form.password.data)
        # print(check_pw)
        #user_id = res["id"]
        #print(db_hash)
        # print(users("name"))
        if db.execute("SELECT name FROM users WHERE name=:name", {"name":form.name.data}).fetchone() is None:
            flash("The username doesn't exsist")
            return redirect(url_for('login'))
        
        # elif check_pw is False:
        #     flash("Wrong password")
        #     return redirect(url_for('login'))
        else:
            session["logged_in"] = True
            #session["user_id"] = users.id
            session["user_name"] = form.name.data
            return redirect(url_for('start'))
    else:
        return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("start"))

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")


          # hash_pw = check_password_hash(form.password.data)
        # pw_db = generate_password_hash(form.password.data)
        #if check_password_hash(users.password)