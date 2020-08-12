import os

from flask import Flask, request
from telebot import TeleBot, types

from constants import TOKEN, APP_NAME
from weather import Weather

bot = TeleBot(TOKEN)
weather = None
server = Flask(__name__)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Для отримання інформації відправте боту назву міста. Бот пришле поточну"
        " погоду та на вибір дати для отримання прогнозу",
    )


@bot.message_handler(content_types=["text"])
def get_weather(message):
    global weather
    weather = Weather(message.text.lower())
    keyboard = types.InlineKeyboardMarkup()
    if weather.url:
        bot.send_message(message.chat.id, weather.pretty_output())
    else:
        for location in weather.similar:
            keyboard.add(
                types.InlineKeyboardButton(text=location, callback_data=location)
            )
        bot.send_message(
            message.chat.id,
            "Вказаної локації немає в списку. Можливо ви мали на увазі:",
            reply_markup=keyboard,
        )
        return
    for date in weather.forecast.keys():
        keyboard.add(types.InlineKeyboardButton(text=date, callback_data=date))
    bot.send_message(message.chat.id, text="Оберіть дату", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global weather
    keyboard = types.InlineKeyboardMarkup()
    s = call.data
    if "День" in s or "Ніч" in s:
        data = s.split()
        answer = ""
        for key, value in weather.forecast[data[0]][data[1]].items():
            answer += f"{key} - {value}\n"
        bot.send_message(call.message.chat.id, text=answer)
    elif not any(char.isdigit() for char in s):
        call.message.text = s
        get_weather(call.message)
    else:
        for day in weather.forecast[s].keys():
            keyboard.add(
                types.InlineKeyboardButton(text=day, callback_data=s + " " + day)
            )
        bot.send_message(
            call.message.chat.id, text="Оберіть період доби", reply_markup=keyboard
        )


@server.route("/" + TOKEN, methods=["POST"])
def get_message():
    bot.process_new_updates(
        [types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://" + APP_NAME + ".herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# bot.polling()
