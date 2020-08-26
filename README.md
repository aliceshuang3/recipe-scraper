# recipe-scraper

<img src="./app/static/logo.png" alt="Novice Chef Logo" width="100"/>

## Table of Contents
[ABOUT](#novice-chef-recipe-search-application)<br>
[MOTIVATION](#motivation)<br>
[TECHNOLOGIES](#technologies)<br>
[FEATURES](#features)<br>
[DEMO](#demo)<br>
[INSTALLATION](#installation)<br>
[FILES](#files)<br>
[FUTURE IMPROVEMENTS](#future-improvements)<br>

## Novice Chef Recipe Search Application
Clean, easy-to-use app for beginner cooks to target their recipe search based on what's already in the fridge. Helping to build more budget-friendly and environment-conscious cooking habits. Users can search a database of 5,000+ recipes from 7 different trusted websites, save recipes to their personal list, and also explore new recipes through the random recipe generator.

Created by **Jacquelyn Chow** and **Alice Huang**, two Swarthmore College students, during the summer of 2020.

#### [Click here to check out the app](http://novicechef.pythonanywhere.com/)

## Motivation
There are so many recipe sites online but no streamlined way to search specifically for ways to use up "eggs" or "lettuce" sitting around in the fridge. We wanted to create an app built specfically for this need, enabling users to search directly for tasty recipes they know are easy to prepare. Hopefully, this tool can also help reduce food waste in the kitchen by making it easy to find uses for leftover ingredients while making home cooking more enjoyable too.

## Technologies
* HTML, CSS, Bootstrap (frontend, styling)
* JavaScript, AJAX (dynamic elements)
* Python, Beautiful Soup (web scraping, loading data into database)
* Flask
* SQLite, SQLAlchemy (database)
* Deployed using PythonAnywhere
* Project Management: Trello

## Features
* **Recipe Search by ingredient** (with autocomplete, searches database recipes' ingredient lists)
* **Recipe Previews** (click each recipe in results for a pop-up preview of ingredients and instructions)
* **Random Recipe Generator** (selects from database of 5,000+ recipes)
* **Recipe Saving/Unsaving** (when user logs into account)
* **Recipe Shuffling** (ensures recipes from different sites are shown to the user)

## Demo
#### [Link to Video](https://youtu.be/E_hDfXbT6j8)

## Installation
1. Go to the project directory in terminal
2. Open a virtual environment:
   `tutorial-env/bin/activate`
3. Download required packages using pip3 or pip: 
   `pip install -r requirements.txt`
4. Change flask to development instead of production:
   `export FLASK_ENV=development`
5. Set to debug mode:
   `export FLASK_DEBUG=1`
6. `flask run`
7. Paste the url into browser!

**Database**<br>
* flask db init (downloaded the db files)<br>
* flask db migrate<br>
* flask db upgrade<br>

## Files
- **app/__init__.py**: initializes all items needed for the flask app
- **app/routes.py**: flask app routes
- **app/models.py**: flask app classes (User, Recipe, etc)
- **app/forms.py**: flask app forms classes (Login, SignUp, etc)
- **app/errors.py**: 404 and 500 error pages
- **app/email.py**: reset email and threading functions
- **templates/layout.html**: jinja template for other html files, links bootstrap + stylesheet
- **templates/index.html**: homepage for web app
- **static/js/script.js**: JavaScript logic for results and random recipes pages
- **static/styles/styles.css**: main css stylesheet
- **data**: contains all webscraping/parsing scripts and scraped json files
- **venv**: for setting up virtual environment
- **flask_session, pycache**: for running flask app

## Future Improvements
* Add more recipes to the database
* Articles/guides (resources section) about being eco-friendly, grocery shopping, etc.
* Ability to choose recipes from a specific site
* Calendar tool to plan out meals/grocery needs

