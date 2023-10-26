from flask import Flask, render_template, request, flash, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from functools import wraps
import os
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
    # Render index page
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/order", methods=["GET", "POST"])
@login_required
def order():
    service = db.execute("SELECT name, price FROM service")
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash[0]["cash"] # Get the cash's current value, because db.execute return a list of dict
    if request.method == "POST":
        # Get info from the form
        petname = request.form.get("petname")
        petage = request.form.get("petage")
        service_type = request.form.get("service")
        service_price = request.form.get("price")

        # Remove the $ sign for the service price & convert the price to int
        if service_price:
            service_price = service_price.replace("$", "")
            service_price = float(service_price)
            
        if not petname:
            flash("Pet name cannot be empty!", "error")
            return redirect("/order")
        elif not petage:
            flash("Pet age cannot be empty!", "error")
            return redirect("/order")
        elif petage.isnumeric() == False or int(petage) < 0:
            flash("Pet age must be greater than 0 and a number", "error")
            return redirect("/order")
        elif cash < service_price:
            flash("Your balance is not enough, please add more", "error")
            return redirect("/order")
        else:
            uploaded_file = request.files.get("file")
            if uploaded_file.filename != '':
                if uploaded_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        
        # Use os.path.join() to create the directory path
                    directory = os.path.join('static', 'images', 'user_img')
        
                    if not os.path.exists(directory):
                        os.makedirs(directory)
        
        # Use os.path.join() to create the file path on server
                    file_path = os.path.join(directory, uploaded_file.filename)
        
                    uploaded_file.save(file_path)
                    flash("Successful", "success")
                    # Update the cash after payment #
                    cash = cash - service_price
                    db.execute("INSERT INTO orders (name, age, service, user_id, image_path) VALUES (?, ?, ?, ?, ?)", petname, petage, service_type, session["user_id"], 'images/user_img/' + uploaded_file.filename)
                    # Update the cash after payment #
                    db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
                    return redirect("/order")
                else:
                    flash('Invalid file type! Please upload an image file', "error")
                    return redirect("/order")   
            else:
                flash("Successful", "success")
                # Update the cash after payment #
                cash = cash - service_price

                db.execute("INSERT INTO orders (name, age, service, user_id, order_status) VALUES (?, ?, ?, ?, ?)", petname, petage, service_type, session["user_id"], 1)
                
                # Update the cash after payment #
                db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
                return redirect("/order")
    return render_template("order.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt', service=service)

@app.route("/history")
@login_required
def history():
    # Get all the order history
    orders = db.execute("SELECT * FROM orders WHERE user_id = ?", session["user_id"])
    return render_template("history.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt', orders=orders)

@app.route("/cancel", methods=["GET", "POST"])
@login_required
def cancel():
    # Cancel the order
    if request.method == "POST":
        # Get the order id
        order_id = request.form.get("cancel")
        # Get the service name
        service = request.form.get("service")
        flash("Appointment canceled", "success")
        # Get the service price
        price = db.execute("SELECT price FROM service WHERE name = ?", service)
        price = price[0]["price"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_cash = user_cash[0]["cash"]
        cash_current = price + user_cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_current, session["user_id"])
        db.execute("DELETE FROM orders WHERE id = ? AND user_id = ?", order_id, session["user_id"])
        return redirect("/history")
    else:
        return redirect("/history")

@app.route("/profile")
@login_required
def profile():
    # Query and display user information
    username = db.execute("SELECT * FROM users WHERE name = ? AND id = ?", session["username"], session["user_id"])
    return render_template("profile.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt', username=username)

@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    # Top up cash 
    if request.method == "POST":
        cash = request.form.get("cash")
        cash_current = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_current = cash_current[0]["cash"]
        if not cash:
            flash("Amount cannot be empty!", "error")
            return redirect("/cash")
        elif int(cash) < 1:
            flash("Amount must be at least $1", "error")
            return redirect("/cash")
        else:
            # Update the current cash amount 
            cash = int(cash) + cash_current
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
            flash("Cash added succesfully", "success")
            return redirect("/cash")
    else:
        return render_template("cash.html", navbar_style='navbar-alt', navbar_brand_style='navbar-brand-alt', nav_link_style='nav-link-alt')


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

# Logging users out
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    # Get info from the form
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("confirmation")
        checkmail = db.execute("SELECT * FROM users WHERE email = ?", email)
        # Validate the info
        if not name:
            flash("Name cannot be blank", "error")
            return redirect("/register")
        if not email:
            flash("Email cannot be blank", "error")
            return redirect("/register")
        if not password:
            flash("Password cannot be blank", "error")
            return redirect("/register")
        if '@' not in email or email.isnumeric() == True:
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