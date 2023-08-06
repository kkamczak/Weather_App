from PyQt5.QtWidgets import *
from PyQt5 import uic
from settings import BACKGROUND_COLOR
from support import save_api_key

class Options(QWidget):
    def __init__(self, api_key, change_api_key) -> None:
        super().__init__()
        # Load and init GUI-----------------
        uic.loadUi('gui/options.ui', self)

        self.api_key = api_key
        self.change_api_key = change_api_key
        self.show_api_key()

        # Configure all buttons-------------
        self.push_Button_Save.clicked.connect(self.read_new_api)
        self.push_Button_Close.clicked.connect(self.close)

        # Define data-----------------------

        self.setStyleSheet(f'background-color: {BACKGROUND_COLOR};')

    def read_new_api(self):
        user_input = self.line_edit_api.text()
        self.change_api_key(user_input)
        self.api_key = user_input
        self.show_api_key()
        save_api_key(user_input)

    def show_api_key(self):
        self.label_api_current.setText(f'Current API Key: {self.api_key}')
