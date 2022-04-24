import json
from flask import Flask, jsonify, request
import GameDataPuller
import converter

app = Flask(__name__)

@app.route('/RIOT_DATA', methods=['POST'])
def query_riot_api():
    data = request.get_json()
    print(data["summoner_name"])
    print(data["game_number"])
    GameDataPuller.run(int(data["game_number"]), data["summoner_name"])
    converter.run()
    f = open("gamedata.json")
    return json.load(f), 200