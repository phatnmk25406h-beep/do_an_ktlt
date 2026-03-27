import sys
from PyQt6.QtWidgets import QApplication

from src.controllers.login_controller import LoginWindow
from src.view.giaodien_splash_ui import SplashScreen


def main():
	app = QApplication(sys.argv)

	splash = SplashScreen()
	login = LoginWindow()

	splash.finished.connect(lambda: (splash.close(), login.show()))
	splash.show()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()