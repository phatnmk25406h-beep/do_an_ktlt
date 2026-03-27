import os

import pandas as pd

from src.config.settings import BASE_DIR

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
