import requests


#ask user for summoner name, API call to get puuid (hidden account id)
def getSummonerName():
    summonerName = input("Enter your summoner name: ")
    summNameResponse = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + apiKey)
    if(summNameResponse.status_code != 200):
        print("Not a recognized summoner name on the North American Server. Try again.")
        return -1
    else:
        return summNameResponse.json()

#get api key from file
file = open("APIkey.txt", "r")
apiKey = file.read()

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
gameNumber = int(input("How many games ago was the game played that you want to analyze? Enter 0 for most recent game. "))
validGameNumber = False
while(validGameNumber == False):
    try:
        if(gameNumber < 0 or gameNumber > 20):
            gameNumber = int(input("Must be a number between 0 and 19. How many games ago was the game you want to analyze? "))
        else:
            validGameNumber = True
    except Exception:
        gameNumber = int(input("Must be a number between 0 and 19. How many games ago was the game you want to analyze? "))

#get game data
response = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + matchHistoryList[gameNumber] + "/timeline?api_key=" + apiKey)
jsonObj = response.json()

champNames = [""] * 10

#parse through entire json object to get the champions listed in the game
frames = jsonObj["info"]["frames"]
for i in range(len(frames)):
    for j in range(len(frames[i]["events"])):
        if frames[i]["events"][j]["type"] == "CHAMPION_KILL":
            try:
                for k in range(10):
                    tempChamp = frames[i]["events"][j]["victimDamageReceived"][k]["name"]
                    tempNum = frames[i]["events"][j]["victimDamageReceived"][k]["participantId"]
                    if "SRU" in tempChamp:
                        pass
                    else:
                        champNames[tempNum - 1] = tempChamp
            except Exception:
                #do nothing
                pass

#determine all the monster and champion deaths
for i in range(len(frames)):
    for j in range(len(frames[i]["events"])):
        if frames[i]["events"][j].get("monsterType"):
            currentObject = frames[i]["events"][j]
            if frames[i]["events"][j]["monsterType"] == "RIFTHERALD":
                print("Rift Herald found:", (int(currentObject["timestamp"])/60000))
            if frames[i]["events"][j]["monsterType"] == "DRAGON":
                print("Dragon found:", currentObject["monsterSubType"], (int(currentObject["timestamp"])/60000))
            if frames[i]["events"][j]["monsterType"] == "BARON_NASHOR":
                print("Baron found:", (int(currentObject["timestamp"])/60000))
        if frames[i]["events"][j]["type"] == "CHAMPION_KILL":
            print(champNames[frames[i]["events"][j]["victimId"] - 1],"killed",champNames[frames[i]["events"][j]["killerId"] - 1])
            
print(champNames)
            
            #print("Kill found: " + currentObject[-1]["name"] + " killed " + currentObject[-1]["name"], (int(currentObject["timestamp"])/60000))