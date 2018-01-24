from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from validate_email import validate_email
import requests
import json
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# use this code for every query
"""
payload = {'app_id' : 'abec09cd',
            'app_key' : '66cc31dcd04ab364bff95bd62fe527c8',
            'q' : 'chicken'
}

r = requests.get('http://api.edamam.com/search', params=payload)
rdict = json.loads(r.text)
"""

# use this code as an example to get 1 thing out of a recipe
"""
for hit in rdict['hits']:
    print(hit['recipe']['label'])
    """

@app.route("/")
@login_required
def index():

    prefs = db.execute("SELECT pref1, pref2, pref3 FROM users WHERE user_id == :userid", \
                        userid = session['user_id'])
    print(prefs)

    payload = {'app_id' : 'abec09cd',
            'app_key' : '66cc31dcd04ab364bff95bd62fe527c8',
            'q' : 'lettuce'
    }

    r = requests.get('http://api.edamam.com/search', params=payload)
    rdict = json.loads(r.text)

    imglink = []
    for hit in rdict['hits']:
        imglink.append(hit['recipe']['image'])

    print(len(imglink))

    return render_template("index.html", link = imglink)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM user WHERE username = :username", \
                            username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["userid"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/zoek", methods=["GET", "POST"])
@login_required
def zoek():
    """Get recipe zoek."""

    #check if symbol excists
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Please insert an ingredient/recipe")

        payload = {'app_id' : 'abec09cd',
            'app_key' : '66cc31dcd04ab364bff95bd62fe527c8',
            'q' : request.form.get("symbol")
        }

        r = requests.get('http://api.edamam.com/search', params=payload)
        rdict = json.loads(r.text)
        if not rdict:
            return apology("that ingedient is not valid")

        imglink = []
        for hit in rdict['hits']:
            imglink.append(hit['recipe']['image'])

        return render_template("gezocht.html", link = imglink)

    else:

        return render_template("zoek.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password was repeated
        elif not request.form.get("repeat"):
            return apology("must repeat password")

        # check if passwords are equal
        elif request.form.get("password") != request.form.get("repeat"):
            return apology("passwords must be equal")

        # check if the username is unique
        exist = db.execute("SELECT username FROM users")
        for name in exist:
            if name['username'] == request.form.get("username"):
                return apology("That username is already taken")

        # encrypt the password and insert the new user into the database
        encryptedpassword = pwd_context.hash(request.form.get("password"))

        # diet
        diets = ["vegetarian", "vegan", "paleo", "high_fiber", "high_protein", \
                "low_carb", "low_fat", "low_sodium", "low_sugar", "alcohol_free", "balanced"]
        Diet = {i: request.form.get(i) for i in diets}

        # allergies
        allergies = ["gluten", "dairy", "eggs", "soy", "wheat", "fish", "shellfish", "treenuts", "peanuts"]
        allergy = {i: request.form.get(i) for i in allergies}

        # preferences
        Pref1 = request.form.get('pref1')
        Pref2 = request.form.get('pref2')
        Pref3 = request.form.get('pref3')

        preflist = [Pref1, Pref2, Pref3]
        for item in preflist:
            if len(item) == 1:
                return apology("Please insert a valid ingredient")

            payload = {'app_id' : 'abec09cd',
            'app_key' : '66cc31dcd04ab364bff95bd62fe527c8',
            'q' : item
            }

            r = requests.get('http://api.edamam.com/search', params=payload)
            rdict = json.loads(r.text)
            if rdict != None:
                continue
            elif rdict == None:
                return apology("There were no recipes found for one of your preferences")

        Email = request.form.get("email")
        is_valid = validate_email(Email)
        if not is_valid:
            return apology("Please insert a valid e-mail")

        db.execute("INSERT INTO users (username, password, pref1, pref2, pref3, email, \
                    gluten, dairy, eggs, soy, wheat, fish, shellfish, treenuts, peanuts, \
                    vegetarian, vegan, paleo, high_fiber, high_protein, low_carb, low_fat, \
                    low_sodium, low_sugar, alcohol_free, balanced) \
                    VALUES (:username, :password, :pref1, :pref2, :pref3, :email, \
                    :gluten, :dairy, :eggs, :soy, :wheat, :fish, :shellfish, :treenuts, :peanuts, \
                    :vegetarian, :vegan, :paleo, :high_fiber, :high_protein, :low_carb, :low_fat, \
                    :low_sodium, :low_sugar, :alcohol_free, :balanced)", \
                    username = request.form.get("username"), password = encryptedpassword, pref1 = Pref1, \
                    pref2 = Pref2, pref3 = Pref3, email = Email, gluten = allergy['gluten'], dairy = allergy['dairy'], \
                    eggs = allergy['eggs'], soy = allergy['soy'], wheat = allergy['wheat'], fish = allergy['fish'], \
                    shellfish = allergy['shellfish'], treenuts = allergy['treenuts'], peanuts = allergy['peanuts'], \
                    vegetarian = Diet['vegetarian'], vegan = Diet['vegan'], paleo = Diet['paleo'], \
                    high_fiber = Diet['high_fiber'], high_protein = Diet['high_protein'], low_carb = Diet['low_carb'], \
                    low_fat = Diet['low_fat'], low_sodium = Diet['low_sodium'], low_sugar = Diet['low_sugar'], \
                    alcohol_free = Diet['alcohol_free'], balanced = Diet['balanced'])

        return render_template("login.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
