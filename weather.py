import requests
from bs4 import BeautifulSoup
from functools import lru_cache
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

URL = 'https://meteo.gov.ua'
disable_warnings(InsecureRequestWarning)


class Weather:
    def __init__(self, name, url=URL):
        self.url = self.get_location_link(name, url)
        self.res = {}
        self.build_local_weather()

    @lru_cache(maxsize=256)
    def get_location_link(self, name, url):
        req = requests.get(url, verify=False)
        soup = BeautifulSoup(req.text, 'html.parser')
        for item in soup.findAll("a", {"class": "m13"}):
            if item.text.lower() == name.lower():
                return item.attrs['href']

    def build_local_weather(self):
        if not self.url:
            print('Вказаної локації немає в списку.')
            return
        req = requests.get(self.url, verify=False)
        # TODO: build dictionary with all weather data
        soup = BeautifulSoup(req.text, 'html.parser')
        current_weather = {}
        # Parse current weather
        for item in soup.findAll("div", {"class": "hdr_fr_bl2"})[0].children:
            if hasattr(item, 'text'):
                if not '\n' in item.text:
                    self.res[item.text] = current_weather
                else:
                    data = list(filter(None, item.text.split('\n')))
                    if len(data) == 1:
                        current_weather['Час'] = data[0].split()[1][:5]
                    elif len(data) > 1:
                        if not data[2].split():
                            current_weather['Темп.'] = data[0] + data[1].strip()
                        else:
                            current_weather[data[0]] = ' '.join(data[1:])
        # Parse forecast
        # for item in soup.findAll("table")[0].children:
        #     if item.name == 'tr':
        #         print(1)
        #     pass


if __name__ == '__main__':
    weather = Weather(input('Введіть локацію: '))
    # weather = Weather('львів')
    print(weather.res)
