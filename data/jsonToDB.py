# --------------script for loading json data into sqlite db---------------------
# run in routes.py
# run both scrips 3x, once per json file, replacing keywords as necessary 

# !!!!!!!!!!!! import json at the top of the file

# load RECIPE data--------------------------------------------------------------
# open scraped json data file and load
  with open('data/tastyData.json') as json_data:
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
  # for i in data:
  #     CRUD.delete(db, i)

# load INGREDIENT data--------------------------------------------------------
# open scraped json data file and load
with open('data/MBData.json') as json_data:
  jsonData = json.load(json_data)

for r in jsonData:
  # get corresponding recipe id from db
  r_id = Recipe.query.filter(Recipe.recipe_link.contains('minimalistbaker')).filter_by(recipe_name=r['name']).first().id
  # get ingredients
  for i in r['ingredients']:
      # make ingredient object to insert
      ingred = Ingredient(recipe_id=r_id, ingredient_name=i)

      CRUD.add(db, ingred)

data = Ingredient.query.all()
# for i in data:
#     CRUD.delete(db, i)
