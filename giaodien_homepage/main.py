import sys
import os
from PyQt6.QtWidgets import QApplication

# --- CƠ CHẾ TỰ TÌM THƯ MỤC GỐC "DO_AN_APP_TU_VUNG" BẤT BẠI ---
current_dir = os.path.abspath(os.path.dirname(__file__))
project_root = current_dir
while os.path.basename(project_root) != "DO_AN_APP_TU_VUNG" and project_root != os.path.dirname(project_root):
    project_root = os.path.dirname(project_root)
if project_root not in sys.path:
    sys.path.append(project_root)

# --- IMPORT CÁC TRANG CẦN LIÊN KẾT ---
# LƯU Ý: Bạn cần chỉnh lại tên thư mục import cho đúng với máy của bạn.
# Ví dụ: from tên_thư_mục.tên_file import tên_class
from giaodien_homepage import HomePageUI
from giaodien_lienket_cacbaitap.main import MainWindow


class DieuPhoiApp:
    def __init__(self):
        # 1. Khởi tạo giao diện Trang chủ
        self.trang_chu = HomePageUI()

        # 2. Dùng vòng lặp quét qua tất cả các thẻ Topic để "bắt" tín hiệu click
        for the_chu_de in self.trang_chu.danh_sach_the:
            the_chu_de.clicked.connect(self.xu_ly_click_chu_de)

    def xu_ly_click_chu_de(self, ten_chu_de):
        """Hàm này sẽ chạy khi bạn bấm vào bất kỳ thẻ Topic nào"""

        # Logic: Chỉ mở trang mới nếu bấm vào 3 thẻ đã mở khóa
        danh_sach_mo_khoa = ["Greetings", "Culture", "Travel"]

        if ten_chu_de in danh_sach_mo_khoa:
            print(f"Đang mở menu bài tập cho chủ đề: {ten_chu_de}")

            # Khởi tạo và hiển thị trang Menu (ảnh 2)
            self.menu_bai_tap = MainWindow()
            self.menu_bai_tap.show()

            # Nếu bạn muốn khi mở bài học lên thì Trang chủ tự động ẩn đi, hãy bỏ dấu # ở dòng dưới:
            # self.trang_chu.hide()
        else:
            print(f"Chủ đề {ten_chu_de} hiện đang bị khóa, hãy cày level thêm!")

    def chay_ung_dung(self):
        # Bắt đầu hiển thị trang chủ
        self.trang_chu.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    phan_mem = DieuPhoiApp()
    phan_mem.chay_ung_dung()
    sys.exit(app.exec())