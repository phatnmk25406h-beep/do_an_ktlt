import os
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from src.models.fill_blank_model import FillBlankManager
from src.view.giaodien_duclo import FillBlankUI
import time
from src.models.user_model import add_learning_time

class FillBlankApp(FillBlankUI):
    def __init__(self, topic_name=None):
        super().__init__()
        self.topic_name = topic_name
        if self.topic_name:
            self.title_label.setText(self.topic_name)
        self.state = "playing"
        self.current_selected_button = None
        self.current_correct_word = ""
        # --- BẮT ĐẦU BẤM GIỜ ---
        self.start_time = time.time()
        self.current_user = "phat" # Tạm fix cứng để test
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        excel_path = os.path.join(base_dir, "data", "fill_blank.xlsx")
        self.manager = FillBlankManager(excel_path)

        self.next_btn.clicked.connect(self.handle_next_click)
        self.next_btn.setEnabled(False)
        self.close_btn.clicked.connect(self.close)

        self.load_new_question()

    def load_new_question(self):
        self.reset_blank_ui()
        data = self.manager.get_question(self.topic_name)

        if not data:
            self.part1.setText("")
            self.part2.setText("")
            self.vi_trans.setText("🎉 Chúc mừng! Bạn đã hoàn thành bài học.")
            self.next_btn.setEnabled(False)
            self.clear_word_bank()
            return

        self.part1.setText(data["part1"])
        self.part2.setText(data["part2"])
        self.vi_trans.setText(data["vi_trans"])
        self.current_correct_word = data["blank_correct"]

        self.clear_word_bank()
        self.create_word_buttons(data["word_bank"])

    def create_word_buttons(self, words):
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        for index, word in enumerate(words):
            btn = QPushButton(word)
            btn.setFixedHeight(50)
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet(
                """
                QPushButton { background-color: #E2E2E2; border: none; color: black; padding: 10px 20px; border-radius: 8px; }
                QPushButton:hover { background-color: #D0D0D0; }
                QPushButton:disabled { color: transparent; background-color: #F0F0F0; }
                """
            )
            btn.clicked.connect(lambda checked, w=word, b=btn: self.select_word_logic(w, b))

            row, col = positions[index]
            self.words_layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

    def select_word_logic(self, word, button):
        if self.state != "playing":
            return

        if self.current_selected_button:
            self.current_selected_button.setEnabled(True)
            self.current_selected_button.setStyleSheet(
                """
                QPushButton { background-color: #E2E2E2; border: none; padding: 12px 20px; color: black; border-radius: 8px; }
                QPushButton:hover { background-color: #D0D0D0; }
                """
            )

        self.blank_label.setText(word)
        button.setEnabled(False)
        button.setStyleSheet("background-color: #F0F0F0; color: transparent; border: none; border-radius: 8px;")

        self.current_selected_button = button
        self.next_btn.setEnabled(True)

    def handle_next_click(self):
        if self.state == "playing":
            if self.blank_label.text() == self.current_correct_word:
                self.blank_label.setStyleSheet("background-color: #3CD070; color: white; font-weight: bold; border-radius: 4px;")
                self.state = "correct"
            else:
                self.blank_label.setStyleSheet("background-color: #FF4444; color: white; font-weight: bold; border-radius: 4px;")
                self.state = "wrong"
        elif self.state == "correct":
            self.manager.remove_current_question()
            self.load_new_question()
        elif self.state == "wrong":
            self.reset_blank_ui()

    def reset_blank_ui(self):
        self.blank_label.setText("")
        self.blank_label.setStyleSheet("background-color: #F0F0F0; border: 1px solid #E0E0E0; color: black;")
        if self.current_selected_button:
            self.current_selected_button.setEnabled(True)
            self.current_selected_button.setStyleSheet(
                """
                QPushButton { background-color: #E2E2E2; border: none; padding: 10px 20px; color: black; border-radius: 8px; }
                QPushButton:hover { background-color: #D0D0D0; }
                """
            )
            self.current_selected_button = None
        self.next_btn.setEnabled(False)
        self.state = "playing"

    def clear_word_bank(self):
        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    def closeEvent(self, event):
        """Hàm này tự động chạy khi người dùng tắt cửa sổ bài học"""
        # 1. Tính số phút đã học
        minutes_spent = (time.time() - self.start_time) / 60.0
        
        # 2. Lưu vào Excel (Chỉ lưu nếu học trên 0.1 phút ~ 6 giây để tránh spam rác)
        if minutes_spent > 0.1:
            success = add_learning_time(self.current_user, minutes_spent)
            if success:
                print(f"Đã lưu thành công {minutes_spent:.2f} phút cho user '{self.current_user}'")
            else:
                print("Lỗi: Không thể lưu thời gian học!")
                
        # 3. Cho phép cửa sổ tắt bình thường
        event.accept()