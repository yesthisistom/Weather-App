__author__ = 'tv'

import requests
from pprint import pprint

api_url = "https://api.weather.gov/points/"


def getWeather(latitude,longitude):
    '''

    :param latitude:
    :param longitude:
    :return: list dictionaries of weather
    '''

    global api_url

    info_url = api_url + str(latitude) + "," + str(longitude)

    try:
        info_request = requests.get(info_url)

        if info_request.status_code == 200:
            forecast_url = info_request.json()["properties"]["forecast"]
            forecastHourly = info_request.json()["properties"]["forecast"]

            weather_result = requests.get(forecast_url)
            if weather_result.status_code == 200:
                return weather_result.json()["properties"]["periods"]
    except:
        print("Exception caught")


if __name__ == "__main__":
    print("Running weather test")
    alexandria_lat = 38.8048
    alexandria_lon = -77.0469

    weather = getWeather(alexandria_lat, alexandria_lon)

    for forecast in weather:
        print(forecast["name"] + ":", forecast["shortForecast"] + ",", str(forecast["temperature"]) + forecast["temperatureUnit"])