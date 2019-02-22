"""
Course: CMPS 4883
Assignemt: A03
Date: 2/13/19
Github username: Rissa-CSS
Repo url: https://github.com/Rissa-CSS/4883-SWTools-Callender/tree/master/Assignments/A03
Name: Clorissa Callender
Description: Calculates various stats for nfl players and games but using the files
             obtained from nfl.py
    
"""
#Imports necessary python libraries needed including beautiful scraper
import os,sys
import json

"""
Assumes you have all of your game data in a folder called '/nfl'
and your files are named gameid.json where gameid can be something like 2009102505.json
"""

"""
Returns a list of files in given directory
"""
def getFiles(path):
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        # print path to all subdirectories first.
        # for subdirname in dirnames:
        #     print(os.path.join(dirname, subdirname))

        # print path to all filenames.
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            files.append(os.path.join(dirname, filename))

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
            # don't go into any .git directories.
            dirnames.remove('.git')
    return files

"""
Checks to see if it is json
"""
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

##############################################################
# getLongestFieldGoal(playerInfo)
# This function calculates the longest field goals.
# 
# Params: 
#    playerInfo [dictionary] : This dictionary stores all the players'
#                              information, including a list  of all of their
#                              field goals.
# Returns: 
#    returns a list of player(s) who have gotten the longest field goals
def getLongestFieldGoal (playerInfo):
    # Intialise list to store the players with the longest field goals
    playerLongestField = []
    # Sets the longest field goal to be 0
    maxi =0
    # Loops through the dictionary of player information
    for playerID,playerData in playerInfo.items():
        #Loops through the list of field goals for a player
        for goal in playerData["FieldGoals"]:
           #Checks if any of the player's field goal is greater than the max field goal 
           if goal > maxi:
               #Sets the goal to the max
               maxi = goal
    # Loops through the dictionary of player information
    for playersID,playersData in playerInfo.items():
        # Checks if this player has the longest field goal
        if maxi in playersData["FieldGoals"]:
            #Adds the player to the list of players with the longest field goals
            playerLongestField.append(playersData['Name'])
    
    print("The following players have a field goal of ", maxi," yards:")
    #Returns the list of players with longest field goals
    return playerLongestField


##############################################################
# getgetFieldGoals(playerInfo,typegoal)
# This function calculates the most field goal.
# 
# Params: 
#    playerInfo [dictionary] : This dictionary stores all the players'
#                              information, including a list  of all of their
#                              field goals.
#
#    typegoal [str]: This determines what kind of field goal the user wants to
#                    calculate. Eg Successful Field Goal or Missed Field Goal.
#
# Returns: 
#    returns a list of player(s) who have gotten the most of that type of field goal.
def getFieldGoals (playerInfo, typegoal):
    # Intialise list to store the players with the most field goals
    playerGoals = []
    # Sets the most field goal to be 0
    maxi =0
    # Loops through the dictionary of player information
    for playerID,playerData in playerInfo.items():
        # Checks to see if the length of the list is longer than maxi
        if len(playerData[typegoal])> maxi:
            # Updates maxi to the length of the list
            maxi = len(playerData[typegoal])
    # Loops through the dictionary of player information        
    for playerID,playerData in playerInfo.items():
        #Checks to see if the number of goals is the same the max
       if len(playerData[typegoal]) == maxi:
           #Adds player to the list
           playerGoals.append(playerData['Name'])

    print("The following players have ", typegoal, " ", maxi," goals:")
    #Returns the list of players with most field goals
    return playerGoals


##############################################################
# mostTeamPen(allTeams)
# This function calculates the team with the most penalites.
# 
# Params: 
#    allTeams [dictionary] : This dictionary stores all the teams'
#                            information, including a list  of all of their
#                             penalities and yards.
#   
# Returns: 
#    returns a list of team(s) with the most penalities 

def mostTeamPen(allTeams):
    #Creates a list to store the team(s) with the most penalties
    penTeams= []
    # Sets the most penalties to 0
    maxi = 0
    # Loops through the dictonary of team information
    for team, teamdata in allTeams.items():
        # Checks if the total number of penalities is more than the max
        if sum(teamdata["Penalties"]) > maxi:
            # Updates max
            maxi = sum(teamdata["Penalties"])
    # Loops through the dictonary of team information
    for teams, teamsdata in allTeams.items():
        # Checks if the teams has the most penalities
        if sum(teamsdata["Penalties"]) ==  maxi:
            #Adds to the list of teams with the most penalities
            penTeams.append(teams)

    print("The following teams have ", maxi," penalties:")
    # Returns list of teams that have the most penalities
    return penTeams


 ##############################################################

# mostTeamPenYards(allTeams)
# This function calculates the team with the most penalites.
# 
# Params: 
#    allTeams [dictionary] : This dictionary stores all the teams'
#                            information, including a list  of all of their
#                             penalities and yards.
#   
# Returns: 
#    returns a list of team(s) with the most penalty yards
   
