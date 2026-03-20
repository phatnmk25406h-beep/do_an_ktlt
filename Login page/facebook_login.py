from PyQt6.QtWebEngineWidgets import QWebEngineView #lib cho phép nhúng trình duyệt mini vào app
from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtWidgets import QDialog, QVBoxLayout
import requests

APP_ID     = "959407916546181"      
APP_SECRET = "a81b437a40a0d3d14abd249f679c9af9"  
REDIRECT   = "https://www.facebook.com/connect/login_success.html" #URL đặc biệt của Facebook — sau khi user đăng nhập xong, Facebook tự redirect về đây.


class FacebookLoginDialog(QDialog):
    login_success = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đăng nhập Facebook")
        self.resize(600, 700)

        # Nhúng trình duyệt mini vào dialog
        self.browser = QWebEngineView()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        # Mở trang đăng nhập Facebook
        url = (
            f"https://www.facebook.com/dialog/oauth?"
            f"client_id={APP_ID}"
            f"&redirect_uri={REDIRECT}"
            f"&scope=email,public_profile"
        )
        self.browser.load(QUrl(url))
        self.browser.urlChanged.connect(self.check_redirect)

    def check_redirect(self, url):
        # Khi Facebook redirect về → lấy token
        url_str = url.toString()
        if REDIRECT in url_str and "code=" in url_str:
            code = url_str.split("code=")[1].split("&")[0]
            self.get_user_info(code)
            self.close()

    def get_user_info(self, code):
        # Đổi code lấy token
        token_url = (
            f"https://graph.facebook.com/v18.0/oauth/access_token?"
            f"client_id={APP_ID}&client_secret={APP_SECRET}"
            f"&redirect_uri={REDIRECT}&code={code}"
        )
        token = requests.get(token_url).json().get("access_token")

        # Dùng token lấy thông tin user
        user_url = f"https://graph.facebook.com/me?fields=name,email,picture&access_token={token}"
        user_info = requests.get(user_url).json()

        self.login_success.emit({
            "name":    user_info.get("name", ""),
            "email":   user_info.get("email", ""),
            "picture": user_info.get("picture", {}).get("data", {}).get("url", "")
        })