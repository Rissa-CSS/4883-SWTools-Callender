from beautifulscraper import BeautifulScraper
from pprint import pprint
import urllib
import json
import sys
from time import sleep
from random import shuffle

scraper = BeautifulScraper()

f = open("nfl_data.json","w")
"""
with urllib.request.urlopen("http://www.nfl.com/liveupdate/game-center/2012020500/2012020500_gtd.json") as url:
        data = json.loads(url.read().decode())
        f.write(json.dumps(data))
        print(data)
f.close
"""
f = open("nfl_data.json","w")
gameids = []
delays = [1,2,.03,.04,.05]
season = ["POST","REG"]
years = [x for x in range(2009,2011)]
weeks = [x for x in range(1,18)]
gamedata = {}
for year in years:
        urls =[]
        gamedata[year] = {}
        for sea in season:
                if sea == "POST":
                        gamedata[year][sea] = {}
                        url ="http://www.nfl.com/schedules/%s/%s%s" % (year,sea,week)
                        page = scraper.go(url)
                        divs = page.find_all('div',{"class":"schedules-list-content"})
                        shuffle(delays)
                        
                        for div in divs:
                                gameids.append(div['data-gameid'])
                                gamedata[year][sea][div['data-gameid']] = {}

                else:
                        for week in weeks:
                                url = "http://www.nfl.com/schedules/%s/%s%s" % (year,sea,week)
                                page = scraper.go(url)
                                divs = page.find_all('div',{"class":"schedules-list-content"})
                                shuffle(delays)
                        
                                for div in divs:
                                        gameids.append(div['data-gameid'])
                                        gamedata[year][sea][div['data-gameid']] = {}


for game in gameids:
        urllib.request.urlretrieve("http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json"%(game,game),'nfl/'+game+'.json')


f.write(json.dumps(gamedata))
