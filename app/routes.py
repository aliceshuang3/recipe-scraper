from flask import render_template, flash, redirect, request, url_for, jsonify
from app import app, db, mail
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Recipe, Ingredient, CRUD
from werkzeug.urls import url_parse
from app.forms import ResetRequestForm, ResetPasswordForm, FeedbackForm
from app.emails import *
import random
import json
@app.route("/", methods=["GET"])
def index():
    with open('data/Data.json') as json_data:
        jsonData = json.load(json_data)

    for r in jsonData:
        # create Recipe DB object to insert
        # turn instructions arr into 1 string
        instrucs = ""
        for i in r['instructions']:
            instrucs = instrucs + i + " "
        recipe = Recipe(recipe_name=r['name'], recipe_link=r['link'], image_link=r['image'], servings=r['servings'], instructions=instrucs)
        
        CRUD.add(db, recipe)

    data = Recipe.query.all()
    return render_template("home.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('All fields are required.', "warning")
            return render_template('feedback.html', form=form)
        else:
            email_feedback(name=form.name.data,
               subject=form.subject.data,
               sender=form.email.data,
               recipient=app.config['MAIL_USERNAME'],
               feedback_body=form.feedbackBody.data)
        flash('Thank you for your feedback.', "success")
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("feedback.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # check if user is already logged in or not
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # if not a logged in user, create the sign up form
    form = SignUpForm()
    # if valid login, add user data to the database
    if form.validate_on_submit():
        # get username from form filled user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You're now registered. Enjoy our app!", "success")
        # redirect user to login page
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    # value of current_user can be a user object from the database
    # or a special anonymous user object if the user did not log in yet
    # check if user is already logged in or not
    if current_user.is_authenticated:
        return redirect(url_for('searchRecipes'))
    # instantiate form object
    form = LoginForm()
    # if at least one field fails validation, then the function will return False,
    # and that will cause the form to be rendered back to the user
    if form.validate_on_submit():
        # get username from form filled user
        user = User.query.filter_by(username=form.username.data).first()
        # the username can be invalid, or the password can be incorrect for the user
        # takes pw hash stored with the user and determines if pw entered in form matches the hash or not
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "warning")
            # redirect user back to login page
            return redirect(url_for('login'))
        # registers the user as logged in, so that means that any future pages the user
        # navigates to will have the current_user variable set to that user.
        login_user(user, remember=form.remember_me.data)
        # If the user navigates to /index, for ex, @login_required will intercept the request & respond with
        # a redirect to login page, but will add a query string argument to this URL, making the complete
        # redirect URL: /login?next=/index.
        # if user just logged in and was to return to the last page they were on before logging in.
        next_page = request.args.get('next')
        # user had no redirects, bring them to recipe landing page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('searchRecipes')
        # otherwise send them to the page they were last at before logging in
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route("/searchRecipes", methods = ["GET", "POST"])
def searchRecipes():
    # when user enters ingredient to search by, pass to results page
    if request.method == 'POST':
        keyword_search = request.form.get('keyword')
        # when user doesn't input anything
        if keyword_search == "":
            flash("Please enter an ingredient", "info")
            return redirect(url_for('searchRecipes'))
        return redirect(url_for('recipeResults', keyword_search=keyword_search))
    return render_template("searchRecipes.html")

@app.route("/saved")
#@login_required # function is protected and will not allow access to users that aren't authenticated
def savedRecipes():
    # user is logged in, then render their saved recipes
    if current_user.is_authenticated:
        following = current_user.followed_recipes(current_user)
        if len(following) > 0:
            saved = True
            ingredients = []

            for r in following:
                # query for all corresponding ingredients
                ingreds = Ingredient.query.filter_by(recipe_id=r.id).all()

                # add list of ingredients to list of all lists
                if ingreds not in ingredients:
                    ingredients.append(ingreds)

            # form key-value pairs to loop through simultaneously in html
            toReturn = zip(following, ingredients)
            return render_template('savedRecipes.html', user=current_user, toReturn=toReturn, saved=saved)
        else:
            saved = False
            return render_template('savedRecipes.html', saved=saved)
            
    flash("Login or Sign Up to start saving recipes", "info")
    # user isn't logged in yet, render login page
    return redirect(url_for('login'))

@app.route("/results")
def recipeResults():
    # get search term user entered
     keyword_search = request.args.get('keyword_search')

     # find all entries in Ingredient that have the keyword ingredient
     all_matches = Ingredient.query.filter(Ingredient.ingredient_name.contains(keyword_search)).all()
     if len(all_matches) > 0:
         recipes = []
         ingredients = []

         for i in range(len(all_matches)):
             # get corresponding recipe for each ingredient by matching up the recipe id
             r = Recipe.query.filter_by(id=all_matches[i].recipe_id).first()
             # query for all corresponding ingredients
             ingreds = Ingredient.query.filter_by(recipe_id=r.id).all()

             if r not in recipes:
                 # add recipe name to list to return
                 recipes.append(r)
             # add list of ingredients to list of all lists
             if ingreds not in ingredients:
                 ingredients.append(ingreds)

         # form key-value pairs to loop through simultaneously in html
         toReturn = zip(recipes, ingredients)

         return render_template('recipeResults.html', toReturn=toReturn, keyword_search=keyword_search)
     else:
         # no recipes found
         return render_template('no_recipes_error.html')


@app.route("/random")
def randomRecipe():
    # get total number of recipes in DB
    total = len(Recipe.query.all())
    # generate random Recipe number
    recipe_num = random.randint(1, total)
    # query recipe from database, save all details
    recipe = Recipe.query.filter_by(id=recipe_num).first()

    # query for all corresponding ingredients
    ingreds = Ingredient.query.filter_by(recipe_id=recipe_num).all()

    return render_template('randomRecipe.html', recipe=recipe, ingreds=ingreds)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password.", "info")
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid or expired token", "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset. You are now able to log in.", "success")
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/saves', methods=['POST'])
@login_required
def saves():
    if current_user.is_authenticated:
        recipeID = request.form['recipeID']
        action = request.form['action']
        user = current_user
        if recipeID and action:
            recipe = Recipe.query.filter_by(id=int(recipeID)).first_or_404()
            if action == 'saves':
                user.saveRecipe(recipe)
                db.session.commit()
                return jsonify({'status':'OK', 'id':recipeID, 'action':action})
            if action == 'unsaves':
                user.unsaveRecipe(recipe)
                db.session.commit()
                return jsonify({'status':'OK', 'id':recipeID, 'action':action})

"""
@app.cli.command("initdb")
def reset_db():
    # Drops and creates fresh database
    db.drop_all()
    db.create_all()
    print("Initialized default DB")

@app.cli.command("bootstrap")
def bootstrap_data():
    db.drop_all()
    db.create_all()
    db.session.add(
        User(
            username="jacq",
            email="icecreamjackie@gmail.com",
            password_hash="asdjfk123"
        )
    )
    db.session.commit()
    print("added development dataset")
"""
