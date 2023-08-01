import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import sys

API_KEY = 'b4e4fbe1b77cc812f09ffd954f8f791a'

class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mygui.ui', self)
        self.show()
        self.pushButtonSearch.clicked.connect(self.search)
        # self.pushButton_2.clicked.connect(lambda: self.sayit(self.textEdit.toPlainText()))
        self.action_Close.triggered.connect(exit)
        self.label_Weather_image.setPixmap(QtGui.QPixmap("sun.jpg"))

        pixmap = QPixmap('image.png')

    def search(self):
        print('Halo')
        user_input = self.line_edit_search.text()
        print(user_input)
        weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_input}&lang=pl&units=metric&appid={API_KEY}')

        if weather_data.json()['cod'] == '404':
            self.message_box('Wrong location name!')
        else:
            print('lol')
            self.enable_informations()
            print('sex')
            self.update_informations(weather_data)

    def enable_informations(self):
        self.label_Name.setEnabled(True)
        self.label_Country.setEnabled(True)
        self.label_Weather.setEnabled(True)
        self.label_Temperature.setEnabled(True)
        self.label_Pressure.setEnabled(True)

    def update_informations(self, data):
        name = data.json()['name']
        country = data.json()['sys']['country']
        weather = data.json()['weather'][0]['description']
        lat = data.json()['coord']['lat']
        lon = data.json()['coord']['lon']
        temp = str(round(data.json()['main']['temp']))
        pressure = str(data.json()['main']['pressure'])
        self.label_Name_display.setText(name)
        self.label_Country_display.setText(country)
        self.label_Weather_display.setText(weather)
        self.label_Temperature_display.setText(temp)
        self.label_Pressure_display.setText(pressure)

    def message_box(self, msg):
        message = QMessageBox()
        message.setText(msg)
        message.exec_()

def main():

    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()