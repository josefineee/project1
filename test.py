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

# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={
#     "key": secrets.key, "isbns": "9781632168146"})
# # pprint.pprint(res.json())


@app.route("/")
def start():
    return render_template("index.html")




            <div class="text-center" style="padding:50px 0">
                <div class="logo">{%block head%}{%endblock%}</div>


                <!DOCTYPE html>
<html>
    <head>
        <title>Bookreads</title>
        <meta name='viewport' content='width=device-width, initial-scale=1.0' charset="UTF-8">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    </head>
    <body>
        <nav class="container-fluid navbar navbar-expand-lg navbar-light">
            <a class="navbar-brand" href="{{ url_for('start') }}">BookReads</a>
        </nav>