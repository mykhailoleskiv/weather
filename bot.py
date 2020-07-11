from telebot import TeleBot, types
from constants import TOKEN
from weather import Weather

bot = TeleBot(TOKEN)
weather = None


@bot.message_handler(content_types=['text'])
def get_weather(message):
    global weather
    weather = Weather(message.text.lower())
    bot.send_message(message.chat.id, weather.pretty_output())
    keyboard = types.InlineKeyboardMarkup()
    for date in weather.forecast.keys():
        keyboard.add(types.InlineKeyboardButton(text=date, callback_data=date))
    bot.send_message(message.chat.id, text="Оберіть дату", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global weather
    keyboard = types.InlineKeyboardMarkup()
    if 'День' in call.data or 'Ніч' in call.data:
        data = call.data.split()
        answer = ''
        for key, value in weather.forecast[data[0]][data[1]].items():
            answer += f"{key} - {value}\n"
        bot.send_message(call.message.chat.id, text=answer)
    else:
        for day in weather.forecast[call.data].keys():
            keyboard.add(types.InlineKeyboardButton(text=day, callback_data=call.data + " " + day))
        bot.send_message(call.message.chat.id, text="Оберіть період доби", reply_markup=keyboard)



bot.polling()
