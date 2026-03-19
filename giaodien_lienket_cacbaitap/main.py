import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from giaodien_lienket_cacbaitap.giaodien import Ui_MainWindow

# --- GIẢI QUYẾT VẤN ĐỀ IMPORT TỪ BẤT CỨ ĐÂU ---
# 1. Lấy đường dẫn của file main.py hiện tại
current_dir = os.path.abspath(os.path.dirname(__file__))

# 2. Vòng lặp tự động lùi dần lên trên cho đến khi tìm thấy thư mục gốc "DO_AN_APP_TU_VUNG"
project_root = current_dir
while os.path.basename(project_root) != "DO_AN_APP_TU_VUNG" and project_root != os.path.dirname(project_root):
    project_root = os.path.dirname(project_root)

# 3. Thêm thư mục gốc vào hệ thống (nếu chưa có)
if project_root not in sys.path:
    sys.path.append(project_root)

# 4. Bây giờ bạn có thể import mọi thứ bằng cú pháp: từ_thư_mục.tên_file import tên_class
from giaodien_baitap_sapxep.logic_sapxep import LessonApp
# -------------------------------------------------
from giaodien_baitap_duclo.logic_duclo import FillBlankApp
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnClose.clicked.connect(self.close)
        self.ui.widgetReorder.clicked.connect(self.mo_trang_sap_xep)
        self.ui.widgetFillBlanks.clicked.connect(self.mo_trang_duc_lo)
    def mo_trang_sap_xep(self):
        self.trang_sap_xep_ui = LessonApp()
        self.trang_sap_xep_ui.show()
    def mo_trang_duc_lo(self):
        self.trang_duc_lo_ui = FillBlankApp()
        self.trang_duc_lo_ui.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())