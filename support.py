import requests
import pandas as pd
import json
from datetime import datetime
from PyQt5.QtGui import QPixmap, QImage
from settings import HOUR_MIN, HOUR_MAX


def get_api_key() -> str:
    with open('api.txt') as f:
        api = f.readline()
    return api

def get_image(icon: str, size: tuple) -> QPixmap:
    url=f'https://openweathermap.org/img/wn/{icon}@2x.png'
    image = QImage()
    image.loadFromData(requests.get(url).content)

    return QPixmap(image).scaled(size[0], size[1])

def get_unix_to_time(data: int, timezone: int = 0) -> str:
    return str(datetime.fromtimestamp(data+timezone).strftime('%H:%M'))

def get_unix_to_short_date(data: int) -> str:
    return str(datetime.fromtimestamp(data).strftime('%d.%m'))

def get_unix_to_full_datetime(data: int) -> str:
    return str(datetime.fromtimestamp(data).strftime('%d.%m.%y - %H:%M'))

def get_unix_to_hours(data: int) -> int:
    return int(datetime.fromtimestamp(data).strftime('%H'))

def get_unix_to_day(data: int) -> int:
    return int(datetime.fromtimestamp(data).strftime('%d'))

def get_utc() -> datetime:
    return datetime.utcnow()

def get_timezone(timezone: int) -> str:
    sign = '+'
    if int(timezone) < 0: sign = ''

    return (f'UTC{sign}{int(timezone / 3600)}.00')

def get_forecast_days(data: dict) -> list:
    data = data['list']
    days = []
    for id, day in enumerate(data):
        day_number = get_unix_to_day(day['dt'])
        hour = get_unix_to_hours(day['dt'])
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
    data = pd.read_html('https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes', encoding="utf8")[0]
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
    except KeyError:
        print('Code not found')
        name = code
    return name

