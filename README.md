# recipe-scraper

## Files
- **application.py**: main flask app code with routes
- **templates/layout.html**: jinja template for other html files, links bootstrap + stylesheet
- **templates/index.html**: homepage for web app
- **static/styles.css**: main css stylesheet
- *data*: contains all webscraping/parsing scripts
- *tutorial-env*: for setting up virtual environment
- *flask_session, pycache*: for running flask app

## Run Flask App
1. Go to the project directory in terminal
2. Type `export FLASK_APP=application.py` (*tells flask where are app's python code is*)
3. Type `export FLASK_DEBUG=1` (*sets the debugger flag so page will update with changes in code*)
4. `flask run`
5. Paste the url under "debug mode: on" into browser!
6. Make changes to code and refresh page to see it updated 

(to be updated if we add a database element)
