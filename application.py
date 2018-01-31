from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from validate_email import validate_email
import requests
import json
from helpers import *
import smtplib
import random

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart

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

@app.route("/")
@login_required
def index():
    """Show the users personal homepage"""

    # get the preferences from the database
    prefs = db.execute("SELECT pref1, pref2, pref3 FROM users WHERE user_id == :userid", \
                        userid = session['user_id'])

    preflist = []

    # get the allergies and diets from the user and store them in a list
    rows = db.execute("SELECT vegetarian, vegan, paleo, high_fiber, high_protein, low_carb, low_fat, \
                                low_sodium, low_sugar, alcohol_free, balanced, glutenfree, dairyfree, eggfree, soyfree, \
                                wheatfree, treenutfree, peanutfree FROM users WHERE user_id == :userid", \
                                userid = session['user_id'])
    for item in rows:
        limitations = [i for i in item.values() if i is not None]

    # get recipes where one of the ingredients in present
    for d in prefs:
        for v in d.values():

            # combine the limitations and the preference in one query
            limitations.append(v)
            query = ' '.join(e for e in limitations)

            # execute the query
            try:
                results = api_query(query, 1000)
            except:
                return render_template("apology.html", text = "Too many query's this minute (5/5)")
            if not results:
                return render_template("apology.html", text = "invalid ingredient(s)")

            for item in results['hits']:
                preflist.append(item)

            # get the preference out of the querylist
            limitations = [i for i in limitations if i != v]

    # get three random recipes
    randomrecipes = []
    for i in range(3):
        rand = random.choice(preflist)
        randomrecipes.append(rand['recipe'])

    return render_template("index.html", recipes = randomrecipes)

@app.route("/changenamepass", methods=["GET", "POST"])
@login_required
def changenamepass():
    """Change a users username and password"""

    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", text = "must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", text = "must provide password")

        # ensure password was repeated
        elif not request.form.get("repeat"):
            return render_template("apology.html", text = "must repeat password")

        # check if passwords are equal
        elif request.form.get("password") != request.form.get("repeat"):
            return render_template("apology.html", text = "passwords must be equal")

        # check if the username is unique
        exist = db.execute("SELECT username FROM users")
        for name in exist:
            if name['username'] == request.form.get("username"):
                return render_template("apology.html", text = "That username is already taken")

        # encrypt the password
        encryptedpassword = pwd_context.hash(request.form.get("password"))

        # update the database
        db.execute("UPDATE users SET username = :username, password = :password WHERE user_id == :userid", \
                    username = request.form.get("username"), password = encryptedpassword, userid = session['user_id'])

        return redirect(url_for("index"))

    else:
        return render_template("changenamepass.html")

@app.route("/changemail", methods=["GET", "POST"])
@login_required
def changemail():
    """Change a users email"""

    if request.method == "POST":

        # check if email was given
        if not request.form.get("email"):
            return render_template("apology.html", text = "Please give an email")

        # check if the email is valid
        Email = request.form.get("email")
        is_valid = validate_email(Email)
        if not is_valid:
            return render_template("apology.html", text = "Please insert a valid e-mail")

        # update the database
        db.execute("UPDATE users SET email = :mail WHERE user_id == :userid", \
                    mail = Email, userid = session['user_id'])

        return redirect(url_for("index"))
    else:
        return render_template("changemail.html")

@app.route("/changepref", methods=["GET", "POST"])
@login_required
def changepref():
    """change a users preferences, diets and allergies"""

    if request.method == "POST":

        # check if the user gave values
        if request.form.get('pref1') and request.form.get('pref1') and request.form.get('pref1'):
            Pref1 = request.form.get('pref1')
            Pref2 = request.form.get('pref2')
            Pref3 = request.form.get('pref3')

            # check if the prefered ingredients are valid
            preflist = [Pref1, Pref2, Pref3]
            for item in preflist:
                if len(item) == 1:
                    return render_template("apology.html", text = "Please insert a valid ingredient")

                try:
                    results = api_query(item)
                except:
                    return render_template("apology.html", text = "Too many query's this minute (5/5)")
                if not results:
                    return render_template("apology.html", text = "invalid ingredient(s)")

                if results != None:
                    continue
                elif results == None:
                    return render_template("apology.html", "There were no recipes found for one of your preferences")

            # insert them into the database
            db.execute("UPDATE users SET pref1 = :pref1, pref2 = :pref2, pref3 = :pref3 \
                        WHERE user_id == :userid", \
                        pref1 = Pref1, pref2 = Pref2, pref3 = Pref3, userid = session['user_id'])

            return redirect(url_for("index"))
        else:
            return render_template("apology.html", text = "Please insert ingredients")
    else:
        return render_template("changepref.html")

