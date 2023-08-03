import requests
import sys
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from support import get_utc, get_image, get_timezone, get_unix_to_time, get_unix_to_short_date, get_api_key, get_forecast_days, \
    get_country_codes, read_country
from settings import SMALL_IMAGE_SIZE, BIG_IMAGE_SIZE, BACKGROUND_COLOR, FORECAST_FRAMES_AMOUNT, FRAMES_VARIABLES

API_KEY = get_api_key()
COUNTRY_CODES = get_country_codes()


#---------CATCHING ERRORS-------------------------------------------------------------------------------------
def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(t))
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions
#------------------------------------------------------------------------------------------------------------

class MyGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # Load and init GUI-----------------
        uic.loadUi('gui/mygui.ui', self)
        self.show()

        # Configure all buttons-------------
        self.pushButtonSearch.clicked.connect(self.search)
        self.action_Close.triggered.connect(exit)

        # Define data-----------------------
        self.weather_data = None
        self.forecast_data = None
        self.forecast_days = None

        self.setStyleSheet(f'background-color: {BACKGROUND_COLOR};')



    def search(self) -> None:

        user_input = self.line_edit_search.text()
        self.forecast_data = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={user_input}&lang=pl&units=metric&appid={API_KEY}').json()
        self.weather_data = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={user_input}&lang=pl&units=metric&appid={API_KEY}').json()


        if self.weather_data['cod'] == 401:
            self.message_box('There was problem with loading weather data of this location!', self.weather_data['message'])
        else:
            self.update_informations(self.weather_data)

        if self.forecast_data['cod'] == 401:
            self.message_box('There was problem with loading forecast data of this location!', self.forecast_data['message'])
        else:
            self.update_forecast(self.forecast_data)


    def update_informations(self, weather: dict) -> None:
        name = weather['name']
        timezone = get_timezone(weather['timezone'])
        country = read_country(weather['sys']['country'], COUNTRY_CODES)
        time = get_unix_to_time(weather['dt'], timezone=weather['timezone'])
        weather_description = weather['weather'][0]['description']
        temp = f"{round(weather['main']['temp'])}°C"
        humidity = f"{str(round(weather['main']['humidity']))}%"
        pressure = f"{str(weather['main']['pressure'])}hPa"
        wind = f"{str(weather['wind']['speed'])}m/s"
        sunrise = get_unix_to_time(weather['sys']['sunrise'])
        sunset = get_unix_to_time(weather['sys']['sunset'])
        icon = weather['weather'][0]['icon']
        image = get_image(icon, BIG_IMAGE_SIZE)

        self.label_Name.setText(name)
        self.label_Timezone.setText(f'{timezone} {country}')
        self.label_Datetime.setText(time)
        self.label_Weather.setText(weather_description)
        self.label_Temperature_display.setText(temp)
        self.label_Humidity_display.setText(humidity)
        self.label_Pressure_display.setText(pressure)
        self.label_Wind_display.setText(wind)
        self.label_Sunrise_display.setText(sunrise)
        self.label_Sunset_display.setText(sunset)
        self.label_main_image.setPixmap(image)

    def update_forecast(self, forecast: dict) -> None:
        forecast_days = get_forecast_days(forecast)

        for i, day in enumerate(forecast_days):
            date = get_unix_to_short_date(day['dt'])
            temp_max = str(round(day['main']['temp_max']))
            temp_min = str(round(day['main']['temp_min']))
            temp = f"{temp_max}°C"
            weather = day['weather'][0]['main']
            icon = day['weather'][0]['icon']
            image = get_image(icon, SMALL_IMAGE_SIZE)
            getattr(self, f'{FRAMES_VARIABLES[0]}_{i + 1}').setText(date)
            getattr(self, f'{FRAMES_VARIABLES[1]}_{i + 1}').setPixmap(image)
            getattr(self, f'{FRAMES_VARIABLES[2]}_{i + 1}').setText(temp)
            getattr(self, f'{FRAMES_VARIABLES[3]}_{i + 1}').setText(weather)

    def message_box(self, msg: str, info: str = None) -> None:
        if info != None: text = f'{msg}\n--message: "{info}"'
        else: text = msg
        message = QMessageBox()
        message.setText(text)
        message.exec_()

def main():

    app = QApplication(sys.argv)
    window = MyGUI()
    app.exec_()

    raise RuntimeError

if __name__ == '__main__':
    main()