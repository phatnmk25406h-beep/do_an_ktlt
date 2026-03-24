from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow

from src.models.auth_model import LocalAuth, GoogleLoginWorker, FacebookLoginDialog
from src.controllers.home_controller import DieuPhoiApp
from src.view.Login_v3 import Ui_MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        LocalAuth.init_excel_file()
        self._google_worker = None
        self.app_coordinator = None

        self.setup_connections()
        self.switch_to_login_tab()

    def setup_connections(self):
        self.ui.btnLogin_Enter.clicked.connect(self.handle_login)
        self.ui.btn_Signup_2.clicked.connect(self.handle_signup)
        self.ui.btn_Login.clicked.connect(self.switch_to_login_tab)
        self.ui.btn_Signup.clicked.connect(self.switch_to_signup_tab)

        self.ui.login_gg.clicked.connect(self.start_google_login)
        self.ui.login_fb.clicked.connect(self.start_facebook_login)

    def switch_to_login_tab(self):
        self.ui.frame.hide()
        self.ui.btn_Login.setStyleSheet(
            "QPushButton{background:#34C759;color:white;border-radius:8px;font-weight:bold;font-size:13px;border:none;}"
            "QPushButton:hover{background:#2db34e;}"
        )
        self.ui.btn_Signup.setStyleSheet(
            "QPushButton{background:transparent;color:#a259ff;border-radius:8px;font-weight:bold;font-size:13px;border:none;}"
            "QPushButton:hover{background:#d8d8d8;}"
        )

    def switch_to_signup_tab(self):
        self.ui.frame.show()
        self.ui.btn_Signup.setStyleSheet(
            "QPushButton{background:#34C759;color:white;border-radius:8px;font-weight:bold;font-size:13px;border:none;}"
            "QPushButton:hover{background:#2db34e;}"
        )
        self.ui.btn_Login.setStyleSheet(
            "QPushButton{background:transparent;color:#a259ff;border-radius:8px;font-weight:bold;font-size:13px;border:none;}"
            "QPushButton:hover{background:#d8d8d8;}"
        )

    def handle_signup(self):
        user_data = {
            "Username": self.ui.Signup_username.text().strip(),
            "Email": self.ui.enter_email_signup.text().strip(),
            "Password": self.ui.enter_password_signup.text(),
            "Phone": self.ui.Signup_Pnumber.text().strip(),
            "Age": self.ui.Signup_age.text().strip(),
            "Level": 1,
        }

        if not user_data["Email"] or not user_data["Password"]:
            self.show_email_error_sgn("Email và Password không được để trống!")
            return

        is_success, message = LocalAuth.register_user(user_data)
        if is_success:
            self.show_toast_sgn(message)
            self.switch_to_login_tab()
        else:
            self.show_email_error_sgn(message)

    def handle_login(self):
        email = self.ui.enter_email.text().strip()
        password = self.ui.enter_password.text()

        is_success, message = LocalAuth.check_login(email, password)
        if is_success:
            self.show_toast(message)
            QTimer.singleShot(700, self.open_homepage)
        else:
            self.show_general_error(message)

    def start_google_login(self):
        self.show_toast("Đang mở trình duyệt...")
        self._google_worker = GoogleLoginWorker()
        self._google_worker.success.connect(self.on_social_success)
        self._google_worker.failed.connect(self.show_general_error)
        self._google_worker.start()

    def start_facebook_login(self):
        dialog = FacebookLoginDialog(self)
        dialog.login_success.connect(self.on_social_success)
        dialog.exec()

    def on_social_success(self, user):
        self.show_toast(f"Xin chào {user.get('name', '')}!")
        QTimer.singleShot(700, self.open_homepage)

    def show_general_error(self, message):
        self.ui.noti_general.setStyleSheet("QLabel{color:#e53935;font-size:11px;background:transparent;border:none;}")
        self.ui.noti_general.setText(message)

    def show_toast(self, message):
        self.ui.noti_general.setStyleSheet("QLabel{color:#2e7d32;font-size:11px;background:transparent;border:none;}")
        self.ui.noti_general.setText(message)
        QTimer.singleShot(2500, lambda: self.ui.noti_general.setText(""))

    def show_email_error_sgn(self, message):
        self.ui.noti_email_signup.setText(message)
        self.ui.noti_general_2.setText(message)

    def show_toast_sgn(self, message):
        self.ui.noti_general_2.setStyleSheet("QLabel{color:#2e7d32;font-size:11px;background:transparent;border:none;}")
        self.ui.noti_general_2.setText(message)
        QTimer.singleShot(2500, lambda: self.ui.noti_general_2.setText(""))

    def open_homepage(self):
        self.app_coordinator = DieuPhoiApp()
        self.app_coordinator.trang_chu.show()
        self.close()