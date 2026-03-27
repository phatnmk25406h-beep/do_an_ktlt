import os
import time

from src.models.fill_blank_model import FillBlankManager
from src.view.giaodien_duclo_render import FillBlankRender
from src.models.user_model import add_learning_time

class FillBlankApp:
    def __init__(self, topic_name=None, current_user=None):
        self.view = FillBlankRender()
        self.topic_name = topic_name
        self.view.set_topic_title(self.topic_name)
        self.state = "playing"
        self.current_selected_button = None
        self.current_correct_word = ""
        self.start_time = time.time()
        self.current_user = current_user or "guest"

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        excel_path = os.path.join(base_dir, "data", "fill_blank.xlsx")
        self.manager = FillBlankManager(excel_path)

        self.view.bind_handlers(on_next=self.handle_next_click, on_close=self.close)
        self.view.set_next_enabled(False)
        self.view.closeEvent = self.closeEvent

        self.load_new_question()

    def show(self):
        self.view.show()

    def close(self):
        self.view.close()

    def load_new_question(self):
        self.reset_blank_ui()
        data = self.manager.get_question(self.topic_name)

        if not data:
            self.view.show_completed()
            return

        self.view.render_question(data["part1"], data["part2"], data["vi_trans"])
        self.current_correct_word = data["blank_correct"]

        self.view.render_word_bank(data["word_bank"], self.select_word_logic)

    def select_word_logic(self, word, button):
        if self.state != "playing":
            return

        if self.current_selected_button:
            self.view.restore_word_button(self.current_selected_button)

        self.view.set_blank_text(word)
        self.view.mark_word_selected(button)

        self.current_selected_button = button
        self.view.set_next_enabled(True)

    def handle_next_click(self):
        if self.state == "playing":
            if self.view.blank_label.text() == self.current_correct_word:
                self.view.set_blank_correct_style()
                self.state = "correct"
            else:
                self.view.set_blank_wrong_style()
                self.state = "wrong"
        elif self.state == "correct":
            self.manager.remove_current_question()
            self.load_new_question()
        elif self.state == "wrong":
            self.reset_blank_ui()

    def reset_blank_ui(self):
        self.view.reset_blank_style()
        if self.current_selected_button:
            self.view.restore_word_button(self.current_selected_button)
            self.current_selected_button = None
        self.view.set_next_enabled(False)
        self.state = "playing"

    def closeEvent(self, event):
        minutes_spent = (time.time() - self.start_time) / 60.0

        if minutes_spent > 0.1 and self.current_user:
            success = add_learning_time(self.current_user, minutes_spent)
            if success:
                print(f"Đã lưu thành công {minutes_spent:.2f} phút cho user '{self.current_user}'")
            else:
                print("Lỗi: Không thể lưu thời gian học!")

        event.accept()