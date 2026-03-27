from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton

from src.view.giaodien_duclo_ui import FillBlankUI


class FillBlankRender(FillBlankUI):
    def __init__(self):
        super().__init__()

    def bind_handlers(self, on_next, on_close):
        self.next_btn.clicked.connect(on_next)
        self.close_btn.clicked.connect(on_close)

    def set_topic_title(self, topic_name):
        if topic_name:
            self.title_label.setText(topic_name)

    def render_question(self, part1, part2, vi_trans):
        self.part1.setText(part1)
        self.part2.setText(part2)
        self.vi_trans.setText(vi_trans)

    def show_completed(self):
        self.part1.setText("")
        self.part2.setText("")
        self.vi_trans.setText("Chuc mung! Ban da hoan thanh bai hoc.")
        self.set_next_enabled(False)
        self.clear_word_bank()

    def set_next_enabled(self, enabled):
        self.next_btn.setEnabled(enabled)

    def clear_word_bank(self):
        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def render_word_bank(self, words, on_word_selected):
        self.clear_word_bank()
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
            btn.clicked.connect(lambda checked, w=word, b=btn: on_word_selected(w, b))
            row, col = positions[index]
            self.words_layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

    def set_blank_text(self, text):
        self.blank_label.setText(text)

    def set_blank_correct_style(self):
        self.blank_label.setStyleSheet("background-color: #3CD070; color: white; font-weight: bold; border-radius: 4px;")

    def set_blank_wrong_style(self):
        self.blank_label.setStyleSheet("background-color: #FF4444; color: white; font-weight: bold; border-radius: 4px;")

    def reset_blank_style(self):
        self.blank_label.setText("")
        self.blank_label.setStyleSheet("background-color: #F0F0F0; border: 1px solid #E0E0E0; color: black;")

    def mark_word_selected(self, button):
        button.setEnabled(False)
        button.setStyleSheet("background-color: #F0F0F0; color: transparent; border: none; border-radius: 8px;")

    def restore_word_button(self, button):
        button.setEnabled(True)
        button.setStyleSheet(
            """
            QPushButton { background-color: #E2E2E2; border: none; padding: 12px 20px; color: black; border-radius: 8px; }
            QPushButton:hover { background-color: #D0D0D0; }
            """
        )
