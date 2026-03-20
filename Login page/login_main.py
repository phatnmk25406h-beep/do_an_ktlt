import sys
from PyQt6.QtWidgets import QApplication
from login_ext import LoginWindow
from splash_screen import SplashScreen


app = QApplication(sys.argv)
splash = SplashScreen()
def open_login():
    splash.close()
    w = LoginWindow()
    w.show()
splash.finished.connect(open_login)
splash.show()
sys.exit(app.exec())
