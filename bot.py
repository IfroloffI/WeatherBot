from telebot import *
from utils.tokens import *
import requests

is_started = False


def get_weather(cords):
    lat, lon = cords
    try:
        headers = {
            'X-Yandex-Weather-Key': get_weather_token()
        }
        request = requests.get("https://api.weather.yandex.ru/v2/forecast?lat=" + str(lat) + "&lon=" + str(lon),
                               headers=headers).json()
        return request["fact"]
    except:
        return "Error"


def get_coords_by_name(name):
    map_token = get_map_token()
    name = '+'.join(name.split())
    response_text = "https://geocode-maps.yandex.ru/1.x/?apikey=" + map_token + "&geocode=" + name + "&format=json"
    request = requests.get(response_text).json()
    try:
        cords = request["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["boundedBy"][
            "Envelope"]
        lower_x, lower_y = map(float, cords["lowerCorner"].split())
        upper_x, upper_y = map(float, cords["upperCorner"].split())
        x, y = (lower_x + upper_x) / 2, (lower_y + upper_y) / 2,
        return (x, y)
    except:
        return "Error"


def run():
    bot = telebot.TeleBot(get_bot_token())

    @bot.message_handler(commands=["start", "go"])
    def start(message):
        global is_started
        is_started = True
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        button_input = types.KeyboardButton(text="Ввести город")

        keyboard.add(button_geo)
        keyboard.add(button_input)

        bot.send_message(message.chat.id, "Поделитесь местоположением", reply_markup=keyboard)

    @bot.message_handler(content_types=['text'])
    def weather_by_adress(message):
        global is_started
        if is_started:
            adress = message.text
            is_started = False
            try:
                lat, lon = get_coords_by_name(adress)
                data = get_weather((lat, lon))
                bot.send_message(message.chat.id, data)
            except:
                bot.send_message(message.chat.id, "Ошибка ввода локации!")

    @bot.message_handler(content_types=['location'])
    def weather_by_location(message):
        global is_started
        is_started = False
        lat, lon = message.location.latitude, message.location.longitude
        data = get_weather((lat, lon))
        bot.send_message(message.chat.id, data)

    bot.polling(none_stop=True, interval=0)
