import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint


def ShowWeather(in_lat, in_lon):

    dotenv_path = './dotenv.env'
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    url = "https://api.weather.yandex.ru/v2/forecast"

    params = {
        "lat": in_lat,
        "lon": in_lon,
        "extra": "true",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "X-Yandex-API-Key":  os.getenv("API_KEY")
    }

    response = requests.get(url, params=params, headers=headers)
    j_data = response.json()

    with open("weather.json", "w") as f:
        json.dump(j_data, f)

    # pprint(j_data)
    
    print("Погода в : " + j_data["geo_object"]["locality"]["name"])
    # pprint(j_data["forecasts"][4]['parts']['day']['temp_avg'])
    print("Средняя температура: ") 
    print(j_data["forecasts"][4]['parts']['day']['temp_avg'])
    print("Максимальная температура: ")
    print(j_data["forecasts"][4]['parts']['day']['temp_max'])
    print("Минимальная температура: ")
    print(j_data["forecasts"][4]['parts']['day']['temp_min'])
    


def ShowMenu():
    print ('''HELLO, USER, Выбери город, в котором нужно показать погоду:
            \n [1] -- Москва
            \n [2] -- Воронеж
            \n [3] -- Санкт-Петербург
            \n [9] -- Показать выбор команд
            \n [0] -- Выход''')

clear = lambda: os.system ('clear')
clear()

ShowMenu()
while True:
    try:
        print('\n Выберете пунтк меню. [9] -- Показать выбор команд: ')
        enteredNum = int(input())
        if (enteredNum == 1):
            ShowWeather("55.75396", "37.620393")
        elif (enteredNum == 2):
            ShowWeather("51.66078186", "39.20029449")
        elif (enteredNum == 3):
            ShowWeather("59.93867493", "30.31449318")
        elif (enteredNum == 9):
            ShowMenu()
        elif (enteredNum == 0):
            break
        else: 
            print("Нет такого пункта меню. [9] -- Показать выбор команд")
    except:
        print('Некорректный ввод. Попробуйте еще раз! [9] -- Показать выбор команд')






