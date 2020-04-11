import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import compare_list, apology
import operator


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hstudents.db")

@app.route("/", methods=["GET", "POST"])
def index():
    # saves the user's major and number of classes to session, then redirects user to a page where they input their course titles
    if request.method == "POST":
        session["major"] = request.form.get("major")
        print(session["major"])
        session["number"] = int(request.form.get("number"))
        return redirect("/classes")
    # queries the user for their major and number of courses
    else:
        majorlist = db.execute("SELECT DISTINCT major FROM hstudents ORDER BY major")
        return render_template("index.html", majorlist=majorlist)

@app.route("/classes", methods=["GET", "POST"])
def classes():
    # makes a list of the classes the user has taken
    if request.method == "POST":
        classes = []
        for n in range(1, int(session["number"])+1):
            classes.append(request.form.get(f"subject{n}"))

        # compiles list from hstudents.db of id's of students that share the same major
        id = db.execute("SELECT DISTINCT id FROM hstudents WHERE major = ?", session["major"])
        peopleid = []
        for row in id:
            peopleid.append(row["id"])

        # makes dictionary with id's as keys and lists of classes taken as values
        # also makes dictionary of jaccard index values as keys and person id's as values
        taken = {}
        j_values = {}
        j_value = 0
        for personid in peopleid:
            thispersonclass=db.execute("SELECT title FROM hstudents WHERE id = ?", personid)
            classlist= []
            for row in thispersonclass:
                classlist.append(row["title"])
            taken[personid] = classlist

            j = compare_list(classlist, classes)
            if j in j_values:
                j_values[j].append(personid)
            else:
                j_values[j] = [personid]
            if j > j_value:
                j_value = j

        # if there is no match to the user's classes, then return them to index
        if j_value == 0:
            flash("Sorry, we couldn't find a match in our database. Please try again.")
            return redirect("/")

        # stores highest 10 jaccard values in list
        # stores person id's with the highest jaccard values in another list
        highest_id = []
        another_highlist = []
        for key in sorted(j_values.keys())[-10:]:
            highest_id += j_values[key]
            if key == j_value:
                another_highlist += (j_values[key])

        # find frequencies of other classes that people who also took the same classes as the user took
        # master is an exhaustive list of all classes people who declared the same concentration as user took
        master = []
        for person in highest_id:
            master += taken[person]
        master = set(master)
        # counts is a dictionary with each unique class in the master list as keys and the number of people who took each class as values
        counts = {}
        for person in highest_id:
            for commonclass in master:
                if (commonclass not in classes) and (commonclass in taken[person]):
                    if commonclass in counts:
                        counts[commonclass] += 1
                    else:
                        counts[commonclass] = 1
        # find frequency of each class
        for c in counts:
            counts[c] = counts[c] / len(highest_id)

        # sort by most frequent classes and get top 10 for recommendation to user
        sorted_counts = sorted(counts.items(), key=operator.itemgetter(1))
        recommendation=[]
        for lines in sorted_counts[-10:]:
            recommendation.append(lines[0])

        # for the people who have the highest jaccard value, save their class profile(s) to another list to show to the user
        profiles = []
        for p in another_highlist:
            profiles.append(taken[p])

        # display results!
        return render_template("results.html", profiles=profiles, recommendation=recommendation, length=len(profiles))

    else:
        titles = db.execute("SELECT DISTINCT title FROM hstudents ORDER BY title")
        return render_template("classes.html", titles=titles, number=int(session["number"]))

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
