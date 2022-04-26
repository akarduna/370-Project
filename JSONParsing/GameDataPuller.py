from types import MethodDescriptorType
import requests
from datetime import datetime
import json

#ask user for summoner name, API call to get puuid (hidden account id)
def getSummonerName(apiKey, summonerName):
    summNameResponse = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + apiKey)
    if(summNameResponse.status_code != 200):
        print("Not a recognized summoner name on the North American Server. Try again.")
        return -1
    else:
        return summNameResponse.json()

def run(gameNumber, summonerName):
    #declare constants
    timeInterval = 60000
        
    #get api key from file
    file = open("APIkey.txt", "r")
    apiKey = file.read()
    print(apiKey)
    file.close

    #get summoner name from method
    summonerNameResponse = -1
    while(summonerNameResponse == -1):
        summonerNameResponse = getSummonerName(apiKey=apiKey, summonerName=summonerName)

    #gets summoner puuid (hidden account ID for Riot Games)
    puuid = summonerNameResponse["puuid"]

    #gets last 20 games on the account (max amount allowed by riot)
    matchHistoryRequest = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=20&api_key=" + apiKey)
    if(matchHistoryRequest.status_code != 200):
        print("Error occured when fetching match history, exiting")
        exit()

    matchHistoryList = matchHistoryRequest.json()

    #get user input for what game they want to query
    #gameNumber = int(input("How many games ago was the game played that you want to analyze? Enter 0 for most recent game. Enter '20' if you want to manually enter a game ID. "))
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
    file = open("gamedata.csv", "w")
    file.write("event,p1,p2,gold,timestamp\n")
    #get 'real time stamp' from json. Currently unable to convert this to a useful time stamp.
    realTimeStamp = jsonObj["info"]["frames"][0]["events"][0]["realTimestamp"]
    file.write("timestamp,{realTimeStamp},null,null\n".format(realTimeStamp = realTimeStamp))

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
    for i in range(len(summonerName)):
        if i < 5:
            file.write("bluename,")
        else:  
            file.write("redname,")
        print(summonerName[i] + " is playing " + champNames[i])
        if(i == 5):
            file.write("redteam:")
        file.write(summonerName[i] + "," + champNames[i] + ",null,null\n")
    playerIndex = summonerName.index(summonerNameResponse["name"])
    file.write("focus," + summonerNameResponse["name"] + "," + champNames[playerIndex] + ",null,null\n")


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
                        file.write("obj,riftherald,blue,{currTime:.3f},null\n".format(currTime = currTime))
                    else:
                        file.write("obj,riftherald,red,{currTime:.3f},null\n".format(currTime = currTime))
                if currentObject["monsterType"] == "DRAGON":
                    #print("Dragon found:", currentObject["monsterSubType"], (int(currentObject["timestamp"])/timeInterval))
                    currTime = (int(currentObject["timestamp"])/timeInterval)
                    if currentObject["killerTeamId"] == 100:
                        if 'HEX' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,hextech,blue,{currTime:.3f}\n".format(currTime = currTime))
                        if 'MOU' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,mountain,blue,{currTime:.3f}\n".format(currTime = currTime))
                        if 'WATER' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,ocean,blue,{currTime:.3f}\n".format(currTime = currTime))
                        if 'FIRE' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,infernal,blue,{currTime:.3f}\n".format(currTime = currTime))
                        if 'AIR' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,cloud,blue,{currTime:.3f}\n".format(currTime = currTime))   
                    else:
                        if 'HEX' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,hextech,red,{currTime:.3f}\n".format(currTime = currTime))
                        if 'MOU' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,mountain,red,{currTime:.3f}\n".format(currTime = currTime))
                        if 'WATER' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,ocean,red,{currTime:.3f}\n".format(currTime = currTime))
                        if 'FIRE' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,infernal,red,{currTime:.3f}\n".format(currTime = currTime))
                        if 'AIR' in currentObject["monsterSubType"]:
                            file.write("obj,dragon,cloud,red,{currTime:.3f}\n".format(currTime = currTime)) 
                        
                if currentObject["monsterType"] == "BARON_NASHOR":
                    currTime = (int(currentObject["timestamp"])/timeInterval)
                    if currentObject["killerTeamId"] == 100:
                        file.write("obj,baron,blue,{currTime:.3f},null\n".format(currTime = currTime))
                    else:
                        file.write("obj,baron,red,{currTime:.3f},null\n".format(currTime = currTime))
                    #print("Baron found:", (int(currentObject["timestamp"])/timeInterval))
            if currentObject["type"] == "CHAMPION_KILL":
            #print(champNames[currentObject["killerId"] - 1],"killed",champNames[currentObject["victimId"] - 1] + " at time", currentObject["timestamp"] / timeInterval)
                currTime = (int(currentObject["timestamp"])/timeInterval)
                killGold = currentObject["bounty"]
                file.write("kill," + champNames[currentObject["killerId"] - 1] + "," + champNames[currentObject["victimId"] - 1] + ",{killGold},{currTime:.3f}\n".format(killGold = killGold, currTime = currTime))
    print("Finished. Wrote to file \"gamedata.csv\"")
    file.close
                

if __name__ == '__main__':
    run(0, "plez")