@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    """Show favorites the user has added"""

    if request.method == "POST":

        # check if button was pressed
        if request.form['submit']:

            # execute the query
            try:
                results = api_query(request.form.get("submit"))
            except:
                return render_template("apology.html", text = "Too many query's this minute (5/5)")
            if not results:
                return render_template("apology.html", text = "invalid ingredient(s)")

            # check if the recipe is already in favorites
            rows = db.execute("SELECT * FROM favorite WHERE name == :name AND user_id == :userid", \
                                name = results['hits'][0]['recipe']['label'], userid = session['user_id'])

            # insert the values into favorites if they are not in it
            if not rows:
                db.execute("INSERT INTO favorite (name, user_id, image, link) \
                            VALUES (:name, :userid, :image, :link)", \
                            name = results['hits'][0]['recipe']['label'], userid = session['user_id'], \
                            image = results['hits'][0]['recipe']['image'], \
                            link = results['hits'][0]['recipe']['url'])
            else:
                return render_template('apology.html', text = "That recipe is already in your favoriteslist")

            # return to index
            return redirect(url_for("favorites"))

    else:
        # retrieve the values from the database
        values = db.execute("SELECT * FROM favorite WHERE user_id == :userid", userid = session['user_id'])

        # store the values in a dict and give them to favorites.html
        fave_recipes = []
        for recipe in values:
            current_recipe = {}

            current_recipe['name'] = recipe['name']
            current_recipe['image'] = recipe['image']
            current_recipe['link'] = recipe['link']
            fave_recipes.append(current_recipe)
        return render_template("favorites.html", data = fave_recipes)

@app.route("/fave_remove", methods=["GET", "POST"])
@login_required
def fave_remove():
    """Remove a recipe from favorites"""
    if request.method == "POST":

        # ensure button was pressed
        if request.form['submit']:

            # delete the recipe from the table
            db.execute("DELETE FROM favorite WHERE name == :name AND user_id == :userid", \
                        name = request.form.get("submit"), userid = session['user_id'])

            return redirect(url_for("favorites"))

        else:
            return redirect(url_for("favorites"))
    else:
        return redirect(url_for("favorites"))

@app.route("/filter_dish", methods=["GET", "POST"])
@login_required
def filter_dish():
    """Get random dishes with the ingredients the user asked for"""

    if request.method == "POST":

        # put the ingredients the user has pressed in a list for the query
        dish_ingredients = ["chicken", "beef", "pork", "lettuce", "cucumber", "carrot", \
                            "brocolli", "beans", "potatoes"]
        query = [request.form.get(i) for i in dish_ingredients if request.form.get(i) != None]

        # get the diets and allergies from the user and add them to the query
        rows = db.execute("SELECT vegetarian, vegan, paleo, high_fiber, high_protein, low_carb, low_fat, \
                                low_sodium, low_sugar, alcohol_free, balanced, glutenfree, dairyfree, eggfree, soyfree, \
                                wheatfree, treenutfree, peanutfree FROM users WHERE user_id == :userid", \
                                userid = session['user_id'])
        for item in rows:
            limitations = [i for i in item.values() if i is not None]

        query += limitations
        query = ' '.join(e for e in query)

        # execute the query
        try:
            results = api_query(query)
        except:
            return render_template("apology.html", text = "Too many query's this minute (5/5)")
        if not results:
            return render_template("apology.html", text = "invalid ingredient(s)")

        # get the recipes from the searchfunction
        recipes = searchfunction(results)

        return render_template("searched.html", data = recipes)

    else:
        return render_template("filtersearch.html")

