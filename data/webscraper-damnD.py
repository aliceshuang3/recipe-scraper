from bs4 import BeautifulSoup # library to parse opened html
import requests # library to open urls
import json

# master list of all links
recipeLinkList = []
# init master recipe list
recipeArr = []

# helper function to get "soup"
def getSoup(link):
    response = requests.get(link).content
    content = BeautifulSoup(response, "html.parser") # root of the parsed tree of our html page
    return content

def getLinks(content):
    # find all divs with a recipe link
    recipeDivs = content.findAll("div", {"class": "archive-post"})
    # append all links to master recipe links list
    for recipe in recipeDivs:
        recipeLinkList.append(recipe.a["href"])

def mainLoop(link, maxPage):
    tempLink = ""
    page = 1
    while page <= maxPage:
        # create each page's link
        tempLink = link + str(page) + "/"
        content = getSoup(tempLink)
        # grab all links from this page
        getLinks(content)
        # next page
        page += 1

# grab recipe data from each link
def addRecipes():
    for link in recipeLinkList:
        # get content from link
        content = getSoup(link)
        print("link: " + link)

        # get title and image from the same container 
        recipe_container = content.find("div", {"class": "recipe-title"})
        # if recipe info exists, then get recipe data
        if recipe_container != None:
            title = recipe_container.find("h2").text
            image = recipe_container.img["src"]

            # get servings
            recipeYield = content.find("span", {"itemprop": "recipeYield"})
            if recipeYield == None:
                yields = "No servings data"
            else:
                yields = recipeYield.text
                
            # grab ingredients 
            ingredList = []
            for ingredient in content.findAll('li', attrs={"itemprop": "ingredients"}):
                ingredList.append(ingredient.text)

            # get instructions
            # check if container is ordered or unordered list or neither
            instructions_container = content.find("div", {"class": "instructions"}).ol
            if instructions_container == None:
                instructions_container = content.find("div", {"class": "instructions"}).ul
            # init instructions list
            instructions = []
            if instructions_container != None:
                for step in instructions_container.findAll('li'):
                    instructions.append(step.text)
            # no instructions found
            else:
                instructions.append("No instructions data")

            # recipe object
            recipeObject = {
                "name": title,
                "servings": yields,
                "ingredients": ingredList,
                "instructions": instructions,
                "link": link,
                "image": image
            }
            # append recipe to master recipe list
            recipeArr.append(recipeObject) 
    
# -------------------------------------------------------------------------- #

# breakfast (6 page)
mainLoop("https://damndelicious.net/category/breakfast/page/", 6)
# chicken (2 page)
mainLoop("https://damndelicious.net/category/chicken/page/", 2)
# christmas (3 page)
mainLoop("https://damndelicious.net/category/christmas/page/", 3)
# drink (3 page)
mainLoop("https://damndelicious.net/category/drink/page/", 3)
# entree (29 page)
mainLoop("https://damndelicious.net/category/entree/page/", 29)
# freezer-friendly (1 page)
mainLoop("https://damndelicious.net/category/freezer-friendly/page/", 1)
# game-day (3 page)
mainLoop("https://damndelicious.net/category/game-day/page/", 3)
# healthy (1 page)
mainLoop("https://damndelicious.net/category/healthy/page/", 1)
# instant-pot (2 page)
mainLoop("https://damndelicious.net/category/instant-pot/page/", 2)
# meal-prep (2 page)
mainLoop("https://damndelicious.net/category/meal-prep/page/", 2)
# one-pot (3 page)
mainLoop("https://damndelicious.net/category/one-pot/page/", 3)
# salad (3 page)
mainLoop("https://damndelicious.net/category/salad/page/", 3)
# pasta (6 page)
mainLoop("https://damndelicious.net/category/pasta/page/", 6)
# side-dish (5 page)
mainLoop("https://damndelicious.net/category/side-dish/page/", 5)
# soup (5 page)
mainLoop("https://damndelicious.net/category/soup/page/", 5)
# slow-cooker (4 page)
mainLoop("https://damndelicious.net/category/slow-cooker/page/", 4)
# vegetarian (6 page)
mainLoop("https://damndelicious.net/category/vegetarian/page/", 6)
# appetizers (10 pages)
mainLoop("https://damndelicious.net/category/appetizer/page/", 10)
# asian-styled recipes (8 pages)
mainLoop("https://damndelicious.net/category/asian-inspired/page/", 8)
# bread (1 page)
mainLoop("https://damndelicious.net/category/bread/page/", 1)

# add all recipes to the master list
addRecipes()

with open('damnDRecipes.json', 'w') as outfile: json.dump(recipeArr, outfile, ensure_ascii=False, indent=4)  

