'''
This is module for support functions
'''
import random
import time
import json
import os
from typing import Optional
from datetime import datetime
import pandas as pd
import requests
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from src.settings import HOUR_MIN, HOUR_MAX, CITIES, TIMEOUT

def message_box(msg: str, info: Optional[str] = None) -> None:
    """
    Display a message box with an optional additional info message.

    Args:
        msg (str): The main message to display.
        info (Optional[str]): Additional information to display.

    Returns:
        None
    """
    if info is not None:
        text = f'{msg}\n--message: "{info}"'
    else:
        text = msg
    message = QMessageBox()
    message.setText(text)
    message.exec_()

def get_api_key() -> str:
    """
    Read the API key from a file.

    Returns:
        str: The API key read from the file.
    """
    try:
        with open('src/api.txt', encoding='utf-8') as file:
            api = file.readline()
        return api
    except FileNotFoundError:
        return ''

def save_api_key(new_key: str) -> None:
    """
    Save an API key to a file.

    Args:
        new_key (str): The new API key to be saved.

    Returns:
        None
    """
    with open('src/api.txt', 'w', encoding='utf-8') as file:
        file.write(new_key)

def check_for_api_file() -> bool:
    """
    Check if the API key file exists.

    Returns:
        bool: True if the file exists and is not empty, False otherwise.
    """
    path = 'src/api.txt'
    if os.path.exists(path):
        if os.path.getsize(path) != 0:
            return True
        return False
    return False

def save_day_to_file(weather: dict, forecast: dict) -> None:
    """
    Save weather and forecast data to a file.

    Args:
        weather (dict): Weather data to be saved.
        forecast (dict): Forecast data to be saved.

    Returns:
        None
    """
    if weather is None or forecast is None:
        return
    data = [weather, forecast]
    name = f"{get_unix_to_datetime(weather['dt'], mode='date')}-" \
           f"{weather['name']}-{weather['sys']['country']}.json"
    with open(f'src/saves/{name}', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def get_image(icon: str, size: tuple[int]) -> QPixmap:
    """
    Get an image from a website and return it as a QPixmap.

    Args:
        icon (str): The icon name.
        size (tuple[int]): The desired size of the image.

    Returns:
        QPixmap: The QPixmap object representing the image.
    """
    url=f'https://openweathermap.org/img/wn/{icon}@2x.png'
    image = QImage()
    image.loadFromData(requests.get(url, timeout=TIMEOUT).content)

    return QPixmap(image).scaled(size[0], size[1])

def get_unix_to_datetime(data: int, mode: str = 'full') -> str:
    """
    Convert a Unix timestamp to a datetime format.

    Args:
        data (int): The Unix timestamp to be converted.
        mode (str): The format mode for the conversion.

    Returns:
        str: The datetime in the specified format.
    """
    if mode == 'full':
        look = '%d.%m.%y - %H:%M'
    elif mode == 'date':
        look = '%d.%m.%y'
    elif mode == 'short_date':
        look = '%d.%m'
    elif mode == 'hours':
        look = '%H'
    elif mode == 'day':
        look = '%d'
    elif mode == 'time':
        look = '%H:%M'
    else:
        raise ValueError('Wrong type of datetime mode...')

    return str(datetime.fromtimestamp(data).strftime(look))

def get_actual_time(timezone: int = 0) -> str:
    """
    Calculate the current time in a location based on the timezone.

    Args:
        timezone (int): The timezone offset.

    Returns:
        str: The current time in HH:MM format.
    """
    return str(datetime.fromtimestamp(get_unix() + timezone).strftime('%H:%M'))

def get_unix_to_time(dt_time: int, timezone: int = 0, actual_time: int = 0) -> str:
    """
    Calculate the time for sunset and sunrise in a location based on the timezone.

    Args:
        dt_time (int): The Unix timestamp for the event.
        timezone (int): The timezone offset.
        actual_time (int): The actual time.

    Returns:
        str: The time of the event in HH:MM format.
    """
    delta = get_unix() + timezone - actual_time
    return str(datetime.fromtimestamp(dt_time + delta).strftime('%H:%M'))

def get_utc() -> datetime:
    """
    Get the current UTC time.

    Returns:
        datetime: The current UTC time.
    """
    return datetime.utcnow()

def get_unix() -> int:
    """
    Get the current Unix timestamp based on UTC.

    Returns:
        int: The current Unix timestamp.
    """
    return int(time.mktime(get_utc().timetuple()))

def get_timezone(timezone: int) -> str:
    """
    Convert a timezone offset to GMT format.

    Args:
        timezone (int): The timezone offset.

    Returns:
        str: The timezone in GMT format (e.g., 'UTC+2.00').
    """
    sign = '+'
    if int(timezone) < 0:
        sign = ''

    return f'UTC{sign}{int(timezone / 3600)}.00'

def get_forecast_days(data: dict) -> list:
    """
    Select appropriate weather forecast records for the following days.

    Args:
        data (dict): The weather forecast data.

    Returns:
        list: A list of selected weather forecast records.
    """
    data = data['list']
    days = []
    for number, day in enumerate(data):
        day_number = int(get_unix_to_datetime(day['dt'], 'day'))
        hour = int(get_unix_to_datetime(day['dt'], 'hours'))
        days.append((number, day_number, hour))
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
        for number, day in enumerate(data):
            if indicator[0] == number:
                new_days.append(day)

    return new_days

def get_country_codes() -> pd.DataFrame:
    """
    Get country names based on country codes from a website.

    Returns:
        pd.DataFrame: A DataFrame containing country codes and names.
    """
    try:
        data = pd.read_html(
            'https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes', encoding="utf8")[0]
    except ConnectionError:
        print('There was problem with loading country codes')
        return pd.DataFrame() # Return empty Data Frame
    data = data.droplevel(0, axis=1)
    data.reset_index(drop=True, inplace=True)
    country_column = [columns for columns in data.columns if 'Country' in columns][0]
    code_column = [columns for columns in data.columns if 'Alpha-2' in columns][0]
    selected_columns = [country_column, code_column]
    codes_data = data[selected_columns]
    codes_data = codes_data.rename(
        columns={'Country name[5]': 'Country', 'Alpha-2 code[5]': 'Code'})
    condition = codes_data['Code'].str.len() <= 3
    codes_data = codes_data[condition]
    codes_data.set_index('Code', inplace=True)

    return codes_data

def read_country(code: str, code_list: pd.DataFrame) -> str:
    """
    Convert a country code to a country name.

    Args:
        code (str): The country code to be converted.
        code_list (pd.DataFrame): A DataFrame containing country codes and names.

    Returns:
        str: The country name.
    """
    try:
        name = str(code_list.loc[code, 'Country'])
        if len(name) > 10:
            name = code
    except (KeyError, AttributeError):
        print('Code not found')
        name = code
    return name

def draw_city() -> str:
    """
    Pick a random city name.

    Returns:
        str: A randomly selected city name.
    """
    return random.choice(CITIES)

def load_stylesheet() -> str:
    """
    Load a stylesheet file and return its contents as a string.

    Returns:
        str: The contents of the stylesheet file.
    """
    with open('src/style.css', 'r', encoding='utf-8') as file:
        return file.read()
