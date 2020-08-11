import os
from telebot import types
from bottle import route, run, post
from constants import TOKEN, APP_NAME
from bot import bot


@route("/")
def index():
    try:
        bot.remove_webhook()
    except Exception:
        pass
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
    return "Hello from Heroku!", 200


@post("/" + TOKEN)
def main():
    bot.process_new_updates([types.Update.de_json("message")])
    return "!", 200


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)
