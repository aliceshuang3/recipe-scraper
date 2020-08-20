# Scraper for Okonomi Kitchen website

# imports
from bs4 import BeautifulSoup
import requests
import json

recipes = []
# go through all 31 pages in recipe index
for i in range(2, 31):
    # update page url
    url = 'https://okonomikitchen.com/category/all-recipes/page/' + str(i)
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        print("Timeout occurred")

    # check if valid url - response returned status code 200
    if response.ok:
        content = BeautifulSoup(response.content, "html.parser")

        # scrape feed listings on that page
        feed = content.findAll('h2', attrs={"class": "entry-title"})
        for item in feed:
            recipes.append(item.text)

# loop through all recipes
allRecipes = []

for food in recipes:
    # get rid of parentheses, punctuation, in title for url
    newRecipe1 = food.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("!", "")

    # form new recipe-specific url
    url = 'https://okonomikitchen.com/' + newRecipe1
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        print("Timeout occurred")

    if response.ok:
        content = BeautifulSoup(response.content, "html.parser")

        # scrape recipe name
        try:
            name = content.find('h1', attrs={"class": "entry-title"}).text
        except:
            name = "No recipe title"

        # scrape servings - splice off last 3 chars
        try:
            servings = content.find('span', attrs={"class": "tasty-recipes-yield"}).text[:-3]
        except:
            try:
                servings = content.find('p', attrs={"class": "ERHead"}).text[7:]
            except:
                servings = "No servings data"

        # scrape ingredients list
        ingredList = []
        try:
            for ingredient in content.find('div', attrs={"class": "tasty-recipes-ingredients"}).findAll('li'):
                ingredList.append(ingredient.text)
        except:
            try:
                for ingredient in content.findAll('li', attrs={"class": "ingredient"}):
                    ingredList.append(ingredient.text)
            except:
                ingredList.append("No ingredients data")

        # scrape instructions
        instructions = []
        try:
            for step in content.find('div', attrs={"class": "tasty-recipes-instructions"}).findAll('li'):
                instructions.append(step.text)
        except:
            try:
                for step in content.findAll('li', attrs={"class": "instruction"}):
                    instructions.append(step.text)
            except:
                instructions.append("No instructions data")

        # scrape image
        try:
            img = content.find('figure', attrs={"class": "wp-block-image"}).find('img').get('src')
        except:
            try:
                img = content.find('div', attrs={"class": "entry-content"}).find('img').get('src')
            except:
                img = "../static/defaultphoto.jpg"

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
        if recipeObject not in allRecipes and (recipeObject["name"] != "No recipe title") and len(recipeObject["ingredients"]) != 0:
            allRecipes.append(recipeObject)

# save data in json file after all recipes scraped
with open('okonomiData.json', 'w', encoding='utf-8') as outfile:
    json.dump(allRecipes, outfile, ensure_ascii=False, indent=4)
