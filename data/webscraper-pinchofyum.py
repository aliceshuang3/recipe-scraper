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
    recipeDivs = content.findAll("article", {"class": "post-summary"})
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
        title = content.find("h2", {"class": "tasty-recipes-title"})
        
        # if recipe info exists, then get recipe data
        if title != None:
            title = title.text
            image = content.find("a", {"class": "first-image-share"}).img
            if image != None:
                image = image["src"]

            # get servings
            recipeYield = content.find("span", {"class": "tasty-recipes-yield"})
            if recipeYield == None:
                yields = "No servings data"
            else:
                yields = recipeYield.text
                
            # grab ingredients 
            ingredList = []
            ingredContent = content.find('div', attrs={"class": "tasty-recipes-ingredients"})
            if ingredContent != None:
                ingredContent = ingredContent.findAll('ul')
                for section in ingredContent:
                    for ingredient in section.findAll('li'):
                        ingredList.append(ingredient.text)

                # get instructions
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
                # append recipe to master recipe list
                recipeArr.append(recipeObject) 
        
# -------------------------------------------------------------------------- #

#  test cases
# recipeLinkList = ["https://pinchofyum.com/coconut-lime-grilled-chicken-and-rice"]

# pinch of yum (65 page)
mainLoop("https://pinchofyum.com/recipes?fwp_paged=", 65)

# add all recipes to the master list
addRecipes()

with open('pinchofyumRecipes.json', 'w') as outfile: json.dump(recipeArr, outfile, ensure_ascii=False, indent=4)  