def mostTeamPenYrds(allTeams):
    #Creates a list to store the team(s) with the most penalty yards
    penTeams= []
    # Sets the most penalty yards to 0
    maxi = 0
    # Loops through the dictonary of team information
    for team, teamdata in allTeams.items():
        # Checks if the total number of penalty yards is more than the max
        if sum(teamdata["PenaltyYards"]) > maxi:
            #  Updates max
            maxi = sum(teamdata["PenaltyYards"])
    # Loops through the dictonary of team information
    for teams, teamsdata in allTeams.items():
        # Checks if the teams has the most penalty yards
        if sum(teamsdata["PenaltyYards"]) ==  maxi:
            #Adds to the list of teams with the most penalty yards
            penTeams.append(teams)

    print("The following teams have ", maxi," penalty yeards:")
    # Returns list of teams that have the most penalty yards
    return penTeams

def getMultipleTeams(data):
     pass

##############################################################
# getPlayerMostTeams(playerInfo)
# This function calculates the player(s) who have played for the most teams.
# 
# Params: 
#    playerInfo [dictionary] : This dictionary stores all the players'
#                              information, including a list  of all of their
#                              teams.
#
# Returns: 
#    returns a list of player(s) who have played for the most teams.

def getPlayerMostTeams (playerInfo):
    # Intialise list to store the players with the longest field goals
    playerTeams=[]
    # Sets the most number of teams to be 0
    maxi =0

    # Loops through the dictionary of player information
    for playerID,playerData in playerInfo.items():
        #Checks if any of the player's teams is greater than the max number of teams anyone had palyed for 
        if len(playerData['Teams']) > maxi:
            #Sets the number of teams to the max
            maxi = len(playerData['Teams'])
    # Loops through the dictionary of player information
    for playersID,playersData in playerInfo.items():
        # Checks if this player has the most teams
        if len(playersData['Teams']) == maxi:
            #Adds the player to the list of players with the most teams
            playerTeams.append(playersData['Name'])
    print("The following players have played for ", maxi," team(s).")
    #Returns the list of players with the most teams
    return playerTeams

def getPlayIds(data,gameid,driveid):
    playIDs = []
    if isinstance(data[gameid]['drives'][driveid],dict):
        for playsId,playsData in data[gameid]['drives'][driveid]['plays'].items():
            playIDs.append(playsId)
            print(playIDs)
        return playIDs
    return []
##############################################################
# getRushingLossYards(playerInfo)
# This function calculates most rushing yards loss
# 
# Params: 
#    playerInfo [dictionary] : This dictionary stores all the players'
#                              information, including a list  of all of their
#                              rushing yards.

# Returns: 
#    returns a list of player(s) who have loss te most rushing yards.

def getRushingLossYards(playerInfo):

    RushIDs = {}
    playerRushes =[]
    minrush = 0
    for playerID,playerData in playerInfo.items():
        #print(playerID, playerData)
        if playerID not in RushIDs:
            RushIDs[playerID]=[]
        for yards in playerData["RushingYards"]:
            if yards <0:
                RushIDs[playerID].append(yards)
    for players, playeryards in RushIDs.items():
        if sum(playeryards) < minrush:
            minrush = sum(playeryards)
    for players, playeryards in RushIDs.items():
        if sum(playeryards) == minrush:
            playerRushes.append(playerInfo[players]['Name'])
    return(playerRushes)

##############################################################
# getLossNum(playerInfo,category)
# This function calculates most rushing yards loss or passing yards loss
# 
# Params: 
#    playerInfo [dictionary] : This dictionary stores all the players'
#                              information, including a list  of all of their
#                              passes and rushing yards.
#
#    category [str]: This determines what kind of loss the user wants calculated.
# Returns: 
#    returns a list of player(s) who have gotten the most of that type loss.

def getLossNum(playerInfo,category):
   
    RushIDs = {}
    playerRush =[]
    maxrush = 0
    for playerID,playerData in playerInfo.items():
        #print(playerID, playerData)
        if playerID not in RushIDs:
            RushIDs[playerID]=[]
        for yards in playerData[category]:
            if yards <0:
                RushIDs[playerID].append(yards)
    for players, playeryards in RushIDs.items():
        if len(playeryards) > maxrush:
            maxrush = len(playeryards)
    for players, playeryards in RushIDs.items():
        if len(playeryards) == maxrush:
            playerRush.append(playerInfo[players]['Name'])
    return(playerRush)
"""
Tries to open a file 
"""
def openFileJson(path):
    try:
      f = open(path, "r")
      data = f.read()
      if is_json(data):
          return json.loads(data)
      else:
          print("Error: Not json.")
          return {}
    except IOError:
        print("Error: Game file doesn't exist.")
        return {}

