#!/usr/bin/env python3
import sys
import os

# Simulate file path như trong account_page_controller.py (ở src/controllers/)
fake_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "controllers", "account_page_controller.py"))

# Tính toán base_dir giống như trong code thực
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(fake_file_path)))
img_path = os.path.join(base_dir, "trang_tri", "images", "motivation.jpg")

print(f"Fake file path: {fake_file_path}")
print(f"base_dir: {base_dir}")
print(f"img_path: {img_path}")
print(f"File tồn tại: {os.path.exists(img_path)}")

# Test import
try:
    from src.view.giaodien_account_page import Ui_MainWindow
    print("✓ Import Ui_MainWindow: OK")
except ImportError as e:
    print(f"✗ Import Ui_MainWindow: {e}")
