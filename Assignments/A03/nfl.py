"""
Course: CMPS 4883
Assignemt: A03
Date: 2/04/19
Github username: Rissa-CSS
Repo url: https://github.com/Rissa-CSS/4883-SWTools-Callender/tree/master/Assignments/A03
Name: Clorissa Callender
Description: 
    To scrape data from the NFL website and get the game data from the
    live update website.

"""
"""
Imports necessary python libraries needed including beautiful scraper
"""
from beautifulscraper import BeautifulScraper
from pprint import pprint
import urllib
import json
import sys
from time import sleep
from random import shuffle

#Initialises the scraper
scraper = BeautifulScraper()

#Opens a file to dumb the IDs
f = open("nfl_data.json","w")

#Initalise a list for the gameids, seasons, years and weeks
gameids = []
delays = [1,2,.03,.04,.05]
season = ["POST","REG"]
years = [x for x in range(2009,2019)]
weeks = [x for x in range(1,17)]

# Loops through for all of the years from 2009 - 2019
for year in years:

        #Initialises a list for the urls
        urls =[]
        #Loops through the seasons
        for sea in season:
                #Checks if the season is POST
                if sea == "POST":
                        #Creates the URL
                        url ="http://www.nfl.com/schedules/%s/%s" % (year,sea)
                        #Goes the the URL
                        page = scraper.go(url)
                        #Gets all the div tags with the values from the website and puts it in a list
                        divs = page.find_all('div',{"class":"schedules-list-content"})
                        #Provides a delay in scraping
                        shuffle(delays)
                        #Loops through the list of div tags btained from the website
                        for div in divs:
                                #Adds the gameIDs to the list
                                gameids.append(div['data-gameid'])
                #Checks to see if it is REG season
                else:
                        #Loop through for the number of weeks in a season
                        for week in weeks:
                                #Creates the URL
                                url = "http://www.nfl.com/schedules/%s/%s%s" % (year,sea,week)
                                #Goes the the URL
                                page = scraper.go(url)
                                #Gets all the div tags with the values from the website and puts it in a list
                                divs = page.find_all('div',{"class":"schedules-list-content"})
                                #Loops through the list of div tags btained from the websiteshuffle(delays)
                                for div in divs:
                                        #Adds the gameIDs to the list
                                        gameids.append(div['data-gameid'])


"""
# Loops through the list of gameids and gets the data from each URL and saves it to a file
for game in gameids:
        url ="http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json"%(game,game)
        urllib.request.urlretrieve(url,'nfl/'+game+'.json')
    
"""



#Outputs list to a file
f.write(json.dumps(gameids))
