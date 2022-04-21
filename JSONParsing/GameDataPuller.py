from types import MethodDescriptorType
import requests
from datetime import datetime
import json

#ask user for summoner name, API call to get puuid (hidden account id)
def getSummonerName():
    summonerName = input("Enter your summoner name: ")
    summNameResponse = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + apiKey)
    if(summNameResponse.status_code != 200):
        print("Not a recognized summoner name on the North American Server. Try again.")
        return -1
    else:
        return summNameResponse.json()

#declare constants
timeInterval = 60000
    
#get api key from file
file = open("APIkey.txt", "r")
apiKey = file.read()
file.close

#get summoner name from method
summonerNameResponse = -1
while(summonerNameResponse == -1):
    summonerNameResponse = getSummonerName()

#gets summoner puuid (hidden account ID for Riot Games)
puuid = summonerNameResponse["puuid"]

#gets last 20 games on the account (max amount allowed by riot)
matchHistoryRequest = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=20&api_key=" + apiKey)
if(matchHistoryRequest.status_code != 200):
    print("Error occured when fetching match history, exiting")
    exit()

matchHistoryList = matchHistoryRequest.json()

#get user input for what game they want to query
gameNumber = int(input("How many games ago was the game played that you want to analyze? Enter 0 for most recent game. Enter '20' if you want to manually enter a game ID. "))
matchID = ""
manualIDFlag = False

validGameNumber = False
while(validGameNumber == False):
    try:
        if(gameNumber < 0 or gameNumber > 20):
            gameNumber = int(input("Must be a number between 0 and 19. How many games ago was the game you want to analyze? "))
        if(gameNumber == 20):
            matchID = input("Enter game ID. Starts with \"NA1\": ")
            manualIDFlag = True
        else:
            validGameNumber = True
    except Exception:
        gameNumber = int(input("Must be a number between 0 and 19. How many games ago was the game you want to analyze? "))

#get game data
if(manualIDFlag == False):
    response = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + matchHistoryList[gameNumber] + "/timeline?api_key=" + apiKey)
else:
    response = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + matchID + "/timeline?api_key=" + apiKey)

if(response.status_code != 200):
    print("Error in fetching match. Exiting.")
    exit()


jsonObj = response.json()

summonerPuuid = [""] * 10
summonerName = [""] * 10
champNames = [""] * 10

#open and begin writing to a file
file = open("gamedata.txt", "w")

#get 'real time stamp' from json. Currently unable to convert this to a useful time stamp.
realTimeStamp = jsonObj["info"]["frames"][0]["events"][0]["realTimestamp"]
file.write("timestamp:{realTimeStamp},".format(realTimeStamp = realTimeStamp))

print("Finding all summoner names in the game.")
#parse through json object metadata to get summoner puuid's from the game
participants = jsonObj["metadata"]["participants"]
for i in range(len(participants)):
    summonerPuuid[i] = participants[i]

for i in range(len(summonerPuuid)):
    response = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + summonerPuuid[i] + "?api_key=" + apiKey)
    summonerName[i] = response.json()["name"]

print("Finding all champions in the game.")
#parse through entire json object to get the champions listed in the game

frames = jsonObj["info"]["frames"]
for i in range(len(frames)):
    for j in range(len(frames[i]["events"])):
        currentFrame = frames[i]["events"][j]

        if currentFrame["type"] == "CHAMPION_KILL":
            try:
                for k in range(10):
                    championDeathFrame = frames[i]["events"][j]["victimDamageReceived"][k]

                    tempChamp = championDeathFrame["name"]
                    tempNum = championDeathFrame["participantId"]
                    if "SRU" in tempChamp: #This means if a minion or non-champion did the final killing blow
                        pass
                    else:
                        champNames[tempNum - 1] = tempChamp
            except Exception:
                #do nothing
                pass
file.write("blueteam:")
for i in range(len(summonerName)):
    print(summonerName[i] + " is playing " + champNames[i])
    if(i == 5):
        file.write("redteam:")
    file.write(summonerName[i] + "-" + champNames[i] + ",")
playerIndex = summonerName.index(summonerNameResponse["name"])
file.write("focus:" + summonerNameResponse["name"] + "-" + champNames[playerIndex] + ",")


print("Finding all objective and champion kills.")
#determine all the monster and champion deaths
for i in range(len(frames)):
    for j in range(len(frames[i]["events"])):
        currentObject = frames[i]["events"][j]
        if currentObject.get("monsterType"):
            if currentObject["monsterType"] == "RIFTHERALD":
                #print("Rift Herald found:", (int(currentObject["timestamp"])/timeInterval))
                currTime = (int(currentObject["timestamp"])/timeInterval)
                if currentObject["killerTeamId"] == 100:
                    file.write("obj-riftherald-blue-{currTime:.3f},".format(currTime = currTime))
                else:
                    file.write("obj-riftherald-red-{currTime:.3f},".format(currTime = currTime))
            if currentObject["monsterType"] == "DRAGON":
                #print("Dragon found:", currentObject["monsterSubType"], (int(currentObject["timestamp"])/timeInterval))
                currTime = (int(currentObject["timestamp"])/timeInterval)
                if currentObject["killerTeamId"] == 100:
                    file.write("obj-dragon-" + currentObject["monsterSubType"] + "-blue-{currTime:.3f},".format(currTime = currTime))
                else:
                    file.write("obj-dragon-" + currentObject["monsterSubType"] + "-red-{currTime:.3f},".format(currTime = currTime))
            if currentObject["monsterType"] == "BARON_NASHOR":
                currTime = (int(currentObject["timestamp"])/timeInterval)
                if currentObject["killerTeamId"] == 100:
                    file.write("obj-baron-blue-{currTime:.3f},".format(currTime = currTime))
                else:
                    file.write("obj-baron-red-{currTime:.3f},".format(currTime = currTime))
                #print("Baron found:", (int(currentObject["timestamp"])/timeInterval))
        if currentObject["type"] == "CHAMPION_KILL":
           #print(champNames[currentObject["killerId"] - 1],"killed",champNames[currentObject["victimId"] - 1] + " at time", currentObject["timestamp"] / timeInterval)
            currTime = (int(currentObject["timestamp"])/timeInterval)
            killGold = currentObject["bounty"]
            file.write("kill-" + champNames[currentObject["killerId"] - 1] + "-" + champNames[currentObject["victimId"] - 1] + "-{killGold}-{currTime:.3f},".format(killGold = killGold, currTime = currTime))
print("Finished. Wrote to file \"gamedata.txt\"")
file.close
            
            