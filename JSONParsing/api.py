import json
from flask_cors import CORS
from flask import Flask, jsonify, request
import GameDataPuller
import converter

app = Flask(__name__)
CORS(app)

@app.route('/RIOT_DATA', methods=['POST'])
def query_riot_api():
    content_type = request.headers.get('Content-Type')
    print(content_type)
    data = request.get_json()
    print(data)
    GameDataPuller.run(int(data["game_number"]), data["summoner_name"])
    converter.run()
    f = open("gamedata.json")
    return json.load(f), 200