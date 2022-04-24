from flask import Flask, jsonify, request
import GameDataPuller

app = Flask(__name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]


@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
  incomes.append(request.get_json())
  return '', 204

@app.route('/RIOT_DATA', methods=['POST'])
def query_riot_api():
    json = request.get_json()
    print(json["summoner_name"])
    print(json["game_number"])
    GameDataPuller.run(int(json["game_number"]), json["summoner_name"])
    return " ", 200