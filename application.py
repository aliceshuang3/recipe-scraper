# Alice Huang, March 2020

import os
import requests
import csv
import random
import time
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ON8ZvUZmSegF1n06YBiw", "isbns": "9781632168146"})
print(res.json())


from flask import Flask, session, render_template, request, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["user_id"] = [] # clear the stored user when logging out
    return render_template("index.html")

@app.route("/chart")
def chart():
    return render_template("chart.html")

@app.route("/hello", methods=["POST"])
def hello():
    username = request.form.get("username") # get form values
    password = request.form.get("password")
    # check if username is already in users table in database
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 1:
          return render_template("error.html", message="That username already exists.")
    else:
      # if not in database, add username and password
      db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
              {"username": username, "password": password})
      db.commit()
      return render_template("hello.html", username=username)

@app.route("/login", methods=["POST"])
def hello2():
    username = request.form.get("username")
    password = request.form.get("password")
    session["user_id"] = [] # set up session to store user id
    # get the object with matching username and password from users database
    id = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).fetchone()
    db.commit()
    # check if user entered wrong username/password
    if id is None:
        return render_template("error.html", message="Wrong username or password.")
    else:
        # if correct login info, add user id to session to store
        session["user_id"].append(id.user_id)
        return render_template("hello2.html", username=username, id=id.username)

# helper function, loads live random data using data_gen.py script 
@app.route("/data")
def data():
    dollars = 0
    projected = 1000
    rec = 1000

    fieldnames = ["dollars", "projected", "rec"]


    with open('static/diningDollars2.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    for i in range(20):
        with open('static/diningDollars2.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "dollars": dollars,
                "projected": projected,
                "rec": rec
            }

            csv_writer.writerow(info)
            print(dollars, projected, rec)

            dollars = dollars + random.randint(-100, 50)
            projected = projected + random.randint(-20, 20)
            rec = rec + random.randint(-15, 25)

        time.sleep(1)
    return render_template("chart.html")
