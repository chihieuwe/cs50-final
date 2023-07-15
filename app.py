from flask import Flask, render_template, request 
from cs50 import SQL
app = Flask(__name__)
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
        ...
    else:
        return render_template("register.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt')