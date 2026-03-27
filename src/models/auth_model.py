import os
import importlib
import pandas as pd
import requests
from PyQt6.QtCore import QThread, pyqtSignal, QUrl
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

try:
    QWebEngineView = importlib.import_module("PyQt6.QtWebEngineWidgets").QWebEngineView
except Exception:
    QWebEngineView = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
EXCEL_FILE = os.path.join(DATA_DIR, "users_data.xlsx")


class LocalAuth:
    @staticmethod
    def init_excel_file():
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(EXCEL_FILE):
            df = pd.DataFrame(columns=["Username", "Email", "Password", "Phone", "Age", "Level"])
            df.to_excel(EXCEL_FILE, index=False)

    @staticmethod
    def register_user(user_data):
        LocalAuth.init_excel_file()
        df = pd.read_excel(EXCEL_FILE)
        if user_data["Email"] in df["Email"].astype(str).values:
            return False, "Email này đã được sử dụng!"
        df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        return True, "Đăng ký thành công!"

    @staticmethod
    def check_login(email, password):
        LocalAuth.init_excel_file()
        df = pd.read_excel(EXCEL_FILE)
        df["Email"] = df["Email"].astype(str)
        df["Password"] = df["Password"].astype(str)
        match = df[(df["Email"] == email) & (df["Password"] == password)]
        if not match.empty:
            return True, "Đăng nhập thành công!"
        return False, "Email hoặc Mật khẩu không chính xác!"


class GoogleLoginWorker(QThread):
    success = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def run(self):
        try:
            secret_path = os.path.join(BASE_DIR, "client_secret.json")
            flow = InstalledAppFlow.from_client_secrets_file(
                secret_path,
                [
                    "openid",
                    "https://www.googleapis.com/auth/userinfo.email",
                    "https://www.googleapis.com/auth/userinfo.profile",
                ],
            )
            creds = flow.run_local_server(port=0)
            service = build("oauth2", "v2", credentials=creds)
            user_info = service.userinfo().get().execute()
            self.success.emit({"name": user_info.get("name", ""), "email": user_info.get("email", "")})
        except Exception as e:
            self.failed.emit(f"Đăng nhập Google thất bại: {e}")


APP_ID = "959407916546181"
APP_SECRET = "a81b437a40a0d3d14abd249f679c9af9"
REDIRECT = "https://www.facebook.com/connect/login_success.html"


class FacebookLoginDialog(QDialog):
    login_success = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đăng nhập Facebook")
        self.resize(600, 700)
        layout = QVBoxLayout(self)
        if QWebEngineView is None:
            fallback = QLabel("Thiếu PyQt6-WebEngine. Hãy cài gói này để dùng Facebook Login.")
            fallback.setWordWrap(True)
            layout.addWidget(fallback)
            return

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        url = (
            "https://www.facebook.com/dialog/oauth?"
            f"client_id={APP_ID}&redirect_uri={REDIRECT}&scope=email,public_profile"
        )
        self.browser.load(QUrl(url))
        self.browser.urlChanged.connect(self.check_redirect)

    def check_redirect(self, url):
        url_str = url.toString()
        if REDIRECT in url_str and "code=" in url_str:
            code = url_str.split("code=")[1].split("&")[0]
            token = requests.get(
                "https://graph.facebook.com/v18.0/oauth/access_token",
                params={
                    "client_id": APP_ID,
                    "client_secret": APP_SECRET,
                    "redirect_uri": REDIRECT,
                    "code": code,
                },
                timeout=30,
            ).json().get("access_token")

            user_info = requests.get(
                "https://graph.facebook.com/me",
                params={"fields": "name,email,picture", "access_token": token},
                timeout=30,
            ).json()
            self.login_success.emit({"name": user_info.get("name", "")})
            self.close()


config = {
    "apiKey": "AIzaSyB75TxAPMSv9e__3Poql_fiCpx3XVW6zTU",
    "authDomain": "m3m-english.firebaseapp.com",
    "projectId": "m3m-english",
    "storageBucket": "m3m-english.firebasestorage.app",
    "messagingSenderId": "529571980593",
    "appId": "1:529571980593:web:8c32e11576a1d2d6a73c10",
    "measurementId": "G-B9ZFE1G1EG",
    "databaseURL": "https://m3m-english-default-rtdb.asia-southeast1.firebasedatabase.app/",
}

try:
    pyrebase_module = importlib.import_module("pyrebase")
    firebase = pyrebase_module.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()
except Exception:
    firebase = None
    auth = None
    db = None
