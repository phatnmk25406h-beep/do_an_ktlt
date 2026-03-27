from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton

from src.view.giaodien_sapxep_ui import LessonUI


class LessonRender(LessonUI):
    def __init__(self):
        super().__init__()

    def bind_handlers(self, on_close, on_check, on_continue):
        self.close_btn.clicked.connect(on_close)
        self.check_button.clicked.connect(on_check)
        self.continue_btn.clicked.connect(on_continue)

    def set_question_text(self, vi_text):
        self.vietnamese_text.setText(vi_text)

    def show_completed(self):
        self.vietnamese_text.setText("Ban da hoan thanh bai hoc!")

    def clear_word_bank(self):
        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def render_word_bank(self, words, on_word_selected):
        self.clear_word_bank()
        for word in words:
            word_btn = QPushButton(word)
            word_btn.setStyleSheet(
                """
                QPushButton { background-color: white; border: 1px solid #333; border-radius: 20px; padding: 10px 20px; font-size: 14px; color: #333; }
                QPushButton:disabled { background-color: #E8E8E8; color: #999; }
                """
            )
            word_btn.clicked.connect(lambda checked, w=word, btn=word_btn: on_word_selected(w, btn))
            self.words_layout.addWidget(word_btn)

    def add_selected_chip(self, word, original_button, on_chip_remove):
        original_button.setEnabled(False)
        chip = QPushButton(word)
        chip.original_button = original_button
        chip.setStyleSheet(
            """
            QPushButton { background-color: white; border: 1px solid #333; border-radius: 15px; padding: 8px 16px; font-size: 14px; color: #333; }
            QPushButton:hover { background-color: #FFE8E8; border-color: #FF4444; }
            """
        )
        chip.clicked.connect(lambda: on_chip_remove(word, chip, original_button))
        self.selected_words_layout.addWidget(chip)

    def clear_selected_words(self, restore_original_buttons):
        while self.selected_words_layout.count():
            item = self.selected_words_layout.takeAt(0)
            chip = item.widget()
            if chip:
                if restore_original_buttons and hasattr(chip, "original_button"):
                    chip.original_button.setEnabled(True)
                chip.deleteLater()

    def set_check_enabled(self, enabled):
        self.check_button.setEnabled(enabled)

    def show_input_footer(self):
        self.footer_stack.setCurrentIndex(0)

    def show_result(self, is_correct, correct_answer):
        if is_correct:
            self.result_widget.setStyleSheet("background-color: #D7FFB8; border-top: 2px solid #58A700;")
            self.result_msg.setText("Correct!")
            self.result_msg.setStyleSheet("color: #58A700; border: none;")
            self.result_icon.setText("OK")
            self.continue_btn.setStyleSheet("background-color: #58A700; border-radius: 25px; color: white; font-weight: bold;")
        else:
            self.result_widget.setStyleSheet("background-color: #FFDFE0; border-top: 2px solid #EA2B2B;")
            self.result_msg.setText(f"Correct solution:\n{correct_answer}")
            self.result_msg.setStyleSheet("color: #EA2B2B; border: none;")
            self.result_icon.setText("X")
            self.continue_btn.setStyleSheet("background-color: #EA2B2B; border-radius: 25px; color: white; font-weight: bold;")
        self.footer_stack.setCurrentIndex(1)
