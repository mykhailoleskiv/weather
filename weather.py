from functools import lru_cache

import requests
from bs4 import BeautifulSoup
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

URL = "https://meteo.gov.ua"
disable_warnings(InsecureRequestWarning)


class Weather:
    def __init__(self, name, url=URL):
        self.url = self.get_location_link(name, url)
        self.current = {}
        self.forecast = {}
        self.build_local_weather()

    @lru_cache(maxsize=256)
    def get_location_link(self, name, url):
        req = requests.get(url, verify=False)
        soup = BeautifulSoup(req.text, "html.parser")
        for item in soup.findAll("a", {"class": "m13"}):
            if item.text.lower() == name.lower():
                return item.attrs["href"]

    def build_local_weather(self):
        if not self.url:
            return
        req = requests.get(self.url, verify=False)
        soup = BeautifulSoup(req.text, "html.parser")
        current_weather = {}
        # Parse current weather
        for item in soup.findAll("div", {"class": "hdr_fr_bl2"})[0].children:
            if hasattr(item, "text"):
                if "\n" not in item.text:
                    self.current = current_weather
                else:
                    data = list(filter(None, item.text.split("\n")))
                    if len(data) == 1:
                        current_weather["Час"] = data[0].split()[1][:5]
                    elif len(data) > 1:
                        if not data[2].split():
                            current_weather["Темп."] = data[0] + data[1].strip()
                        else:
                            current_weather[data[0]] = " ".join(data[1:])
        # Parse forecast
        table = soup.find_all("tr")

        forecast = {
            "date": table[0].text.split()[1::2],
            "day": table[1].text.split(),
            "clouds": [
                i.contents[1].attrs["title"] for i in list(table[2].children)[3::2]
            ],
            "temp": table[3].text.split()[2:],
            "wind": table[4].text.split()[2:],
            "direction": [
                i.contents[1].attrs["title"] for i in list(table[5].children)[3::2]
            ],
        }

        i = 0
        for date in forecast["date"]:
            self.forecast[date] = {}
            for _ in range(2):
                try:
                    self.forecast[date][forecast["day"][i]] = {
                        "Хмарн.": forecast["clouds"][i],
                        "Темп.": forecast["temp"][i] + "°",
                        "Вітер": forecast["wind"][i] + " м/с",
                        "Напрям": forecast["direction"][i],
                    }
                except IndexError:
                    continue
                i += 1

    def pretty_output(self, weather_type="current"):
        res = ''
        if weather_type == "current":
            for key, value in self.current.items():
                res += f"{key} - {value}\n"
        elif weather_type == "forecast":
            for key, value in self.forecast.items():
                res += f"{key}:\n"
                for k1, v1 in value.items():
                    res += f"\t{k1}:\n"
                    for k2, v2 in v1.items():
                        res += f"\t\t{k2} - {v2}\n"
        return res


if __name__ == "__main__":
    weather = Weather(input("Введіть локацію: "))
    # weather = Weather('львів')
    print(weather.pretty_output(weather_type="current"))
    print(weather.pretty_output(weather_type="forecast"))
