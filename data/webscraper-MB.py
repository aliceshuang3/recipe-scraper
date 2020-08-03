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
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        print("Timeout occurred")

    # check if valid url - response returned status code 200
    if response.ok:
        content = BeautifulSoup(response.content, "html.parser")

        # scrape feed listings on that page
        feed = content.findAll('h3', attrs={"class": "post-summary__title"})
        for item in feed:
            recipes.append(item.text)

# loop through all recipes
allRecipes = []

for food in recipes:
    # get rid of parentheses, punctuation, in title for url
    newRecipe1 = food.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("!", "")

    # form new recipe-specific url
    url = 'https://minimalistbaker.com/' + newRecipe1
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        print("Timeout occurred")

    if response.ok:
        content = BeautifulSoup(response.content, "html.parser")

        # scrape only if page is individual recipe
        # compilation recipes all show up individually in feed anyway
        if content.find('li', attrs={"class": "wprm-recipe-ingredient"}):
            # scrape recipe name
            if content.find('h1', attrs={"class": "entry-title"}):
                name = content.find('h1', attrs={"class": "entry-title"}).text
            else:
                # some pages don't have a title up top?
                name = content.find('h2', attrs={"class": "wprm-recipe-name"}).text

            # scrape servings
            try:
                servings = content.find('span', attrs={"class": "wprm-recipe-servings-with-unit"}).text + "servings"
            except:
                servings = "No servings data"

            # scrape ingredients list
            ingredList = []
            for ingredient in content.findAll('li', attrs={"class": "wprm-recipe-ingredient"}):
                ingredList.append(ingredient.text)

            # scrape instructions
            instructions = []
            for step in content.findAll('div', attrs={"class": "wprm-recipe-instruction-text"}):
                instructions.append(step.text)

            # scrape prep time/cook time?

            # "scrape link" - url above

            # scrape image
            img = content.find('img', attrs={"class": "attachment-thumbnail"}).get("src")

            # convert scraped data to json
            recipeObject = {
                "name": name,
                "servings": servings,
                "ingredients": ingredList,
                "instructions": instructions,
                "link": url,
                "image": img
            }

            # ensure no duplicates
            if recipeObject not in allRecipes:
                allRecipes.append(recipeObject)

# save data in json file after all recipes scraped
with open('MBData.json', 'w', encoding='utf-8') as outfile:
    json.dump(allRecipes, outfile, ensure_ascii=False, indent=4)
