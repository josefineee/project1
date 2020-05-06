import os
import datetime
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
SECRET_KEY = os.urandom(32)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=5)
app.config['SECRET_KEY'] = SECRET_KEY
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
            return render_template("welcome.html", form=form, last_updated=dir_last_updated('project1/static'))
        else:
            #User already logged in should be directed to homepage

            return render_template("index.html", username=session.get("user_name"), last_updated=dir_last_updated('project1/static'))
    else:
        q = ""
        if request.form.get("books-isbn") not in [None, ""]:
            q = "AND isbn LIKE :i "
        if request.form.get("book-title") not in [None, ""]:
            q += "AND title LIKE :t "
        if request.form.get("book-author") not in [None, ""]:
            q += "AND author LIKE :a "
        if request.form.get("publish-year") not in [None, ""]:
            q += "AND year LIKE :y"
        print("SELECT * FROM books WHERE (isbn LIKE :f OR title LIKE :f OR author LIKE :f OR year LIKE :f) {}".format(q))
        results = db.execute("SELECT * FROM books WHERE isbn LIKE :f OR title LIKE :f OR author LIKE :f OR year LIKE :f {}".format(q),
                            {"i":('%'+ request.form.get("books-isbn")+'%'), "t":('%'+ request.form.get("book-title")+ '%'), "a":('%' + request.form.get("book-author") + '%'), "y":('%' + request.form.get("publish-year") + '%'), "f":('%' + request.form.get("free-text")+ '%')})
        if results is None:
            return redirect(url_for('mypages', username=session.get("user_name")))
        return render_template("search.html", results=results, username=session.get("user_name"), last_updated=dir_last_updated('project1/static'))

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
        return render_template("welcome.html", form=form,clast_updated=dir_last_updated('project1/static'))

        
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
        return render_template("login.html", form=form, last_updated=dir_last_updated('project1/static'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("start"))

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")

@app.route("/mypages/<username>")
def mypages(username):
    return render_template("mypages.html", username=session["user_name"], last_updated=dir_last_updated('project1/static'))

@app.route("/book/<bookid>")
def book(bookid):
    book = db.execute("SELECT * FROM books WHERE id=:id", {"id":bookid}).fetchone()
    return render_template("book.html", bookid=book.id, book=book, username=session["user_name"], last_updated=dir_last_updated('project1/static'))

@app.route("/static/pictures/book3.jpg")
def get_img():
   return app.send_static_file("http://127.0.0.1/8080/static/pictures/book3.jpg")
