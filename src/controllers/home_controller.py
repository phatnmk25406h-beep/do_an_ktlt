from src.controllers.menu_controller import MainWindow
from src.controllers.vocab_controller import M3M_Vocab_Ext
from src.controllers.account_page_controller import AccountWindow
from src.view.giaodien_homepage_ui import HomePageUI


class DieuPhoiApp:
    def __init__(self, current_user=None):
        self.current_user = current_user or "guest"
        self.trang_chu = HomePageUI()

        for the_chu_de in self.trang_chu.danh_sach_the:
            the_chu_de.clicked.connect(self.xu_ly_click_chu_de)

        self.trang_chu.btn_create_vocab.clicked.connect(self.mo_trang_tao_tu_vung)
        self.trang_chu.progress_label.clicked.connect(self.mo_trang_progress)
        self.trang_chu.logout_btn.clicked.connect(self.xu_ly_dang_xuat)
    def mo_trang_tao_tu_vung(self):
        self.trang_tao_tu = M3M_Vocab_Ext()
        self.trang_tao_tu.show()
        self.trang_chu.hide()

    def mo_trang_progress(self):
        self.trang_progress = AccountWindow(current_user=self.current_user)
        self.trang_progress.show()
        self.trang_chu.hide()

    def xu_ly_click_chu_de(self, ten_chu_de):
        danh_sach_mo_khoa = ["Greetings", "Education", "Travel and Culture"]

        if ten_chu_de in danh_sach_mo_khoa:
            self.menu_bai_tap = MainWindow(ten_chu_de, current_user=self.current_user)
            self.menu_bai_tap.show()
        else:
            print(f"Chủ đề {ten_chu_de} hiện đang bị khóa, hãy cày level thêm!")

    def chay_ung_dung(self):
        self.trang_chu.show()
    def xu_ly_dang_xuat(self):
        """Hàm xử lý khi bấm nút Logout"""
        print("Đang đăng xuất...")
        
        # Import cục bộ ngay trong hàm để tránh lỗi Circular Import
        from src.controllers.login_controller import LoginWindow 
        
        # Khởi tạo và mở lại trang đăng nhập
        self.trang_dang_nhap = LoginWindow()
        self.trang_dang_nhap.show()
        
        # Đóng trang chủ
        self.trang_chu.close()