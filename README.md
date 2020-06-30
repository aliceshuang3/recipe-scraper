# recipe-scraper

## Files
- **app/__init__.py**: initializes all items needed for the flask app
- **app/routes.py**: flask app routes
- **app/models.py**: flask app classes (User, Recipe, etc)
- **app/forms.py**: flask app forms classes (Login, SignUp, etc)
- **app/errors.py**: 404 and 500 error pages
- **app/email.py**: reset email and threading functions
- **templates/layout.html**: jinja template for other html files, links bootstrap + stylesheet
- **templates/index.html**: homepage for web app
- **static/styles.css**: main css stylesheet
- *data*: contains all webscraping/parsing scripts
- *venv*: for setting up virtual environment
- *flask_session, pycache*: for running flask app

## Run Flask App
1. Go to the project directory in terminal
  - Open a virtual environment 
    `tutorial-env/bin/activate`
  - Download the following using pip3 or pip: 
    `pip3 install flask`
    `pip3 install flask_session`
    `pip3 install sqlalchemy`
    `pip3 install flask-sqlalchemy`
    `pip3 install flask-wtf`
    `pip3 install flask-migrate --upgrade`
    `pip3 install flask_login`
    `pip3 install email-validator`
    `pip3 install flask-mail`
    `pip3 install pyjwt`
  - Change flask to development instead of production
    `export FLASK_ENV=development`
2. Type `export FLASK_APP=application.py` (*tells flask where are app's python code is*)
3. Type `export FLASK_DEBUG=1` (*sets the debugger flag so page will update with changes in code*)
4. `flask run`
5. Paste the url under "debug mode: on" into browser!
6. Make changes to code and refresh page to see it updated 

(to be updated if we add a database element)
flask db init (downloaded the db files)
flask db migrate
flask db upgrade
