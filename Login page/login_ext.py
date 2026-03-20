from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6.QtCore import Qt, QTimer,QThread,pyqtSignal
import sys
from Login_v3 import Ui_MainWindow
from google_login import login_with_google
from facebook_login import FacebookLoginDialog

#tách riêng cho khỏi lag
class GoogleLoginWorker(QThread): #QThread dùng để chạy luồng riêng, which is hàm run
    success = pyqtSignal(dict)   # Phát khi đăng nhập thành công
    failed  = pyqtSignal(str)    # Phát khi thất bại
 # Vì 2 thread chạy song song nên cần có pyqt signal để báo cho nhau
    def run(self):
        user = login_with_google()
        if user:
            self.success.emit(user)
        else:
            self.failed.emit("Đăng nhập Google thất bại!")


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.login()
        self._center_window()
        self.ui.frame.hide() 
        

    def _center_window(self): # set màn hình ở giữa 
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width()  - self.width())  // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def login(self):
        # Login
        self.ui.btnLogin_Enter.clicked.connect(self.check_var)
        self.ui.btn_Signup_2.clicked.connect(self.check_var_sgn)

        # Tab switch
        self.ui.btn_Login.clicked.connect(self.switch_to_login_tab)
        self.ui.btn_Signup.clicked.connect(self.switch_to_signup_tab)

        # Click Sign Up/Login phụ ( chỗ M3M ) -> vẫn là Tab switch =))
        self.ui.label_firsttime_full.mousePressEvent = lambda e: self.switch_to_signup_tab()
        self.ui.label_login1.mousePressEvent = lambda e: self.switch_to_login_tab()

        # Clear lỗi khi user gõ lại mail or pass or username (login)
        self.ui.enter_email.textChanged.connect(self._clear_email_error)
        self.ui.enter_password.textChanged.connect(self._clear_password_error)
        self.ui.lineEdit_username.textChanged.connect(self._clear_general_error)

         # Clear lỗi khi user gõ lại mail or pass or username (sgn)
        self.ui.enter_email_signup.textChanged.connect(self._clear_email_error_sgnup)
        self.ui.enter_password_signup.textChanged.connect(self._clear_password_error_sgn)
        self.ui.Signup_username.textChanged.connect(self._clear_general_error_sgn)

        #button liên kết đăng nhập/ký với trình duyệt bên ngoài
        self.ui.login_fb.clicked.connect(self.handle_facebook_login)
        self.ui.login_gg.clicked.connect(self.handle_google_login)
        self.ui.login_fb_2.clicked.connect(self.handle_facebook_login)
        self.ui.signup_gg_2.clicked.connect(self.handle_google_login)

    # Styles Sheet gián tiếp ( aka set style sheet cho các ô label) 
    _STYLE_NORMAL = """QLineEdit{
        border:1.5px solid #FEC300;border-radius:8px;
        padding:4px 10px;background:white;font-size:13px;color:#555;
    }QLineEdit:focus{border:1.5px solid #34C759;}"""

    _STYLE_ERROR = """QLineEdit{
        border:1.5px solid #e53935;border-radius:8px;
        padding:4px 10px;background:#fff5f5;font-size:13px;color:#555;
    }"""

    _STYLE_OK = """QLineEdit{
        border:1.5px solid #34C759;border-radius:8px;
        padding:4px 10px;background:white;font-size:13px;color:#555;
    }"""

    # Chuyển tab  - đổi màu với font là chính
    def switch_to_login_tab(self):
        self.ui.btn_Login.setStyleSheet("""QPushButton{
            background:#34C759;color:white;border-radius:8px;
            font-weight:bold;font-size:13px;border:none;}""")
        self.ui.btn_Signup.setStyleSheet("""QPushButton{
            background:transparent;color:#a259ff;border-radius:8px;
            font-weight:bold;font-size:13px;border:none;}
            QPushButton:hover{background:#d8d8d8;}""")
        self.ui.Signup_username.setText("")
        self.ui.enter_email_signup.setText("")
        self.ui.enter_password_signup.setText("")
        self.ui.Signup_Pnumber.setText("")
        self.ui.Signup_age.setText("")
        self._clear_email_error_sgnup
        self._clear_general_error_sgn
        self._clear_password_error_sgn
        self.ui.frame.hide()


    def switch_to_signup_tab(self): # giống như cái trên
        """Signup tab active"""
        self.ui.btn_Signup.setStyleSheet("""QPushButton{
            background:#34C759;color:white;border-radius:8px;
            font-weight:bold;font-size:13px;border:none;}""")
        self.ui.btn_Login.setStyleSheet("""QPushButton{
            background:transparent;color:#a259ff;border-radius:8px;
            font-weight:bold;font-size:13px;border:none;}
            QPushButton:hover{background:#d8d8d8;}""")
        self.ui.lineEdit_username.setText("")
        self.ui.enter_email.setText("")
        self.ui.enter_password.setText("")
        self._clear_email_error
        self._clear_general_error
        self._clear_password_error
        self.ui.frame.show()

    # Show noti 
    def show_password_error(self, msg: str = "Password không hợp lệ"):
        self.ui.noti_password.setText(msg)
        self.ui.enter_password.setStyleSheet(self._STYLE_ERROR)
        self.ui.label_forgot.setText("Bạn quên mật khẩu?")

    def show_password_error_sgn(self, msg: str = "Password không hợp lệ"):
        self.ui.noti_password_signup.setText(msg)
        self.ui.enter_password_signup.setStyleSheet(self._STYLE_ERROR)
        self.ui.label_forgot_2.setText("Bạn quên mật khẩu?")

    def show_email_error(self, msg: str = "Email không hợp lệ"):
        self.ui.noti_email.setText(msg)
        self.ui.enter_email.setStyleSheet(self._STYLE_ERROR)
    
    def show_email_error_sgn(self, msg: str = "Email không hợp lệ"):
        self.ui.noti_email_signup.setText(msg)
        self.ui.enter_email_signup.setStyleSheet(self._STYLE_ERROR)

    def show_general_error(self, msg: str):
        self.ui.noti_general.setText(msg)
        self.ui.noti_general.setStyleSheet(
            "QLabel{color:#e53935;font-size:11px;background:transparent;border:none;}")
    
    def show_general_error_sgn(self, msg: str):
        self.ui.noti_general_2.setText(msg)
        self.ui.noti_general_2.setStyleSheet(
            "QLabel{color:#e53935;font-size:11px;background:transparent;border:none;}")

    def show_general_success(self, msg: str):
        self.ui.noti_general.setText(msg)
        self.ui.noti_general.setStyleSheet(
            "QLabel{color:#34C759;font-size:11px;background:transparent;border:none;font-weight:bold;}")

    def show_general_success_sgn(self, msg: str):
        self.ui.noti_general_2.setText(msg)
        self.ui.noti_general_2.setStyleSheet(
            "QLabel{color:#34C759;font-size:11px;background:transparent;border:none;font-weight:bold;}")
    def show_toast(self, msg: str, success: bool = True, duration_ms: int = 3000): # set giờ hiện
        if success:
            self.show_general_success(msg)
        else:
            self.show_general_error(msg)
        QTimer.singleShot(duration_ms, lambda: self.ui.noti_general.setText(""))

    def show_toast_sgn(self, msg: str, success: bool = True, duration_ms: int = 3000): # set giờ hiện
        if success:
            self.show_general_success_sgn(msg)
        else:
            self.show_general_error_sgn(msg)
        QTimer.singleShot(duration_ms, lambda: self.ui.noti_general_2.setText(""))


    # Reset noti error
    def _clear_email_error(self):
        self.ui.noti_email.setText("")
        self.ui.enter_email.setStyleSheet(self._STYLE_NORMAL)

    def _clear_email_error_sgnup(self):
        self.ui.noti_email_signup.setText("")
        self.ui.enter_email_signup.setStyleSheet(self._STYLE_NORMAL)

    def _clear_password_error(self):
        self.ui.noti_password.setText("")
        self.ui.label_forgot.setText("")
        self.ui.enter_password.setStyleSheet(self._STYLE_NORMAL)

    def _clear_password_error_sgn(self):
        self.ui.noti_password_signup.setText("")
        self.ui.label_forgot_2.setText("")
        self.ui.enter_password_signup.setStyleSheet(self._STYLE_NORMAL)

    def _clear_general_error(self):
        self.ui.noti_general.setText("")

    def _clear_general_error_sgn(self):
        self.ui.noti_general_2.setText("")
    
    # Check var signup
    def check_var_sgn(self):
        usernamesgn = self.ui.Signup_username.text().strip()
        emailsgn    = self.ui.enter_email_signup.text().strip()
        passwordsgn = self.ui.enter_password_signup.text()
        phonenumbersgn = self.ui.Signup_Pnumber.text()
        agesgn = self.ui.Signup_age.text()
        valid = True

        if not usernamesgn:
            self.show_general_error_sgn(" Vui lòng nhập username")
            valid = False

        if not emailsgn or "@" not in emailsgn:
            self.show_email_error_sgn("Email không hợp lệ")
            valid = False
        else:
            self._clear_email_error_sgnup()

        if len(passwordsgn) <= 6:
            self.show_password_error_sgn(" Độ dài password nên >6")
            valid = False
        else:
            self._clear_password_error_sgn()

        if valid:
            # TODO: gọi API, nhớ nhaaaaaa
            self.show_toast_sgn("Đăng ký thành công!", success=True)
    # Check var login 
    def check_var(self):
        username = self.ui.lineEdit_username.text().strip()
        email    = self.ui.enter_email.text().strip()
        password = self.ui.enter_password.text()
        valid = True

        if not username:
            self.show_general_error(" Vui lòng nhập username")
            valid = False

        if not email or "@" not in email:
            self.show_email_error("Email không hợp lệ")
            valid = False
        else:
            self._clear_email_error()

        if len(password) <= 6:
            self.show_password_error(" Độ dài password nên >6")
            valid = False
        else:
            self._clear_password_error()

        if valid:
            # TODO: gọi API, nhớ nhaaaaaa
            self.show_toast("Đăng nhập thành công!", success=True)
           
    
     #--- Google Login ---------
    def handle_google_login(self):
        #Nhấn login_gg sẽ mở trình duyệt chọn tài khoản Google
        self.show_toast("Đang mở trình duyệt...", success=True, duration_ms=10000)
        self.ui.login_gg.setEnabled(False) 
        self.ui.signup_gg_2.setEnabled(False) # Disable button cho khỏi spam !!!!!
 
        # Chạy ở thread riêng (khỏi lag UI)
        self._google_worker = GoogleLoginWorker()
        self._google_worker.success.connect(self._on_google_success)
        self._google_worker.failed.connect(self._on_google_failed)
        self._google_worker.start()
 
    def _on_google_success(self, user: dict):
        #Nhận thông tin user sau khi đăng nhập Google thành công
        self.ui.login_gg.setEnabled(True)
        self.ui.signup_gg_2.setEnabled(True)
        name  = user.get('name', '')
        email = user.get('email', '')
        print(f"[Google] Đăng nhập thành công: {name} - {email}")
        self.show_toast(f"Xin chào {name}!", success=True)
        self.show_toast_sgn(f"Xin chào {name}!", success=True)

        # TODO: chuyển sang màn hình chính
        #self.open_main_window(user)
 
    def _on_google_failed(self, error_msg: str):
        #Xử lý khi đăng nhập Google thất bại
        self.ui.login_gg.setEnabled(True)
        self.ui.signup_gg_2.setEnabled(True)
        self.show_toast(error_msg, success=False)
        self.show_toast_sgn(error_msg, success=False)
        
    # -- FB Login ------
    def handle_facebook_login(self):
        dialog = FacebookLoginDialog(self)
        dialog.login_success.connect(self._on_facebook_success)
        dialog.exec()

    def _on_facebook_success(self, user: dict):
        name = user.get('name', '')
        self.show_toast(f"Xin chào {name}!", success=True)
        print(f"[Facebook] {name} - {user.get('email')}")
        

# Các chức năng cần kiểm thử --------------
# Raise error, login logic, add vào database
# Chưa test kết nối vào data base
#Chưa nối với main screen