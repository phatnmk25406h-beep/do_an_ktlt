import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect,
                             QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class FillBlankUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Khởi tạo toàn bộ giao diện tĩnh"""
        self.setWindowTitle("M3M English - Fill in the blank")
        self.showMaximized()
        self.setStyleSheet("background-color: #FAFAFA;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(40, 30, 40, 30)

        # 1. Header
        main_layout.addWidget(self.create_header())
        main_layout.addStretch(1)

        # 2. Main Card
        card_widget = self.create_main_card()
        card_h_layout = QHBoxLayout()
        card_h_layout.addStretch(1)
        card_h_layout.addWidget(card_widget, 4)
        card_h_layout.addStretch(1)

        main_layout.addLayout(card_h_layout)
        main_layout.addStretch(1)

    def create_header(self):
        header_widget = QWidget()
        layout = QHBoxLayout(header_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self.flag_label = QLabel()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "trang_tri", "images", "united_kingdom.png")
        try:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaledToHeight(35, Qt.TransformationMode.SmoothTransformation)
                self.flag_label.setPixmap(scaled_pixmap)
            else:
                self.flag_label.setText("🇬🇧")
        except:
            self.flag_label.setText("🇬🇧")

        layout.addWidget(self.flag_label)

        title_label = QLabel(" Topic: Travel & Culture")
        title_label.setFont(QFont("Arial Black", 24, QFont.Weight.Black))
        title_label.setStyleSheet("color: black; background-color: transparent;")
        layout.addWidget(title_label)

        layout.addStretch()

        self.close_btn = QPushButton("X")
        self.close_btn.setFixedSize(40, 40)
        self.close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #333; font-size: 28px; border: none; }
            QPushButton:hover { color: #FF4444; }
        """)
        layout.addWidget(self.close_btn)

        return header_widget

    def create_main_card(self):
        card = QFrame()
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        card.setMinimumWidth(600)
        card.setStyleSheet("QFrame { background-color: white; border-radius: 8px; }")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(Qt.GlobalColor.lightGray)
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 60, 50, 40)

        # --- KHU VỰC CÂU HỎI ---
        sentence_layout = QHBoxLayout()
        sentence_layout.setSpacing(10)

        self.part1 = QLabel()
        self.part1.setFont(QFont("Arial", 18))
        self.part1.setStyleSheet("color : black;")
        self.part1.setWordWrap(True)
        self.part1.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.blank_label = QLabel()
        self.blank_label.setMinimumWidth(120)
        self.blank_label.setFixedHeight(35)
        self.blank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blank_label.setFont(QFont("Arial", 16))
        self.blank_label.setStyleSheet("background-color: #F0F0F0; border: 1px solid #E0E0E0; color: black;")

        self.part2 = QLabel()
        self.part2.setFont(QFont("Arial", 18))
        self.part2.setStyleSheet("color : black;")
        self.part2.setWordWrap(True)
        self.part2.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        sentence_layout.addWidget(self.part1)
        sentence_layout.addWidget(self.blank_label)
        sentence_layout.addWidget(self.part2)
        card_layout.addLayout(sentence_layout)

        card_layout.addSpacing(10)

        self.vi_trans = QLabel()
        self.vi_trans.setFont(QFont("Arial", 14))
        self.vi_trans.setStyleSheet("color: #333;")
        self.vi_trans.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vi_trans.setWordWrap(True)
        card_layout.addWidget(self.vi_trans)

        card_layout.addSpacing(20)

        # --- WORD BANK ---
        self.words_layout = QGridLayout()
        self.words_layout.setSpacing(20)
        words_widget = QWidget()
        words_widget.setLayout(self.words_layout)
        card_layout.addWidget(words_widget)

        card_layout.addSpacing(20)

        # --- NEXT BTN ---
        next_layout = QHBoxLayout()
        next_layout.addStretch()
        self.next_btn = QPushButton("NEXT")
        self.next_btn.setFixedSize(140, 50)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setStyleSheet("""
            QPushButton { background-color: #3CD070; color: white; border-radius: 6px; font-weight: bold; font-size: 16px; }
            QPushButton:hover { background-color: #35B862; }
            QPushButton:disabled { background-color: #A0E8B9; }
        """)
        next_layout.addWidget(self.next_btn)
        card_layout.addLayout(next_layout)

        return card