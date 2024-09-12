import json

def get_bot_token():
    f = open('tokens.json')
    data = json.load(f)
    f.close()
    return str(data["tg-token"])

def get_weather_token():
    f = open('tokens.json')
    data = json.load(f)
    f.close()
    return str(data["weather-token"])

def get_map_token():
    f = open('tokens.json')
    data = json.load(f)
    f.close()
    return str(data["map-token"])