# Scraper for Tasty website 

# imports
from bs4 import BeautifulSoup
import requests
import json

url = 'https://tasty.co'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

# scrape feed listings
recipes = []
feed = content.findAll('div', attrs={"class": "feed-item__title"})
for item in feed:
    if "Potato" in item.text:
        recipes.append(item.text)

print(recipes)

# loop through all potato recipes on feed
allRecipes = []

for food in recipes:
    recipe1 = food
    newRecipe1 = recipe1.lower().replace(" ", "-")

    # form new recipe-specific url
    url = 'https://tasty.co/recipe/' + newRecipe1
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    # scrape recipe name
    name = content.find('h1', attrs={"class": "recipe-name"}).text

    # scrape servings
    servings = content.find('p', attrs={"class": "servings-display"}).text

    # scrape ingredients list
    ingredList = []
    for ingredient in content.findAll('li', attrs={"class": "ingredient"}):
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
with open('tastyData.json', 'w') as outfile:
    json.dump(allRecipes, outfile)
