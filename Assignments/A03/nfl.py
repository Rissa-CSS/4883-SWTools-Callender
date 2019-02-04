from beautifulscraper import BeautifulScraper
from pprint import pprint
import urllib
import json
import sys
from time import sleep
from random import shuffle

scraper = BeautifulScraper()
"""
f = open("nfl_data.json","w")
with urllib.request.urlopen("http://www.nfl.com/liveupdate/game-center/2012020500/2012020500_gtd.json") as url:
        data = json.loads(url.read().decode())
        f.write(json.dumps(data))
        print(data)
f.close
"""
f = open("nfl_data.json","w")
gameids = []
delays = [.01,.02,.03,.04,.05]
season = ["POST","REG"]
years = [x for x in range(2009,2019)]
weeks = [x for x in range(1,18)]
for seas in season:    
         for year in years:
                
                for week in weeks:
                        if seas == "POST":
                                week=""
                        url = "http://www.nfl.com/schedules/%s/%s%s" % (year,seas,week)
                        page = scraper.go(url)
                        divs = page.find_all('div',{"class":"schedules-list-content"})
                        shuffle(delays)
                        #print(divs)
                        for div in divs:
                                if div['data-gameid'] not in divs:
                                        gameids.append(div['data-gameid'])
for game in gameids:
        urllib.request.urlretrieve("http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json"%(game,game),'nfl/'+game+'.json')

print(len(gameids))
