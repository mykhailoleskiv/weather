import requests
from bs4 import BeautifulSoup

URL = 'https://meteo.gov.ua'


class Weather:
    def __init__(self, name, url=URL):
        req = requests.get(url, verify=False)
        soup = BeautifulSoup(req.text)
        for item in soup.findAll("a", {"class": "m13"}):
            if item.text.lower() == name.lower():
                self.url = item.attrs['href']
                self.build_local_weather()

    def build_local_weather(self):
        req = requests.get(self.url, verify=False)
        # TODO: build dictionary with all weather data
        soup = BeautifulSoup(req.text)
        for item in soup.findAll("div", {"class": "hdr_fr_bl2"})[0].children:
            print(item)

# l = Weather('львів')
