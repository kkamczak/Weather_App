import requests
import pandas as pd
import random
import time
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from settings import HOUR_MIN, HOUR_MAX, CITIES


def message_box(msg: str, info: str = None) -> None:
    if info != None:
        text = f'{msg}\n--message: "{info}"'
    else:
        text = msg
    message = QMessageBox()
    message.setText(text)
    message.exec_()

def get_api_key() -> str:
    try:
        with open('api.txt') as f:
            api = f.readline()
        return api
    except FileNotFoundError:
        return ''

def save_api_key(new_key: str) -> None:
    with open('api.txt', 'w') as f:
        f.write(new_key)

def check_for_api_file() -> bool:
    path = 'api.txt'
    if os.path.exists(path):
        if os.path.getsize(path) != 0:
            return True
        else:
            return False
    else:
        return False

def save_day_to_file(weather: dict, forecast: dict) -> None:
    if weather == None or forecast == None: return
    data = [weather, forecast]
    name = f"{get_unix_to_datetime(weather['dt'], mode='date')}-{weather['name']}-{weather['sys']['country']}.json"
    with open(f'saves/{name}', 'w') as f:
        json.dump(data, f, indent=4)

def get_image(icon: str, size: tuple) -> QPixmap:
    url=f'https://openweathermap.org/img/wn/{icon}@2x.png'
    image = QImage()
    image.loadFromData(requests.get(url).content)

    return QPixmap(image).scaled(size[0], size[1])

def get_unix_to_datetime(data: int, mode: str = 'full') -> str:
    if mode == 'full': format = '%d.%m.%y - %H:%M'
    elif mode == 'date': format = '%d.%m.%y'
    elif mode == 'short_date': format = '%d.%m'
    elif mode == 'hours': format = '%H'
    elif mode == 'day': format = '%d'
    elif mode == 'time': format = '%H:%M'
    else: raise ValueError('Wrong type of datetime mode...')

    return str(datetime.fromtimestamp(data).strftime(format))

def get_actual_time(timezone: int = 0) -> str:
    return str(datetime.fromtimestamp(get_unix() + timezone).strftime('%H:%M'))

def get_unix_to_time(time: int, timezone: int = 0, actual_time: int = 0) -> str:
    delta = get_unix() + timezone - actual_time
    return str(datetime.fromtimestamp(time + delta).strftime('%H:%M'))

def get_unix_to_full_datetime(data: int) -> str:
    return str(datetime.fromtimestamp(data).strftime('%d.%m.%y - %H:%M'))

def get_utc() -> datetime:
    return datetime.utcnow()

def get_unix() -> int:
    return int(time.mktime(get_utc().timetuple()))

def get_timezone(timezone: int) -> str:
    sign = '+'
    if int(timezone) < 0: sign = ''

    return (f'UTC{sign}{int(timezone / 3600)}.00')

def get_forecast_days(data: dict) -> list:
    data = data['list']
    days = []
    for id, day in enumerate(data):
        day_number = int(get_unix_to_datetime(day['dt'], 'day'))
        hour = int(get_unix_to_datetime(day['dt'], 'hours'))
        days.append((id, day_number, hour))
    new_days_indicators = []
    active_day = days[0]
    for day in days:
        if day[1] == active_day[1]:
            if day[2] > HOUR_MIN and day[2] < HOUR_MAX:
                new_days_indicators.append(day)
        if day[1] > active_day[1]:
            active_day = day
    new_days = []
    for indicator in new_days_indicators:
        for id, day in enumerate(data):
            if indicator[0] == id:
                new_days.append(day)

    return new_days

def get_country_codes() -> pd.core.frame.DataFrame:
    try:
        data = pd.read_html('https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes', encoding="utf8")[0]
    except:
        print('There was problem with loading country codes')
        return
    data = data.droplevel(0, axis=1)
    data.reset_index(drop=True, inplace=True)
    selected_columns = ['Country name[5]', 'Alpha-2 code[5]']
    codes_data = data[selected_columns]
    codes_data.columns = ['Country', 'Code']
    condition = codes_data['Code'].str.len() <= 3
    codes_data = codes_data[condition]
    codes_data.set_index('Code', inplace=True)

    return codes_data

def read_country(code: str, code_list: pd.core.frame.DataFrame) -> str:
    try:
        name = code_list.loc[code, 'Country']
        if len(name) > 10: name = code
    except (KeyError, AttributeError):
        print('Code not found')
        name = code
    return name

def draw_city() -> str:
    return random.choice(CITIES)

def load_stylesheet() -> str:
    with open('style.css', 'r') as f:
        return f.read()
