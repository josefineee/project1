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

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# Session
# session["logged_in"] = True/False
# session["user_id"] = user_id
# session["user_name"] = username

def dir_last_updated(folder):
    return str(max((os.path.getmtime(os.path.join(ROOT_PATH, f))
                   for ROOT_PATH, dirs, files in os.walk(folder)
                   for f in files), default=0))


@app.route("/", methods=["GET", "POST"])
def start():
    form = RegistrationForm(request.form)
    if request.method == "GET":
        if session.get("logged_in") is not True:
            # No stored session needs to log in
            return render_template("welcome.html", form=form)
        else:
            #User already logged in should be directed to homepage
            return render_template("index.html", username=session.get("user_name"), last_updated=dir_last_updated('project1/static'))
    else:
        search= {"freetext": request.form.get("free-text"), 
                "title": request.form.get("book-title"), 
                "author":request.form.get("book-author"),
                "isbn" : request.form.get("books-isbn"),
                "year" :request.form.get("publish-year")}

        print(search)
        # for k in search.copy():
        #     if search[k] is None:
        #         del search[k]
        
        # print(search)
        results = db.execute("SELECT * FROM books WHERE isbn=:i OR title=:t OR author=:a OR year=:y",
                    {"isbn":search["isbn"], "title":search["title"], 
                    "author":search["author"], "year":search["year"]})
        return render_template("search.html", results=results)

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
        res = db.execute("SELECT password,id, name FROM users WHERE name=:name", {"name":form.name.data}).fetchone()
        
        if res == None:
            flash("The username doesn't exsist")
            return redirect(url_for('login'))
        
        check_pw = check_password_hash(res.password, form.password.data)
        if check_pw is False:
            flash("Wrong password")
            return redirect(url_for('login'))
        else:
            session["logged_in"] = True
            session["user_id"] = res.id
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