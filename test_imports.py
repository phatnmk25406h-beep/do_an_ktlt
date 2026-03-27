#!/usr/bin/env python3
import sys
import os

# Test 1: Import Ui_MainWindow
try:
    from src.view.giaodien_account_page import Ui_MainWindow
    print("✓ Import Ui_MainWindow thành công")
except ImportError as e:
    print(f"✗ Lỗi import Ui_MainWindow: {e}")
    sys.exit(1)

# Test 2: Kiểm tra đường dẫn ảnh
try:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    img_path = os.path.join(base_dir, "trang_tri", "images", "motivation.jpg")
    exists = os.path.exists(img_path)
    print(f"✓ Đường dẫn ảnh: {img_path}")
    print(f"✓ File ảnh tồn tại: {exists}")
except Exception as e:
    print(f"✗ Lỗi đường dẫn ảnh: {e}")
    sys.exit(1)

print("\n✅ Tất cả lỗi import/tập tin đã fix!")
