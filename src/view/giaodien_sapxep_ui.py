import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton,
                             QFrame, QGraphicsDropShadowEffect,
                             QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class LessonUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("M3M English - Lesson")
        self.showMaximized()
        self.setStyleSheet("background-color: #F5F5F5;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        main_layout.addWidget(self.create_top_bar())
        main_layout.addWidget(self.create_content_area())

        # Ngăn kéo Footer
        self.footer_stack = QStackedWidget()
        self.footer_stack.addWidget(self.create_bottom_buttons())  # Trang 0
        self.footer_stack.addWidget(self.create_result_panel())  # Trang 1

        main_layout.addWidget(self.footer_stack)
        self.footer_stack.setCurrentIndex(0)

    def create_top_bar(self):
        top_widget = QWidget()
        layout = QHBoxLayout(top_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        question_label = QLabel("Question 5")
        question_label.setStyleSheet("color: #999; font-size: 14px;")
        layout.addWidget(question_label)
        layout.addStretch()

        question_right = QLabel("Question 5")
        question_right.setStyleSheet("color: #999; font-size: 14px;")
        layout.addWidget(question_right)

        return top_widget

    def create_content_area(self):
        content_widget = QFrame()
        content_widget.setStyleSheet("background-color: white; border-radius: 15px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(Qt.GlobalColor.gray)
        content_widget.setGraphicsEffect(shadow)

        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(15)

        # Header (Close btn + Progress bar)
        header_layout = QHBoxLayout()
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; color: #999; font-size: 24px; font-weight: bold; }
            QPushButton:hover { color: #333; }
        """)
        header_layout.addWidget(self.close_btn)

        progress_container = QWidget()
        progress_layout = QHBoxLayout(progress_container)
        progress_layout.setContentsMargins(10, 0, 10, 0)
        progress_layout.setSpacing(5)

        progress_green = QFrame()
        progress_green.setFixedHeight(8)
        progress_green.setStyleSheet("background-color: #7BC342; border-radius: 4px;")

        progress_gray = QFrame()
        progress_gray.setFixedHeight(8)
        progress_gray.setStyleSheet("background-color: #F0F0F0; border-radius: 4px;")

        progress_layout.addWidget(progress_green, 2)
        progress_layout.addWidget(progress_gray, 3)

        header_layout.addWidget(progress_container)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        layout.addSpacing(15)

        # Title
        title_label = QLabel("Write this in English")
        title_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #333;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Mascot + Bubble
        mascot_container = QWidget()
        mascot_layout = QHBoxLayout(mascot_container)
        mascot_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mascot_layout.setSpacing(20)

        mascot_label = QLabel()
        mascot_label.setFixedSize(120, 120)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "trang_tri", "images", "dinohocbai.png")
        try:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                mascot_label.setPixmap(scaled_pixmap)
            else:
                mascot_label.setText("🦕")
                mascot_label.setFont(QFont("Arial", 80))
        except:
            mascot_label.setText("🦕")
            mascot_label.setFont(QFont("Arial", 80))

        mascot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        speech_bubble = QFrame()
        speech_bubble.setMinimumWidth(400)
        speech_bubble.setStyleSheet("background-color: white; border-radius: 20px; border: 1px solid #000000;")

        speech_layout = QVBoxLayout(speech_bubble)
        speech_layout.setContentsMargins(20, 15, 20, 15)

        self.vietnamese_text = QLabel()
        self.vietnamese_text.setFont(QFont("Arial", 16))
        self.vietnamese_text.setWordWrap(True)
        self.vietnamese_text.setStyleSheet("color: #333; background-color: transparent; border: none;")
        self.vietnamese_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        speech_layout.addWidget(self.vietnamese_text)

        mascot_layout.addWidget(mascot_label, 0)
        mascot_layout.addWidget(speech_bubble, 1)
        mascot_layout.addStretch()

        layout.addWidget(mascot_container)
        layout.addSpacing(10)

        # Khu vực thả câu trả lời (Answer Area)
        answer_container = QWidget()
        answer_v_layout = QVBoxLayout(answer_container)
        answer_v_layout.setContentsMargins(0, 5, 0, 5)
        answer_v_layout.setSpacing(5)

        top_line = QFrame()
        top_line.setFixedHeight(1)
        top_line.setStyleSheet("background-color: #DCDCDC; border: none;")

        self.selected_words_widget = QWidget()
        self.selected_words_widget.setMinimumHeight(60)
        self.selected_words_layout = QHBoxLayout(self.selected_words_widget)
        self.selected_words_layout.setContentsMargins(0, 0, 0, 0)
        self.selected_words_layout.setSpacing(8)
        self.selected_words_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bottom_line = QFrame()
        bottom_line.setFixedHeight(1)
        bottom_line.setStyleSheet("background-color: #DCDCDC; border: none;")

        answer_v_layout.addWidget(top_line)
        answer_v_layout.addWidget(self.selected_words_widget)
        answer_v_layout.addWidget(bottom_line)
        layout.addWidget(answer_container)

        # Word bank (Khởi tạo vùng trống)
        word_bank_label = QLabel("Word bank:")
        word_bank_label.setStyleSheet("color: #999; font-size: 12px;")
        layout.addWidget(word_bank_label)

        words_widget = QWidget()
        self.words_layout = QHBoxLayout(words_widget)
        self.words_layout.setSpacing(15)
        self.words_layout.setContentsMargins(0, 10, 0, 10)
        self.words_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(words_widget)
        layout.addStretch()

        return content_widget

    def create_bottom_buttons(self):
        bottom_widget = QWidget()
        layout = QHBoxLayout(bottom_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.skip_btn = QPushButton("SKIP")
        self.skip_btn.setFixedSize(150, 50)
        self.skip_btn.setStyleSheet("""
            QPushButton { background-color: white; border: 2px solid #E0E0E0; border-radius: 25px; font-size: 14px; font-weight: bold; color: #999; }
            QPushButton:hover { border-color: #BBB; color: #666; }
        """)
        layout.addWidget(self.skip_btn)
        layout.addStretch()

        self.check_button = QPushButton("CHECK")
        self.check_button.setFixedSize(150, 50)
        self.check_button.setStyleSheet("""
            QPushButton { background-color: #E0E0E0; border: none; border-radius: 25px; font-size: 14px; font-weight: bold; color: #999; }
            QPushButton:enabled { background-color: #7BC342; color: white; }
            QPushButton:enabled:hover { background-color: #6BA332; }
        """)
        self.check_button.setEnabled(False)
        layout.addWidget(self.check_button)

        return bottom_widget

    def create_result_panel(self):
        panel = QFrame()
        self.result_widget = panel
        panel.setFixedHeight(150)
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(50, 20, 50, 20)

        self.result_icon = QLabel()
        self.result_icon.setFixedSize(60, 60)
        self.result_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_icon.setStyleSheet("font-size: 30px; background-color: white; border-radius: 30px;")
        layout.addWidget(self.result_icon)

        self.result_msg = QLabel()
        self.result_msg.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.result_msg.setWordWrap(True)
        layout.addWidget(self.result_msg)

        layout.addStretch()

        self.continue_btn = QPushButton("CONTINUE")
        self.continue_btn.setFixedSize(180, 50)
        self.continue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.continue_btn.setStyleSheet(
            "border-radius: 25px; color: white; font-weight: bold; font-size: 16px; border: none;")
        layout.addWidget(self.continue_btn)

        return panel