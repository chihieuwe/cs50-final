from flask import Flask, render_template, request, flash, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
db = SQL("sqlite:///pet.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    if request.method == "POST":
        ...
    else: 
        return render_template("login.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("confirmation")
        checkmail = db.execute("SELECT * FROM users WHERE email = ?", email)
        if not name:
            flash("Name cannot be blank")
            return redirect("/register")
        if not email:
            flash("Email cannot be blank")
            return redirect("/register")
        if not password:
            flash("Password cannot be blank")
            return redirect("/register")
        if '@' not in email or email.isnumeric == True:
            flash("Email not valid")
            return redirect("/register")
        if checkmail:
            flash("Email already exists!")
            return redirect("/register")
        else:
            db.execute("INSERT INTO users (name, email, hash) VALUES (?, ?, ?)", name, email, generate_password_hash(password))
            flash("Registered successfully!")
        return redirect("/register")
    else:
        return render_template("register.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt')