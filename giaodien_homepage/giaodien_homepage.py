import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QLineEdit,
                             QScrollArea, QFrame, QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

# Class này giúp biến khung viền thành một nút bấm có thể truyền dữ liệu
class ClickableFrame(QFrame):
    clicked = pyqtSignal(str) # Tín hiệu phát ra sẽ mang theo tên của chủ đề

    def __init__(self, topic_name, parent=None):
        super().__init__(parent)
        self.topic_name = topic_name

    def mousePressEvent(self, event):
        self.clicked.emit(self.topic_name)
        super().mousePressEvent(event)

class HomePageUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("M3M English - Home Page")
        self.resize(1200, 900)
        self.setStyleSheet("background-color: white;")

        # 1. TẠO KHUNG CUỘN (Scroll Area)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")

        # 2. TẠO NỘI DUNG CHÍNH (Content Widget)
        self.content_widget = QWidget()
        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Thêm Navbar sát viền trên
        self.main_layout.addWidget(self.create_navbar())

        # 3. THÂN TRANG (Body Widget) - Nơi chứa các nội dung chính
        self.body_widget = QWidget()
        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(100, 40, 100, 50)
        self.body_layout.setSpacing(50)

        # Thêm các thành phần giao diện theo thứ tự từ trên xuống
        self.body_layout.addWidget(self.create_profile_section())
        self.body_layout.addWidget(self.create_learning_path_section())
        self.body_layout.addWidget(self.create_divider())
        self.body_layout.addWidget(self.create_progress_section())
        self.body_layout.addWidget(self.create_divider())
        self.body_layout.addWidget(self.create_vocabulary_section())
        self.body_layout.addWidget(self.create_divider())

        # Phần chủ đề và chân trang
        self.body_layout.addWidget(self.create_available_topics_header())
        self.body_layout.addWidget(self.create_topics_grid())
        self.body_layout.addWidget(self.create_footer())

        self.main_layout.addWidget(self.body_widget)
        self.main_layout.addStretch()

        # Gắn nội dung vào khung cuộn và hiển thị
        self.scroll_area.setWidget(self.content_widget)
        self.setCentralWidget(self.scroll_area)

    def create_divider(self):
        """Tạo đường kẻ ngang mờ để phân chia các khu vực"""
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #F0F0F0; border: none; height: 1px;")
        return divider

    def create_navbar(self):
        """Thanh điều hướng phía trên cùng"""
        navbar = QFrame()
        navbar.setFixedHeight(60)
        navbar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8CC63F, stop:1 #22B573);
            }
        """)
        layout = QHBoxLayout(navbar)
        layout.setContentsMargins(40, 0, 40, 0)

        logo = QLabel("M3MEnglish")
        logo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        logo.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(logo)

        layout.addStretch()

        # Các mục Menu
        menu_items = ["Home", "Topics", "My Vocabulary", "Progress"]
        for item in menu_items:
            btn = QLabel(item)
            btn.setStyleSheet("color: white; background: transparent; font-size: 14px; margin-right: 15px;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)

        # Ô tìm kiếm
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search in site...")
        search_bar.setFixedSize(200, 30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border-radius: 15px;
                padding-left: 15px;
                border: none;
                color: #333;
            }
        """)
        layout.addWidget(search_bar)

        # Ảnh đại diện nhỏ
        mini_avatar = QLabel()
        mini_avatar.setFixedSize(36, 36)
        pixmap=QPixmap("images/avatar.png").scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        mini_avatar.setPixmap(pixmap)
        mini_avatar.setStyleSheet("border-radius: 18px;")
        layout.addWidget(mini_avatar)

        return navbar

    def create_profile_section(self):
        """Khu vực thông tin người dùng"""
        profile_widget = QWidget()
        layout = QHBoxLayout(profile_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        avatar = QLabel()
        avatar.setFixedSize(120, 120)
        pixmap_large = QPixmap("images/avatar.png").scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        avatar.setPixmap(pixmap_large)
        avatar.setStyleSheet("border-radius: 60px;")
        layout.addWidget(avatar)

        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        name_label = QLabel("Yamate")
        name_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))

        level_badge = QLabel("Level 1: Beginner")
        level_badge.setStyleSheet(
            "background-color: #F0F0F0; padding: 4px 8px; border-radius: 4px; ")
        level_badge.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        level_badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

        quote_label = QLabel("Keep learning new words every day!")
        quote_label.setFont(QFont("Arial", 10,QFont.Weight.Bold))
        info_layout.addWidget(name_label)
        info_layout.addWidget(level_badge)
        info_layout.addWidget(quote_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        # Nút Logout và Settings
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        logout_btn = QPushButton("Logout")
        logout_btn.setFixedSize(140, 40)
        logout_btn.setStyleSheet(
            "QPushButton { background-color: white; border: 1px solid black; border-radius: 6px; font-weight: bold; }")

        settings_btn = QPushButton("Settings")
        settings_btn.setFixedSize(140, 40)
        settings_btn.setStyleSheet(
            "QPushButton { background-color: black; color: white; border-radius: 6px; font-weight: bold; }")

        btn_layout.addWidget(logout_btn)
        btn_layout.addWidget(settings_btn)

        layout.addLayout(btn_layout)
        return profile_widget

    def create_learning_path_section(self):
        """Lộ trình học tập với các thẻ A1, B1, C1"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        title = QLabel("Your Learning Path")
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Progress through vocabulary topics.")
        subtitle.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        explore_btn = QPushButton("Explore Topics")
        explore_btn.setFixedSize(160, 45)
        explore_btn.setStyleSheet(
            "QPushButton { background-color: #3CB371; color: white; border-radius: 8px; font-weight: bold; font-size: 14px; }")

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(explore_btn)
        btn_layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(btn_layout)
        layout.addSpacing(20)

        grid = QGridLayout()
        grid.setSpacing(20)

        # Tạo các thẻ bài học
        card_a1 = self.create_course_card(
            "#00C85 green", "Beginner\nA1", "Beginners", "Start your journey",
            "Unlock and learn basic vocabulary.", [("Unlocked", "#00C853"), ("Locked", "#FF5252")], "images/a1.png"
        )
        card_b1 = self.create_course_card(
            "#7C4DFF", "Intermediate\nB1", "Intermediate", "Enhance your skills",
            "Learn more complex words and phrases.", [("Locked", "#FF5252")],"images/b1.png"
        )
        card_c1 = self.create_course_card(
            "#FFD600", "Advanced\nC1", "Advanced", "Master vocabulary",
            "Prepare for advanced English communication.", [("Locked", "#FF5252")], "images/c1.png"
        )

        grid.addWidget(card_a1, 0, 0)
        grid.addWidget(card_b1, 0, 1)
        grid.addWidget(card_c1, 1, 0, 1, 2)

        layout.addLayout(grid)
        return container

    def create_course_card(self, color, level_text, title, subtitle, desc, badges, icon_path):
        """Mẫu thẻ bài học dùng chung"""
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border: 1px solid #E0E0E0; border-radius: 8px; }")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        color_block = QLabel()
        color_block.setFixedSize(100, 100)
        #lấy đường dẫn tuyệt đối để tí nx chuyển trang ko bị lỗi tìm k thấy file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, icon_path)

        try:
            pixmap = QPixmap(img_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
            color_block.setPixmap(pixmap)
        except:
            # Nếu không tìm thấy ảnh, vẫn hiện chữ dự phòng
            color_block.setText(level_text)
            color_block.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Đổi màu chữ dựa trên nền
        t_color = "black" if color == "#FFD600" else "white"
        color_block.setStyleSheet(f"background-color: {color}; color: {t_color}; border-radius: 4px;")
        layout.addWidget(color_block)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        lbl_title = QLabel(title)
        lbl_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        lbl_title.setStyleSheet("border: none;")

        lbl_sub = QLabel(subtitle)
        lbl_sub.setStyleSheet("color: #888; font-size: 12px; border: none;")

        lbl_desc = QLabel(desc)
        lbl_desc.setStyleSheet("color: #333; font-size: 14px; border: none;")

        badge_layout = QHBoxLayout()
        for text, bg in badges:
            b_label = QLabel(text)
            if text == "Unlocked":
                b_label.setStyleSheet(
                    f"background-color: {bg}; color: black; padding: 3px 8px; border-radius: 4px; font-size: 11px; border: none; font-weight: bold;")
            else:
                b_label.setStyleSheet(
                    f"background-color: {bg}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; border: none;")
            badge_layout.addWidget(b_label)
        badge_layout.addStretch()

        info_layout.addWidget(lbl_title)
        info_layout.addWidget(lbl_sub)
        info_layout.addWidget(lbl_desc)
        info_layout.addLayout(badge_layout)
        info_layout.addStretch()

        layout.addLayout(info_layout)
        return card

    def create_progress_section(self):
        """Phần biểu đồ và thống kê tiến độ"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(40)

        mascot = QLabel()
        mascot.setFixedSize(150, 150)
        pixmap_dino = QPixmap("images/khunglong_streak.png").scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio,
                                                             Qt.TransformationMode.SmoothTransformation)
        mascot.setPixmap(pixmap_dino)
        layout.addWidget(mascot)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Learning Progress\nSummary")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        subtitle = QLabel("Track your daily and overall progress.")
        subtitle.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        # Thẻ Streak
        card_streak = QFrame()
        card_streak.setStyleSheet("QFrame { border: 1px solid #E0E0E0; border-radius: 8px; }"
                                  "QLabel { border: none;}")
        card_streak.setFixedSize(150, 100)
        lay_s = QVBoxLayout(card_streak)
        lay_s.addWidget(QLabel("Daily Streak"))
        val_s = QLabel("5 Days")
        val_s.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        lay_s.addWidget(val_s)
        day_plus=QLabel("+2 Days")
        day_plus.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        lay_s.addWidget(day_plus)

        # Thẻ Words
        card_words = QFrame()
        card_words.setStyleSheet("QFrame { border: 1px solid #E0E0E0; border-radius: 8px; } QLabel {border:none;}")
        card_words.setFixedSize(170, 100)
        lay_w = QVBoxLayout(card_words)
        lay_w.addWidget(QLabel("Total Words"))
        val_w = QLabel("150 Words")
        val_w.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        lay_w.addWidget(val_w)
        lay_w.addStretch()

        stats_layout.addWidget(card_streak)
        stats_layout.addWidget(card_words)
        stats_layout.addStretch()

        info_layout.addWidget(title)
        info_layout.addWidget(subtitle)
        info_layout.addSpacing(15)
        info_layout.addLayout(stats_layout)
        layout.addWidget(info_widget)

        # Biểu đồ cột
        chart_card = QFrame()
        chart_card.setStyleSheet("QFrame { border: 1px solid #E0E0E0; border-radius: 8px; }"
                                 "QLabel {border:none;}")
        chart_card.setMinimumWidth(350)
        chart_lay = QVBoxLayout(chart_card)
        chart_lay.addWidget(QLabel("Words Memorization Progress"))

        bars_widget = QWidget()
        bars_lay = QHBoxLayout(bars_widget)
        bars_lay.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # 3. ĐÃ THÊM DỮ LIỆU NGÀY THÁNG VÀO (Chiều cao, Màu sắc, Ngày)
        bar_data = [
            (100, "#FFD700", "10/3"),
            (70, "#2ECA71", "11/3"),
            (50, "#FF8C00", "12/3"),
            (80, "#1E90FF", "13/3"),
            (60, "#808080", "14/3"),
            (110, "#808080", "15/3"),
            (70, "#808080", "16/3")
        ]

        for h, c, date_str in bar_data:
            # Tạo một cột dọc cho mỗi thanh bar
            col_lay = QVBoxLayout()

            # Cục gạch tàng hình (Stretch) đè từ trên xuống để cột nằm sát đáy
            col_lay.addStretch()

            # Vẽ thanh màu
            bar = QFrame()
            bar.setFixedSize(25, h)
            bar.setStyleSheet(f"background-color: {c}; border-radius: 4px; border: none;")
            col_lay.addWidget(bar, alignment=Qt.AlignmentFlag.AlignHCenter)

            # Viết ngày tháng bên dưới
            lbl_date = QLabel(date_str)
            lbl_date.setStyleSheet("color: #888; font-size: 11px; border: none;")
            col_lay.addWidget(lbl_date, alignment=Qt.AlignmentFlag.AlignHCenter)

            # Nhét cột dọc này vào hàng ngang của biểu đồ
            bars_lay.addLayout(col_lay)

        chart_lay.addWidget(bars_widget)
        layout.addWidget(chart_card)
        return container

    def create_vocabulary_section(self):
        """Phần danh sách từ vựng cá nhân"""
        container = QWidget()
        layout = QHBoxLayout(container)

        l_layout = QVBoxLayout()
        title = QLabel("My Vocabulary List")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        btn = QPushButton("Create New Vocabulary")
        btn.setFixedSize(200, 45)
        btn.setStyleSheet("background-color: #3CB371; color: white; border-radius: 8px; font-weight: bold;")

        l_layout.addWidget(title)
        l_layout.addWidget(btn)
        layout.addLayout(l_layout)
        layout.addStretch()

        i_card = QFrame()
        i_card.setMinimumWidth(400)
        i_card.setStyleSheet("QFrame { background-color: white; border-bottom: 1px solid #E0E0E0; } QLabel { border: none; }")
        i_lay = QHBoxLayout(i_card)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap_voca = QPixmap("images/Flashcard.png").scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon.setPixmap(pixmap_voca)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        i_lay.addWidget(icon)

        m_lay = QVBoxLayout()
        m_lay.addWidget(QLabel("Study Flashcard"))
        m_lay.addWidget(QLabel("Vocabulary Word"))
        i_lay.addLayout(m_lay)
        i_lay.addStretch()
        i_lay.addWidget(QLabel("e.g., 'Apple' -\n'Manzana'"))

        layout.addWidget(i_card)
        return container

    def create_available_topics_header(self):
        """Tiêu đề phần Available Topics"""
        container = QWidget()
        layout = QVBoxLayout(container)
        title = QLabel("Available Topics")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        sub = QLabel("Unlock new topics to expand your vocabulary.")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub, alignment=Qt.AlignmentFlag.AlignCenter)
        return container

    def create_topics_grid(self):
        """Lưới các chủ đề khóa học"""
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(30)
        #Danh sách lưu lại các thẻ để file lienket.py dễ dàng bắt sự kiện
        self.danh_sach_the = []
        topics = [
            ("Greetings", "Unlocks at Level 1", "Unlocked", "#3CB371", "images/greet.png"),
            ("Culture", "Unlocks at Level 1", "Unlocked", "#3CB371", "images/culture.png"),
            ("Travel", "Unlocks at Level 1", "Unlocked", "#3CB371", "images/travel.png"),
            ("Work", "Locked", "Locked", "#FF5252", "images/work.png"),
            ("Health", "Locked", "Locked", "#FF5252", "images/health.png")
        ]

        row, col = 0, 0
        for t, s, st, c,k in topics:
            card = self.create_topic_card(t, s, st, c, k)

            # MỚI: Nếu thẻ "Unlocked" thì hiện con trỏ bàn tay, "Locked" thì hiện dấu cấm
            if st == "Unlocked":
                card.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                card.setCursor(Qt.CursorShape.ForbiddenCursor)

            grid.addWidget(card, row, col)
            self.danh_sach_the.append(card)  # Lưu thẻ vào danh sách

            col += 1
            if col > 2:
                col = 0
                row += 1
        return grid_container

    def create_topic_card(self, title, sub, status, s_color, topic_icon):
        """Thẻ chủ đề riêng lẻ"""
        card = ClickableFrame(title)
        card.setStyleSheet(
            "QFrame { background-color: white; border: 1px solid #E0E0E0; border-radius: 12px; } QLabel { border: none; }")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 15)
        layout.setSpacing(0)

        img_label = QLabel()
        img_label.setObjectName("topic_img")
        img_label.setFixedHeight(250)
        img_label.setStyleSheet(f"""
                    #topic_img {{
                        border-image: url("{topic_icon}") 0 0 0 0 stretch stretch;
                        border-top-left-radius: 12px;
                        border-top-right-radius: 12px;
                        border-bottom-left-radius: 0px;
                        border-bottom-right-radius: 0px;
                    }}
                """)


            # Nhãn Unlocked / Locked
        badge = QLabel(status, img_label)
        badge.move(10, 10)
        badge.setStyleSheet(
            f"background-color: {s_color}; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 11px;")

        # ==========================================
        # 2. KHU VỰC CHỮ (Hộp chứa giúp tạo khoảng cách)
        # ==========================================
        txt_container = QWidget()
        txt_layout = QVBoxLayout(txt_container)
        txt_layout.setContentsMargins(15, 15, 15, 0)  # Cố ý thêm lề trên 15px để cách ảnh ra
        txt_layout.setSpacing(5)

        lbl_title = QLabel(title)
        lbl_title.setFont(QFont("Arial", 12))
        lbl_title.setStyleSheet("color: #888;")

        lbl_sub = QLabel(sub)
        lbl_sub.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        lbl_sub.setStyleSheet("color: #333;")

        txt_layout.addWidget(lbl_title)
        txt_layout.addWidget(lbl_sub)

        # Ráp 2 khối (Ảnh + Hộp chữ) vào thẻ
        layout.addWidget(img_label)
        layout.addWidget(txt_container)
        layout.addStretch()

        return card

    def create_footer(self):
        """Phần chân trang cuối cùng"""
        footer = QFrame()
        footer.setFixedHeight(200)
        footer.setStyleSheet("background-color: #EEEEEE; border-radius: 10px;")
        layout = QVBoxLayout(footer)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        txt = QLabel("Join our community to learn and share together.")
        txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(txt)
        layout.addWidget(QLabel("● ○ ○"), alignment=Qt.AlignmentFlag.AlignCenter)
        return footer


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePageUI()
    window.show()
    sys.exit(app.exec())