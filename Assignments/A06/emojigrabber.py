"""
Course: CMPS 4883
Assignemt: A06
Date: 3/10/19
Github username: Rissa-CSS
Repo url: https://github.com/Rissa-CSS/4883-SWTools-Callender/tree/master/Assignments/A06
Name: Clorissa Callender
Description: 
    To scrape the emoji website and save all the emojis.

"""
"""
Imports necessary python libraries needed including beautiful scraper
"""
from beautifulscraper import BeautifulScraper
import urllib
import sys
#Initialises the scraper
scraper = BeautifulScraper()

#Initalise a list for the all of emoji names
allEmojis = []

#Creates the URL
url ="https://www.webfx.com/tools/emoji-cheat-sheet/"

#Goes the the URL
page = scraper.go(url)

#Gets all the span tags with the emoji paths from the website and puts it in a list
emojis = page.find_all("span",{"class":"emoji"})

#Loops through the list of span tags obtained from the website
for emoji in emojis:
    #Adds the emoji paths to the list
    allEmojis.append(emoji['data-src'])


# Loops through the list of emoji paths and gets the  emojis from each URL and saves it to a file
for emo in allEmojis:
    #Gets the emojis and saves them 
    urllib.request.urlretrieve(url+emo, 'emojis/'+(emo.split('/'))[2])
