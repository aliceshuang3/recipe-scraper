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
for item in feed:
    if "Pasta" in item.text:
        recipes.append(item.text)

print(recipes)

# loop through all potato recipes on feed
allRecipes = []

for food in recipes:
    recipe1 = food
    newRecipe1 = recipe1.lower().replace(" ", "-")

    # form new recipe-specific url
    url = 'https://www.bonappetit.com/recipe/' + newRecipe1
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    # scrape recipe name
    name = content.find('a', attrs={"class": "top-anchor"}).text

    # scrape servings
    servings = content.find('span', attrs={"class": "recipe__header__servings"}).text

    # scrape ingredients list
    ingredList = []
    for ingredient in content.findAll('div', attrs={"class": "ingredients__text"}):
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
with open('BAData.json', 'w') as outfile:
    json.dump(allRecipes, outfile)
