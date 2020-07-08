from app import db, app
from app.models import User, Recipe, Ingredient

import json

import os
os.chdir('/data')
f = open('foobar.txt', 'r')

jsonFiles = [tastyData.json]
for File in jsonFiles:
    # Opening JSON file 
    f = open(File)  
    # returns JSON object as a dictionary 
    data = json.load(f) 
    # Iterating through the json list 
    for recipe in data: 
        recipe_name = recipe.name
        servings = recipe.servings
        instructions = recipe.instructions
        recipe_link = recipe.link
        image_link = recipe.image
        print("Recipe: " + recipe_name + servings + instructions + recipe_link + image_link)
    # Closing file 
    f.close() 
    
# Add recipe data into database
# recipe = Recipe(recipe_name=, servings=, instructions=, recipe_link=, image_link=)


"""
user = User(username=form.username.data, email=form.email.data)
user.set_password(form.password.data)
db.session.add(user)
db.session.commit()
"""