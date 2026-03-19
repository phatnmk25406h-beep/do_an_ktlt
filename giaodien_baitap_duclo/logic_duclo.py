import sys
import os
import pandas as pd
import random
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Thay đổi cach import giaodien_baitap_duclo.giaodien_duclo vì nó mới xử lý được việc import class từ TỆP khác ( bất kể cấp nào)
from giaodien_baitap_duclo.giaodien_duclo import FillBlankUI


# =====================================================================
# PHẦN 1: CLASS QUẢN LÝ DỮ LIỆU (Đọc Excel, xáo trộn từ)
# =====================================================================
class FillBlankManager:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.data = self.df.to_dict('records')
        self.current_question = None

    def get_question(self, topic):
        # Lọc câu hỏi theo Topic
        filtered_data = [d for d in self.data if d['Topic'] == topic]
        if not filtered_data:
            return None  # Đã làm hết câu hỏi

        # Random 1 câu và lưu lại trạng thái
        self.current_question = random.choice(filtered_data)

        part1 = str(self.current_question['Đoạn đầu']).strip()
        correct_blank = str(self.current_question['Ô trống']).strip()
        part2 = str(self.current_question['Đoạn cuối']).strip()
        vi_trans = str(self.current_question['Dịch nghĩa']).strip()

        # 1. Lấy các ô trống khác trong Excel làm nhiễu
        all_blanks = [str(d['Ô trống']).strip() for d in self.data]
        distractors = list(set(all_blanks) - {correct_blank})

        # Chỉ lấy đúng 5 từ nhiễu (để cộng 1 đúng = 6 nút)
        distractors = distractors[:5]

        # 2. NẾU THIẾU (Ví dụ file chỉ có 5 câu -> chỉ có 4 nhiễu)
        if len(distractors) < 5:
            words_in_sentence = (part1 + " " + part2).replace('"', '').replace('.', '').split()
            extra_words = list(set(words_in_sentence) - set(distractors) - {correct_blank})
            for w in extra_words:
                if len(distractors) >= 5:
                    break
                distractors.append(w)

        # 3. Gộp lại và xáo trộn vị trí
        word_bank = [correct_blank] + distractors
        random.shuffle(word_bank)

        return {
            "part1": part1,
            "blank_correct": correct_blank,
            "part2": part2,
            "vi_trans": vi_trans,
            "word_bank": word_bank
        }

    def remove_current_question(self):
        """Xóa câu hỏi khỏi bộ nhớ nếu người dùng đã làm đúng"""
        if self.current_question in self.data:
            self.data.remove(self.current_question)


# =====================================================================
# PHẦN 2: CLASS XỬ LÝ SỰ KIỆN GIAO DIỆN (Click nút bấm, đổi màu)
# =====================================================================
class FillBlankApp(FillBlankUI):
    def __init__(self):
        super().__init__()

        # 1. Quản lý trạng thái
        self.state = "playing"
        self.current_selected_button = None
        self.current_correct_word = ""

        # 2. Khởi tạo Manager dữ liệu
        current_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(current_dir, "fill_blank.xlsx")
        self.manager = FillBlankManager(excel_path)

        # 3. Kết nối sự kiện cho nút Next và nút Close
        self.next_btn.clicked.connect(self.handle_next_click)
        self.next_btn.setEnabled(False)
        self.close_btn.clicked.connect(self.close)  # Cho phép bấm nút X để thoát

        # 4. Tải câu hỏi đầu tiên
        self.load_new_question()

    def load_new_question(self):
        """Logic tải câu hỏi từ Excel và vẽ nút lên giao diện"""
        self.reset_blank_ui()
        data = self.manager.get_question("Travel")

        if not data:
            self.part1.setText("")
            self.part2.setText("")
            self.vi_trans.setText("🎉 Chúc mừng! Bạn đã hoàn thành bài học.")
            self.next_btn.setEnabled(False)
            self.clear_word_bank()
            return

        self.part1.setText(data['part1'])
        self.part2.setText(data['part2'])
        self.vi_trans.setText(data['vi_trans'])
        self.current_correct_word = data['blank_correct']

        self.clear_word_bank()
        self.create_word_buttons(data['word_bank'])

    def create_word_buttons(self, words):
        """Logic tạo nút động"""
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        for i, word in enumerate(words):
            btn = QPushButton(word)
            btn.setFixedHeight(50)
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet("""
                QPushButton { background-color: #E2E2E2; border: none; color: black; padding: 10px 20px; border-radius: 8px; }
                QPushButton:hover { background-color: #D0D0D0; }
                QPushButton:disabled { color: transparent; background-color: #F0F0F0; }
            """)
            btn.clicked.connect(lambda checked, w=word, b=btn: self.select_word_logic(w, b))

            row, col = positions[i]
            self.words_layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

    def select_word_logic(self, word, button):
        """Xử lý logic khi người dùng chọn từ"""
        if self.state != "playing": return

        if self.current_selected_button:
            self.current_selected_button.setEnabled(True)
            self.current_selected_button.setStyleSheet("""
                QPushButton { background-color: #E2E2E2; border: none; padding: 12px 20px; color: black; border-radius: 8px; }
                QPushButton:hover { background-color: #D0D0D0; }
            """)

        self.blank_label.setText(word)
        button.setEnabled(False)
        button.setStyleSheet("background-color: #F0F0F0; color: transparent; border: none; border-radius: 8px;")

        self.current_selected_button = button
        self.next_btn.setEnabled(True)

    def handle_next_click(self):
        """Xử lý logic nút NEXT (Check -> Next/Reset)"""
        if self.state == "playing":
            if self.blank_label.text() == self.current_correct_word:
                self.blank_label.setStyleSheet(
                    "background-color: #3CD070; color: white; font-weight: bold; border-radius: 4px;")
                self.state = "correct"
            else:
                self.blank_label.setStyleSheet(
                    "background-color: #FF4444; color: white; font-weight: bold; border-radius: 4px;")
                self.state = "wrong"
        elif self.state == "correct":
            self.manager.remove_current_question()
            self.load_new_question()
        elif self.state == "wrong":
            self.reset_blank_ui()

    def reset_blank_ui(self):
        """Trả UI ô trống về trạng thái ban đầu"""
        self.blank_label.setText("")
        self.blank_label.setStyleSheet("background-color: #F0F0F0; border: 1px solid #E0E0E0; color: black;")
        if self.current_selected_button:
            self.current_selected_button.setEnabled(True)
            self.current_selected_button.setStyleSheet("""
                QPushButton { background-color: #E2E2E2; border: none; padding: 10px 20px; color: black; border-radius: 8px; }
                QPushButton:hover { background-color: #D0D0D0; }
            """)
            self.current_selected_button = None
        self.next_btn.setEnabled(False)
        self.state = "playing"

    def clear_word_bank(self):
        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Lấy đường dẫn thư mục hiện tại để chạy file đúng vị trí
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    window = FillBlankApp()
    window.show()
    sys.exit(app.exec())