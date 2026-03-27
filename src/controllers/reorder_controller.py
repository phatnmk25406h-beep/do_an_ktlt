import os
from PyQt6.QtWidgets import QPushButton

from src.models.reorder_model import LessonManager
from src.view.giaodien_sapxep import LessonUI
import time
from src.models.user_model import add_learning_time

class LessonApp(LessonUI):
    def __init__(self, topic_name=None):
        super().__init__()
        self.topic_name = topic_name
        self.current_correct_answer = ""
        self.selected_words = []
        # --- BẮT ĐẦU BẤM GIỜ ---
        self.start_time = time.time()
        self.current_user = "phat" # Tạm fix cứng để test
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        excel_path = os.path.join(base_dir, "data", "sapxeptu.xlsx")
        self.manager = LessonManager(excel_path)

        self.close_btn.clicked.connect(self.close)
        self.check_button.clicked.connect(self.check_answer)
        self.continue_btn.clicked.connect(self.reset_for_next_question)

        self.load_new_question()

    def load_new_question(self):
        data = self.manager.get_question(self.topic_name)
        if not data:
            self.vietnamese_text.setText("Bạn đã hoàn thành bài học!")
            return

        self.vietnamese_text.setText(data["vi"])
        self.current_correct_answer = data["en_correct"]

        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for word in data["word_bank"]:
            word_btn = QPushButton(word)
            word_btn.setStyleSheet(
                """
                QPushButton { background-color: white; border: 1px solid #333; border-radius: 20px; padding: 10px 20px; font-size: 14px; color: #333; }
                QPushButton:disabled { background-color: #E8E8E8; color: #999; }
                """
            )
            word_btn.clicked.connect(lambda checked, w=word, btn=word_btn: self.add_word_to_answer(w, btn))
            self.words_layout.addWidget(word_btn)

        self.check_button.setEnabled(False)

    def add_word_to_answer(self, word, button):
        button.setEnabled(False)

        word_chip = QPushButton(word)
        word_chip.original_button = button
        word_chip.setStyleSheet(
            """
            QPushButton { background-color: white; border: 1px solid #333; border-radius: 15px; padding: 8px 16px; font-size: 14px; color: #333; }
            QPushButton:hover { background-color: #FFE8E8; border-color: #FF4444; }
            """
        )
        word_chip.clicked.connect(lambda: self.remove_word_from_answer(word, word_chip, button))

        self.selected_words.append(word)
        self.selected_words_layout.addWidget(word_chip)
        self.check_button.setEnabled(len(self.selected_words) > 0)

    def remove_word_from_answer(self, word, word_chip, original_button):
        if word in self.selected_words:
            self.selected_words.remove(word)

        word_chip.deleteLater()
        original_button.setEnabled(True)
        self.check_button.setEnabled(len(self.selected_words) > 0)

    def reset_for_next_question(self):
        self.footer_stack.setCurrentIndex(0)

        if getattr(self, "is_correct", False):
            current_vi_text = self.vietnamese_text.text()
            self.manager.remove_question(current_vi_text)

            while self.selected_words_layout.count():
                item = self.selected_words_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            self.selected_words.clear()
            self.check_button.setEnabled(False)
            self.load_new_question()
        else:
            while self.selected_words_layout.count():
                item = self.selected_words_layout.takeAt(0)
                word_chip = item.widget()
                if word_chip:
                    if hasattr(word_chip, "original_button"):
                        word_chip.original_button.setEnabled(True)
                    word_chip.deleteLater()

            self.selected_words.clear()
            self.check_button.setEnabled(False)

    def check_answer(self):
        user_answer = " ".join(self.selected_words)
        correct_answer = self.current_correct_answer.strip()

        if user_answer.strip() == correct_answer:
            self.is_correct = True
            self.result_widget.setStyleSheet("background-color: #D7FFB8; border-top: 2px solid #58A700;")
            self.result_msg.setText("Correct!")
            self.result_msg.setStyleSheet("color: #58A700; border: none;")
            self.result_icon.setText("✔️")
            self.continue_btn.setStyleSheet("background-color: #58A700; border-radius: 25px; color: white; font-weight: bold;")
        else:
            self.is_correct = False
            self.result_widget.setStyleSheet("background-color: #FFDFE0; border-top: 2px solid #EA2B2B;")
            self.result_msg.setText(f"Correct solution:\n{correct_answer}")
            self.result_msg.setStyleSheet("color: #EA2B2B; border: none;")
            self.result_icon.setText("❌")
            self.continue_btn.setStyleSheet("background-color: #EA2B2B; border-radius: 25px; color: white; font-weight: bold;")

        self.footer_stack.setCurrentIndex(1)
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