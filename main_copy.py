import requests
import sys
import settings
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage

API_KEY = 'b4e4fbe1b77cc812f09ffd954f8f791a'

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
    def __init__(self):
        super().__init__()
        uic.loadUi('mygui.ui', self)

        self.pushButtonSearch.clicked.connect(self.search)
        self.action_Close.triggered.connect(exit)

        self.small_frames = settings.SMALL_FRAMES

        self.show()


    def search(self):

        user_input = self.line_edit_search.text()
        forecast_data = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={user_input}&lang=pl&units=metric&appid={API_KEY}')
        weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_input}&lang=pl&units=metric&appid={API_KEY}')

        #print(forecast_data.json())

        if weather_data.json()['cod'] == '404':
            self.message_box('Wrong location name!')
        else:
            self.update_informations(weather_data, forecast_data)

    def update_informations(self, data, forecast):
        name = data.json()['name']
        timezone = (f'UTC+{int(data.json()["timezone"] / 3600)}.00')
        country = data.json()['sys']['country']
        time = str(datetime.fromtimestamp(data.json()['dt']).strftime('%H:%M'))
        weather = data.json()['weather'][0]['description']
        temp = str(round(data.json()['main']['temp']))
        humidity = str(round(data.json()['main']['humidity']))
        pressure = str(data.json()['main']['pressure'])
        wind = str(data.json()['wind']['speed'])
        sunrise = str(datetime.fromtimestamp(data.json()['sys']['sunrise']).strftime('%H:%M'))
        sunset = str(datetime.fromtimestamp(data.json()['sys']['sunset']).strftime('%H:%M'))
        image = QPixmap('full_sun.png')

        self.label_Name.setText(name)
        self.label_Timezone.setText(f'{timezone} {country}')
        self.label_Datetime.setText(time)
        self.label_Weather.setText(weather)
        self.label_Temperature_display.setText(temp)
        self.label_Humidity_display.setText(pressure)
        self.label_Pressure_display.setText(humidity)
        self.label_Wind_display.setText(wind)
        self.label_Sunrise_display.setText(sunrise)
        self.label_Sunset_display.setText(sunset)

        self.label_main_image.setPixmap(image)


        self.update_frames(forecast)

    def message_box(self, msg):
        message = QMessageBox()
        message.setText(msg)
        message.exec_()

    def update_frames(self, data):
        for id, day in enumerate(self.small_frames):
            lp=id*5
            date = str(datetime.fromtimestamp(data.json()['list'][lp]['dt']).strftime('%d.%m'))
            #image = QPixmap('small_full_sun.png')
            image = get_image()
            temp = str(round(data.json()['list'][lp]['main']['temp']))
            weather = data.json()['list'][lp]['weather'][0]['main']
            getattr(self, f'{settings.SMALL_FRAMES_VARIABLES[0]}_{id + 1}').setText(date)
            getattr(self, f'{settings.SMALL_FRAMES_VARIABLES[1]}_{id + 1}').setPixmap(image)
            getattr(self, f'{settings.SMALL_FRAMES_VARIABLES[2]}_{id + 1}').setText(temp)
            getattr(self, f'{settings.SMALL_FRAMES_VARIABLES[3]}_{id + 1}').setText(weather)

def get_image():
    url='https://openweathermap.org/img/wn/10d@2x.png'
    image = QImage()
    image.loadFromData(requests.get(url).content)

    return QPixmap(image).scaled(settings.SMALL_IMAGE_SIZE[0], settings.SMALL_IMAGE_SIZE[1])

def get_utc():
    return datetime.utcnow()

def main():

    app = QApplication(sys.argv)
    window = MyGUI()
    app.exec_()


    raise RuntimeError

if __name__ == '__main__':
    main()