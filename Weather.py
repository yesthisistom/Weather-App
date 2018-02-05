__author__ = 'tv'

import requests
from dateutil import parser

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
            forecast_hourly = info_request.json()["properties"]["forecastHourly"]

            weather_result = requests.get(forecast_url)
            weather_hourly = requests.get(forecast_hourly)
            if weather_result.status_code == 200:
                hourly_periods = weather_hourly.json()["properties"]["periods"]
                for period in hourly_periods:
                    period["endTime"] = parser.parse(period["endTime"]).strftime("%A %I %p").lstrip("0").replace(" 0", " ")

                return weather_result.json()["properties"]["periods"], hourly_periods
    except:
        print("Exception caught")


if __name__ == "__main__":
    print("Running weather test")
    alexandria_lat = 38.8048
    alexandria_lon = -77.0469

    weather = getWeather(alexandria_lat, alexandria_lon)

    for forecast in weather:
        print(forecast["name"] + ":", forecast["shortForecast"] + ",", str(forecast["temperature"]) + forecast["temperatureUnit"])