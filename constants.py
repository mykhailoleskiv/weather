import os
from decouple import config

if os.environ.get('APP_LOCATION') == 'heroku':
    TOKEN = os.environ['TOKEN']
    APP_NAME = os.environ['APP_NAME']
else:
    TOKEN = config('TOKEN', cast=str, default='TOKEN')
    APP_NAME = config('APP_NAME', cast=str, default='APP_NAME')
