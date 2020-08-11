import os
from decouple import config

if os.environ.get("APP_LOCATION") == "heroku":
    TOKEN = os.environ["TOKEN"]
    APP_NAME = os.environ["APP_NAME"]
    TOKEN_SLICE = os.environ["TOKEN_SLICE"]
else:
    TOKEN = config("TOKEN", cast=str, default="TOKEN")
    APP_NAME = config("APP_NAME", cast=str, default="APP_NAME")
    TOKEN_SLICE = config("TOKEN_SLICE", cast=str, default="TOKEN_SLICE")
