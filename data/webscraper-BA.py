# Scraper for bonappetit 5 ingredient recipes

# imports
from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.bonappetit.com/gallery/simple-recipes-five-ingredients'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

# scrape feed listings
recipes = []
feed = content.findAll('h2', attrs={"class": "gallery-slide-caption__hed"})

# add all 89 recipes to be saved
for item in feed:
    recipes.append(item.text)

# loop through all recipes on feed - go to each recipe's url
allRecipes = []

for food in recipes:
    recipe1 = food
    newRecipe1 = recipe1.lower().replace(" ", "-")

    # form new recipe-specific url
    url = 'https://www.bonappetit.com/recipe/' + newRecipe1

    # catch out any timeout errors
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        print("Timeout occurred")

    # filter out invalid urls (check if response status code = 200)
    if response.ok:
        content = BeautifulSoup(response.content, "html.parser")

        # scrape recipe name
        name = content.find('a', attrs={"class": "top-anchor"}).text

        # scrape image url
        img = content.find('img', attrs={"class": "ba-picture--fit"}).get("srcset")

        # scrape servings
        servings = content.find('span', attrs={"class": "recipe__header__servings"}).text

        # scrape ingredients list
        # (no separation for quantity and measurement for ingredients on this
        # site, so store it all together in one table)
        ingredList = []
        for ingredient in content.findAll('div', attrs={"class": "ingredients__text"}):
            ingredList.append(ingredient.text)

        # scrape instructions
        instructions = []
        for step in content.findAll('li', attrs={"class": "step"}):
            instructions.append(step.text)

        # "scrape link" - use url variable above

        # (no prep/cook time on this site)

        # convert scraped data to json
        recipeObject = {
            "name": name,
            "servings": servings,
            "ingredients": ingredList,
            "instructions": instructions,
            "link": url,
            "image": img
        }

        # save all json objects
        allRecipes.append(recipeObject)

# save data in json file
with open('data/BAData.json', 'w', encoding='utf-8') as outfile:
    json.dump(allRecipes, outfile, ensure_ascii=False, indent=4) # formats nicely
