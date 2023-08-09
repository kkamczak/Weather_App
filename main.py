'''
This module is responsible for displaying the program window and its content.
'''
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.program import MyGUI

sys.path.append('/src')

#---------CATCHING ERRORS--------------------------------------
def catch_exceptions(type, value, traceback):
    QMessageBox.critical(None,
                                   "An exception was raised",
                                   f"Exception type: {type}")
    old_hook(type, value, traceback)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions
#--------------------------------------------------------------

def main():

    app = QApplication(sys.argv)
    MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()
