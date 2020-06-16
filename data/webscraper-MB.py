# Scraper for Minimalist Baker website

# imports
from bs4 import BeautifulSoup
import requests
import json

recipes = []
# go through all 63 pages in recipe index
for i in range(1, 64):
    # update page url
    url = 'https://minimalistbaker.com/recipe-index/?fwp_paged=' + str(i)
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    # scrape feed listings
    feed = content.findAll('h3', attrs={"class": "post-summary__title"})
    for item in feed:
        if "Matcha" in item.text:
            recipes.append(item.text)

print(recipes)

# loop through all matcha recipes on feed
allRecipes = []

for food in recipes:
    recipe1 = food
    # get rid of parentheses, punctuation, in title for url
    newRecipe1 = recipe1.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("!", "")

    # form new recipe-specific url
    url = 'https://minimalistbaker.com/' + newRecipe1
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    # scrape only if page is individual recipe
    if content.find('li', attrs={"class": "wprm-recipe-ingredient"}):
        # scrape recipe name
        name = content.find('h1', attrs={"class": "entry-title"}).text

        # scrape servings
        servings = content.find('span', attrs={"class": "wprm-recipe-servings-with-unit"}).text

        # scrape ingredients list
        ingredList = []
        for ingredient in content.findAll('li', attrs={"class": "wprm-recipe-ingredient"}):
            ingredList.append(ingredient.text)

        # convert scraped data to json
        recipeObject = {
            "name": name,
            "servings": servings,
            "ingredients": ingredList
        }

        print(recipeObject)

        allRecipes.append(recipeObject)

# save data in json file
with open('MBData.json', 'w') as outfile:
    json.dump(allRecipes, outfile)
