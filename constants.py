from decouple import config

TOKEN = config('TOKEN', cast=str, default='TOKEN')
