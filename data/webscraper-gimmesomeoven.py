from bs4 import BeautifulSoup # library to parse opened html
import requests # library to open urls
import json

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"}
# master list of all links
recipeLinkList = []
# init master recipe list
recipeArr = []

# helper function to get "soup"
def getSoup(link):
    response = requests.get(link, headers=headers).content
    content = BeautifulSoup(response, "html.parser") # root of the parsed tree of our html page
    return content

def getLinks(content):
    # find all divs with a recipe link
    recipeDivs = content.findAll("div", {"class": "teaser-post-sm"})
    # append all links to master recipe links list
    for recipe in recipeDivs:
        recipeLinkList.append(recipe.a["href"])

def mainLoop(link, maxPage):
    tempLink = ""
    page = 1
    while page <= maxPage:
        # create each page's link
        tempLink = link + str(page)
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
        content_container = content.find("h1", {"class": "posttitle"})
        # get title 
        title = content_container.text
        
        # get image
        image = content.find("img", {"class": "size-full"})
        if image == None:
            image = ""
        else:
            image = image["src"]

        # get servings
        recipeYield = content.find("span", {"class": "tasty-recipes-yield"})
        if recipeYield == None:
            yields = "No servings data"
        else:
            yields = recipeYield.text
            
        # grab ingredients 
        ingredList = []
        if content.find("div", {"class": "tasty-recipes-ingredients"}) != None:
            ingredient_container = content.find("div", {"class": "tasty-recipes-ingredients"}).ul
            if ingredient_container != None:
                for ingredient in ingredient_container.findAll('li'):
                    ingredList.append(ingredient.text)
            else:
                ingredient_container = content.find("div", {"class": "tasty-recipes-ingredients"}).p
                ingredList = ingredient_container.text.split("\n")

            # if there are instructions
            if content.find("div", {"class": "tasty-recipes-instructions"}) != None:
            # check if container is ordered or unordered list or neither
                instructions_container = content.find("div", {"class": "tasty-recipes-instructions"}).ol
                if instructions_container == None:
                    instructions_container = content.find("div", {"class": "tasty-recipes-instructions"}).ul
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
                # ensure no duplicates
                if recipeObject not in recipeArr:
                    # append recipe to master recipe list
                    recipeArr.append(recipeObject)
    
# -------------------------------------------------------------------------- #

# test cases
# recipeLinkList = ["https://www.gimmesomeoven.com/rice-krispie-treats/"]
# recipeLinkList = ["https://www.gimmesomeoven.com/how-to-cook-chicken-steak-pork-fish-shrimp-and-tofu-in-the-oven/"]
# recipeLinkList = ["https://www.gimmesomeoven.com/apple-cider-baked-chicken/"]

# gimmesomeoven (141 page)
mainLoop("https://www.gimmesomeoven.com/all-recipes/?fwp_paged=", 141)

# add all recipes to the master list
addRecipes()

with open('gimmesomeovenRecipes.json', 'w') as outfile: json.dump(recipeArr, outfile, ensure_ascii=False, indent=4)  

