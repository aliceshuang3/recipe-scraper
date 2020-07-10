# Scraper for Tasty website

# imports
from bs4 import BeautifulSoup
import requests
import json

# -----------------------HELPER FUNCTIONS-----------------------------------
# helper function
# scrape relevant details from specific recipe link and save as json object
def getRecipeDetails(response, url, allRecipes):
    content = BeautifulSoup(response.content, "html.parser")

    # scrape recipe name
    name = content.find('h1', attrs={"class": "recipe-name"}).text

    # scrape servings
    servings = content.find('p', attrs={"class": "servings-display"}).text

    # scrape ingredients list
    ingredList = []
    for ingredient in content.findAll('li', attrs={"class": "ingredient"}):
        ingredList.append(ingredient.text)

    # scrape instructions
    instructions = []
    for step in content.findAll('li', attrs={"class": "xs-mb2"}):
        instructions.append(step.text)

    # scrape prep time/cook time (not available for Tasty recipes)

    # "scrape link" - url param

    # scrape image
    img = content.find('meta', attrs={"property": "og:image"}).get("content")

    # convert scraped data to json
    recipeObject = {
        "name": name,
        "servings": servings,
        "ingredients": ingredList,
        "instructions": instructions,
        "link": url,
        "image": img
    }

    allRecipes.append(recipeObject)


# helper function
# find all individual recipes on 1 "page" of the site: before the user has
# to click "Show More" at the bottom to get to the next page of recipes
def getRecipesOnPage(recipe, allRecipes):
    name = recipe['name'].strip()
    converted_name = name.lower().replace(" ", "-")

    # check if single recipe or compilation
    if recipe['content_type'] == "recipe":
        # single recipe - make GET request to that recipe's url, call function
        # to scrape its page
        test_link = 'https://tasty.co/recipe/' + converted_name
        try:
            response = requests.get(test_link, timeout=10)
        except requests.exceptions.Timeout:
            print("Timeout occurred")
        if response.ok:
            getRecipeDetails(response, test_link, allRecipes)
    # UPDATE: don't look through compilations because recipes are listed
    # individually too (results in duplicates!!)
    
    # else:
    #     # recipe compilation
    #     test_link = 'https://tasty.co/compilation/' + converted_name
    #     try:
    #         response = requests.get(test_link, timeout=10)
    #     except requests.exceptions.Timeout:
    #         print("Timeout occurred")
    #     if response.ok:
    #         # get all the individual recipes on the compilation page
    #         content = BeautifulSoup(response.content, "html.parser")
    #         feed = content.findAll('a', attrs={"class": "feed-item"})
    #         # for each recipe, make GET request to that recipe's url, call function
    #         # to scrape its page
    #         for item in feed:
    #             test_link = item.get("href")
    #             try:
    #                 response = requests.get(test_link, timeout=10)
    #             except requests.exceptions.Timeout:
    #                 print("Timeout occurred")
    #
    #             if response.ok:
    #                 getRecipeDetails(response, test_link, allRecipes)


# helper function
# go to a submenu link under Recipes on Tasty's homepage
# get all recipes under that category, iterating through all pages using GET requests
def getSubmenuRecipes(submenu, allRecipes):
    # first page
    url = 'https://tasty.co' + '/api/recipes/search?from=0&in_unit=true&position_offset=1&size=20&tag_names=' + submenu + '&primary_terms='
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        print("Timeout occurred")

    # makes response readable json - returns 3 things: items (recipes), page (current page #), next (url of next page)
    all_json = response.json()
    # go through each item on page, call function to figure out if they are
    # individual recipes or compilations
    for recipe in all_json["items"]:
        getRecipesOnPage(recipe, allRecipes)
    # subsequent pages - continue as long as their is a next page (not None)
    # keep making GET requests and parsing the json returned
    while all_json["next"]:
        url = 'https://tasty.co' + all_json["next"]
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.Timeout:
            print("Timeout occurred")

        all_json = response.json()
        for recipe in all_json["items"]:
            getRecipesOnPage(recipe, allRecipes)


# ------------------MAIN PROGRAM---------------------------------------------
# init list for all json objects for all recipes
allRecipes = []
# scrape each submenu under Recipes on Tasty's homepage
# scrape "easy" recipes to fit our app theme
getSubmenuRecipes("no_bake_desserts", allRecipes)
getSubmenuRecipes("5_ingredients_or_less", allRecipes)
getSubmenuRecipes("meal_prep", allRecipes)

# save data in json file at the end after all recipes are scraped
with open('tastyData.json', 'w', encoding='utf-8') as outfile:
    json.dump(allRecipes, outfile, ensure_ascii=False, indent=4)
