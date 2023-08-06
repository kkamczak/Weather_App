import requests
import sys
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from support import get_image, get_timezone, get_unix_to_time, get_unix_to_short_date, get_api_key, get_forecast_days, \
    get_country_codes, read_country, draw_city, save_day_to_file, message_box, get_unix
from settings import SMALL_IMAGE_SIZE, BIG_IMAGE_SIZE, BACKGROUND_COLOR, FRAMES_VARIABLES
from options import Options

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
        self.push_Button_Search.clicked.connect(self.search)
        self.action_Close.triggered.connect(exit)
        self.action_Settings.triggered.connect(self.open_options)
        self.action_Save.triggered.connect(lambda: save_day_to_file(self.weather_data, self.forecast_data))
        self.action_Open.triggered.connect(self.open_day_file)

        # Define data-----------------------
        self.weather_data = None
        self.forecast_data = None
        self.forecast_days = None

        self.setStyleSheet(f'background-color: {BACKGROUND_COLOR};')

        self.search(start=True)


    def search(self, start=False, save=None) -> None:
        if save == None:
            if start == False: user_input = self.line_edit_search.text()
            else: user_input = draw_city()
            self.forecast_data = requests.get(
                f'https://api.openweathermap.org/data/2.5/forecast?q={user_input}&lang=pl&units=metric&appid={API_KEY}').json()
            self.weather_data = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={user_input}&lang=pl&units=metric&appid={API_KEY}').json()
            print(self.weather_data)
        else:
            self.weather_data = save[0]
            self.forecast_data = save[1]

        if self.weather_data['cod'] == 401 or self.weather_data['cod'] == '404':
            message_box('There was problem with loading weather data of this location!', self.weather_data['message'])
        else:
            self.update_informations(self.weather_data)

        if self.forecast_data['cod'] == 401 or self.weather_data['cod'] == '404':
            message_box('There was problem with loading forecast data of this location!', self.forecast_data['message'])
        else:
            self.update_forecast(self.forecast_data)



    def update_informations(self, weather: dict) -> None:
        name = weather['name']
        timezone = get_timezone(weather['timezone'])
        country = read_country(weather['sys']['country'], COUNTRY_CODES)
        time = get_unix_to_time(weather['timezone'])
        date = get_unix_to_short_date(weather['dt'])
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
        self.label_Datetime.setText(f"{date} - {time}")
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
            date_now = get_unix_to_short_date(get_unix())
            temp_max = str(round(day['main']['temp_max']))
            temp_min = str(round(day['main']['temp_min']))
            temp = f"{temp_max}°C"
            weather = day['weather'][0]['main']
            icon = day['weather'][0]['icon']
            image = get_image(icon, SMALL_IMAGE_SIZE)
            if i == 0 and date == date_now: getattr(self, f'{FRAMES_VARIABLES[0]}_{i + 1}').setText('today')
            else: getattr(self, f'{FRAMES_VARIABLES[0]}_{i + 1}').setText(date)
            getattr(self, f'{FRAMES_VARIABLES[1]}_{i + 1}').setPixmap(image)
            getattr(self, f'{FRAMES_VARIABLES[2]}_{i + 1}').setText(temp)
            getattr(self, f'{FRAMES_VARIABLES[3]}_{i + 1}').setText(weather)


    def open_options(self) -> None:
        self.options = Options(API_KEY, self.change_api_key)
        self.options.show()

    def change_api_key(self, new_key: str) -> None:
        globals()['API_KEY'] = new_key


    def open_day_file(self) -> None:
        file_name = QFileDialog.getOpenFileName(self, 'Open file', 'D:\GitHub\Weather_App\saves', '*.json')
        try:
            with open(file_name[0], 'r') as f:
                content = json.load(f)
            self.search(save=content)
        except FileNotFoundError:
            print('No such directory')



def main():

    app = QApplication(sys.argv)
    window = MyGUI()
    app.exec_()

    raise RuntimeError

if __name__ == '__main__':
    main()