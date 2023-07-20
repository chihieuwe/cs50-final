from flask import Flask, render_template, request, flash, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from functools import wraps
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

# Establish database connection
db = SQL("sqlite:///pet.db")

def usd(value):
    return f"${value:,.2f}"
# Custom filter
app.jinja_env.filters["usd"] = usd

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/order")
@login_required
def order():
    return render_template("order.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt')

@app.route("/profile")
@login_required
def profile():
    username = db.execute("SELECT * FROM users WHERE name = ?", session["username"])
    return render_template("profile.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt', username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email:
            flash("Email cannot be blank", "error")
            return redirect("/login")
        if not password:
            flash("Password cannot be blank", "error")
            return redirect("/login")
        else:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE email = ?", email)

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                flash("Login failed", "error")
                return redirect("/login")

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            session["username"] = rows[0]["name"]
            session["email"] = rows[0]["email"]

            # Redirect user to home page
            return render_template("index.html")
    else: 
        return render_template("login.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("confirmation")
        checkmail = db.execute("SELECT * FROM users WHERE email = ?", email)
        if not name:
            flash("Name cannot be blank", "error")
            return redirect("/register")
        if not email:
            flash("Email cannot be blank", "error")
            return redirect("/register")
        if not password:
            flash("Password cannot be blank", "error")
            return redirect("/register")
        if '@' not in email or email.isnumeric == True:
            flash("Email not valid", "error")
            return redirect("/register")
        if checkmail:
            flash("Email already exists!", "error")
            return redirect("/register")
        else:
            db.execute("INSERT INTO users (name, email, hash) VALUES (?, ?, ?)", name, email, generate_password_hash(password))
            flash("Registered successfully!", "success")
        return redirect("/register")
    else:
        return render_template("register.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt')