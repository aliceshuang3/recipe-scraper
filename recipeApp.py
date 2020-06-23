from app import app, db

# to run the flask shell command in terminal w/o having to keep importing libraries
from app.models import User, Recipe
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Recipe': Recipe}