path = '../A03/nfltest'
files = getFiles(path)
#print(files)
files = sorted(files)
allPlayers = {}
tempPlayers ={}
playersdict ={}
allTeams = {}
totalPlays = []
totFieldGoals = []
# loop through files
for file in files:
    
    # read in json data and convert to dictionary
    data = openFileJson(file)
    
    # pull out the game id and game data
    #if isinstance(data,dict):
    # pull out the game id and game data
    
    for gameid,gamedata in data.items():
        if gameid != "nextupdate":
            if gamedata['home']['abbr'] not in allTeams:
                allTeams[gamedata['home']['abbr']] = {}
                allTeams[gamedata['home']['abbr']]["Penalties"] = []
                allTeams[gamedata['home']['abbr']]["PenaltyYards"] = []
            if gamedata['away']['abbr'] not in allTeams:
                allTeams[gamedata['away']['abbr']] = {}
                allTeams[gamedata['away']['abbr']]["Penalties"] = []
                allTeams[gamedata['away']['abbr']]["PenaltyYards"] = []

            allTeams[gamedata['home']['abbr']]["Penalties"].append(gamedata['home']['stats']['team']['pen'])
            allTeams[gamedata['home']['abbr']]["PenaltyYards"].append(gamedata['home']['stats']['team']['penyds'])
            allTeams[gamedata['away']['abbr']]["Penalties"].append(gamedata['away']['stats']['team']['pen'])
            allTeams[gamedata['away']['abbr']]["PenaltyYards"].append(gamedata['away']['stats']['team']['penyds'])
            
            for driveid,drivedata in gamedata['drives'].items():
                if driveid != 'crntdrv':
                    if isinstance(data[gameid]['drives'][driveid],dict):
                        for playsId,playsData in data[gameid]['drives'][driveid]['plays'].items():
                            totalPlays.append(int(playsId))
                            for playerID,playerData in data[gameid]['drives'][driveid]['plays'][playsId]['players'].items():
                                #print(playerID, playerData)
                                if playerID != "0":
                                    if playerID not in playersdict:
                                        playersdict[playerID] = {}
                                        playersdict[playerID]['Teams'] = []
                                        playersdict[playerID]['FieldGoals'] = []
                                        playersdict[playerID]['MissedFieldGoals'] = []
                                        playersdict[playerID]['PassingYards'] = []
                                        playersdict[playerID]['RushingYards'] = []
                                        playersdict[playerID]['Name'] = playerData[0]['playerName']
                                    if playerData[0]['clubcode'] not in playersdict[playerID]['Teams']:
                                        playersdict[playerID]['Teams'].append(playerData[0]['clubcode'])
                             
                                    for play in playerData:
                                        #print(play['statId'] )
                                        if play['statId'] == 69:
                                            #print(play['statId'] )
                                            playersdict[playerID]['MissedFieldGoals'].append(play['yards'])
                                        if play['statId'] == 70:
                                            playersdict[playerID]['FieldGoals'].append(play['yards'])
                                        if play['statId'] == 15:
                                            playersdict[playerID]['PassingYards'].append(play['yards'])
                                        if play['statId'] == 10:
                                            playersdict[playerID]['RushingYards'].append(play['yards'])
                                        
 
print ("Name: Clorissa Callender")
print ("Assignment: A03 - NFL Stats")
print("Date: Wednesday 13th February,2019")
print("============================================================")
print("1) Find the player(s) that played for the most teams.")
print("Answer: ")
for players in getPlayerMostTeams(playersdict):
    print ("Player: ", players)
print("2) Find the player(s) that played for multiple teams in one year.")
print("Answer: ")
print("3) Find the player(s) that had the most yards rushed for a loss.")
print("Answer: ")
print(getRushingLossYards(playersdict))
print("4) Find the player(s) that had the most rushes for a loss.")
print("Answer: ")
print(getLossNum(playersdict,"RushingYards"))
print("5) Find the player(s) with the most number of passes for a loss.")
print("Answer: ")
print(getLossNum(playersdict,"PassingYards"))
print("6) Find the team with the most penalties.")
print("Answer: ")
print(mostTeamPen(allTeams))  
print("7) Find the team with the most yards in penalties.")
print("Answer: ")
print(mostTeamPenYrds(allTeams)) 
print("8) Find the correlation between most penalized teams and games won / lost.")
print("Answer: ")
print("9) Average number of plays in a game.")
print("Answer: ")
print( len(totalPlays)/len(files))
print("10) Longest field goal.")
print("Answer: ")
print(getLongestFieldGoal(playersdict))
print("11) Most field goals.")
print("Answer: ")
print(getFieldGoals(playersdict,'FieldGoals'))
print("12) Most missed field goals.")
print("Answer: ")
print(getFieldGoals(playersdict,'MissedFieldGoals'))
print("13) Most dropped passes (Search for 'pass' and 'dropped' in play description, and stat-id 115).")
print("Answer: ")