@app.route("/filter_dessert", methods=["POST"])
@login_required
def filter_dessert():
    """Get random desserts with the ingredients the user has given"""

    # get the ingredients the user has pressed in a list for the query
    dessert_ingredients = ["vanilla", "choco", "coconut", "apple", "orange", "pineapple"]
    query = [request.form.get(i) for i in dessert_ingredients if request.form.get(i) != None]

    # get the diets and allergies from the user and add them to the query
    rows = db.execute("SELECT vegetarian, vegan, paleo, high_fiber, high_protein, low_carb, low_fat, \
                                low_sodium, low_sugar, alcohol_free, balanced, glutenfree, dairyfree, eggfree, soyfree, \
                                wheatfree, treenutfree, peanutfree FROM users WHERE user_id == :userid", \
                                userid = session['user_id'])
    for item in rows:
        limitations = [i for i in item.values() if i is not None]

    query += limitations
    query = ' '.join(e for e in query)

    # execute the query
    try:
        results = api_query(query)
    except:
        return render_template("apology.html", text = "Too many query's this minute (5/5)")
    if not results:
        return render_template("apology.html", text = "invalid ingredient(s)")

    # get the recipes from the searchfunction
    recipes = searchfunction(results)

    return render_template("searched.html", data = recipes)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return render_template('apology.html', text = "must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):

            return render_template('apology.html', text = "Must provide password!")


        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", \
                            username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            return render_template('apology.html', text = "username does not exists or password is not correct")

        # remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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

@app.route("/mail", methods=["GET", "POST"])
@login_required
def mail():

    if request.method == "POST":
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("MakesRightDiner@gmail.com", "Phisingisstommm")

        msg = request.form.get("msg")
        msg = "".join(['<a href="', msg, '">You might like this reccipe, click here</a>'])
        msg = MIMEText(msg, 'html')
        server.sendmail("MakesRightDiner@gmail.com", request.form.get("EMAILADDRESSTO"), msg.as_string())
        server.quit()
        return render_template("index.html")
    else:
        return render_template("mail.html")

@app.route("/search", methods=["POST"])
def search():
    """Search for a recipe"""

    if request.method == "POST":

        # check if ingredient exists
        if not request.form.get("ingredient"):
            return render_template("apology.html", text = "Please insert an ingredient/recipe")

        query = [request.form.get("ingredient")]

        # if the user searches while logged in, also retrieve their allergies and diets
        if session.get('user_id'):
            rows = db.execute("SELECT vegetarian, vegan, paleo, high_fiber, high_protein, low_carb, low_fat, \
                                low_sodium, low_sugar, alcohol_free, balanced, glutenfree, dairyfree, eggfree, soyfree, \
                                wheatfree, treenutfree, peanutfree FROM users WHERE user_id == :userid", \
                                userid = session['user_id'])
            for item in rows:
                limitations = [i for i in item.values() if i is not None]

            # add them to the query
            limitations.append(request.form.get("ingredient"))
            query = ' '.join(e for e in limitations)

        print(query)
        # execute the query
        try:
            results = api_query(query)
        except:
            return render_template("apology.html", text = "Too many query's this minute (5/5)")
        if not results:
            return render_template("apology.html", text = "invalid ingredient(s)")

        # get the recipes
        recipes = searchfunction(results)

        return render_template("searched.html", data = recipes)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", text = "must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", text = "must provide password")

        # ensure password was repeated
        elif not request.form.get("repeat"):
            return render_template("apology.html", text = "must repeat password")

        # check if passwords are equal
        elif request.form.get("password") != request.form.get("repeat"):
            return render_template("apology.html", text = "passwords must be equal")

        # check if the username is unique
        exist = db.execute("SELECT username FROM users")
        for name in exist:
            if name['username'] == request.form.get("username"):
                return render_template("apology.html", text = "That username is already taken")

        # encrypt the password
        encryptedpassword = pwd_context.hash(request.form.get("password"))

        # sort the diet
        diets = ["vegetarian", "vegan", "paleo", "high_fiber", "high_protein", \
                "low_carb", "low_fat", "low_sodium", "low_sugar", "alcohol_free", "balanced"]
        Diet = {i: request.form.get(i) for i in diets}

        # sort the allergies
        allergies = ["gluten", "dairy", "eggs", "soy", "wheat", "treenuts", "peanuts"]
        allergy = {i: request.form.get(i) for i in allergies}

        # preferences
        Pref1 = request.form.get('pref1')
        Pref2 = request.form.get('pref2')
        Pref3 = request.form.get('pref3')

        # check if the prefered ingredients are valid
        preflist = [Pref1, Pref2, Pref3]
        for item in preflist:
            if len(item) == 1:
                return render_template("apology.html", text = "Please insert a valid ingredient")

            try:
                results = api_query(item)
            except:
                return render_template("apology.html", text = "Too many query's this minute (5/5)")
            if not results:
                return render_template("apology.html", text = "invalid ingredient(s)")

            if results != None:
                continue
            elif results == None:
                return render_template("apology.html", "There were no recipes found for one of your preferences")

        # check if email was given
        if not request.form.get("email"):
            return render_template("apology.html", text = "Please give an email")

        # check if the email is valid
        Email = request.form.get("email")
        is_valid = validate_email(Email)
        if not is_valid:
            return render_template("apology.html", text = "Please insert a valid e-mail")

        # insert everything into the users database
        db.execute("INSERT INTO users (username, password, pref1, pref2, pref3, email, \
                    glutenfree, dairyfree, eggfree, soyfree, wheatfree, treenutfree, peanutfree, \
                    vegetarian, vegan, paleo, high_fiber, high_protein, low_carb, low_fat, \
                    low_sodium, low_sugar, alcohol_free, balanced) \
                    VALUES (:username, :password, :pref1, :pref2, :pref3, :email, \
                    :gluten, :dairy, :eggs, :soy, :wheat, :treenuts, :peanuts, \
                    :vegetarian, :vegan, :paleo, :high_fiber, :high_protein, :low_carb, :low_fat, \
                    :low_sodium, :low_sugar, :alcohol_free, :balanced)", \
                    username = request.form.get("username"), password = encryptedpassword, pref1 = Pref1, \
                    pref2 = Pref2, pref3 = Pref3, email = Email, gluten = allergy['gluten'], dairy = allergy['dairy'], \
                    eggs = allergy['eggs'], soy = allergy['soy'], wheat = allergy['wheat'], \
                    treenuts = allergy['treenuts'], peanuts = allergy['peanuts'], \
                    vegetarian = Diet['vegetarian'], vegan = Diet['vegan'], paleo = Diet['paleo'], \
                    high_fiber = Diet['high_fiber'], high_protein = Diet['high_protein'], low_carb = Diet['low_carb'], \
                    low_fat = Diet['low_fat'], low_sodium = Diet['low_sodium'], low_sugar = Diet['low_sugar'], \
                    alcohol_free = Diet['alcohol_free'], balanced = Diet['balanced'])

        return render_template("login.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
