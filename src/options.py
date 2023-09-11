'''
This module is responsible for displaying the options window and its content.
'''
from typing import Callable
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from src.settings import STYLE
from src.support import save_api_key


class Options(QWidget):
    """
    This class represents the options window for managing API keys.

    Args:
        api_key (str): The initial API key.
        change_api_key (Callable[[str], None]): A callable function to change the API key.

    Attributes:
        api_key (str): The current API key.
        change_api_key (Callable[[str], None]): A callable function to change the API key.

    Methods:
        read_new_api(): Reads and updates the API key based on user input.
        show_api_key(): Displays the current API key in the user interface.

    """
    def __init__(self, api_key: str, change_api_key: Callable[[str], None]) -> None:
        """
        Initialize the Options window.

        Args:
            api_key (str): The initial API key.
            change_api_key (Callable[[str], None]): A callable function to change the API key.

        Returns:
            None
        """
        super().__init__()
        # Load and init GUI-----------------
        uic.loadUi('src/gui/options.ui', self)

        self.api_key = api_key
        self.change_api_key = change_api_key
        self.show_api_key()

        # Configure all buttons-------------
        self.push_Button_Save.clicked.connect(self.read_new_api)
        self.push_Button_Close.clicked.connect(self.close)

        # Define data-----------------------

        self.setStyleSheet(STYLE)

    def read_new_api(self) -> None:
        """
        Read and update the API key based on user input.

        Returns:
            None
        """
        user_input = self.line_edit_api.text()
        self.change_api_key(user_input)
        self.api_key = user_input
        self.show_api_key()
        save_api_key(user_input)

    def show_api_key(self) -> None:
        """
        Display the current API key in the user interface.

        Returns:
            None
        """
        self.label_api_current.setText(f'Current API Key: {self.api_key}')
