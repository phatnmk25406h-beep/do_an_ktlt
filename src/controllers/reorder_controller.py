import os
import time

from src.models.reorder_model import LessonManager
from src.view.giaodien_sapxep_render import LessonRender
from src.models.user_model import add_learning_time

class LessonApp:
    def __init__(self, topic_name=None, current_user=None):
        self.view = LessonRender()
        self.topic_name = topic_name
        self.current_correct_answer = ""
        self.selected_words = []
        self.start_time = time.time()
        self.current_user = current_user or "guest"

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        excel_path = os.path.join(base_dir, "data", "sapxeptu.xlsx")
        self.manager = LessonManager(excel_path)

        self.view.bind_handlers(on_close=self.close, on_check=self.check_answer, on_continue=self.reset_for_next_question)
        self.view.closeEvent = self.closeEvent

        self.load_new_question()

    def show(self):
        self.view.show()

    def close(self):
        self.view.close()

    def load_new_question(self):
        data = self.manager.get_question(self.topic_name)
        if not data:
            self.view.show_completed()
            return

        self.view.set_question_text(data["vi"])
        self.current_correct_answer = data["en_correct"]

        self.view.render_word_bank(data["word_bank"], self.add_word_to_answer)
        self.view.set_check_enabled(False)

    def add_word_to_answer(self, word, button):
        self.selected_words.append(word)
        self.view.add_selected_chip(word, button, self.remove_word_from_answer)
        self.view.set_check_enabled(len(self.selected_words) > 0)

    def remove_word_from_answer(self, word, word_chip, original_button):
        if word in self.selected_words:
            self.selected_words.remove(word)

        word_chip.deleteLater()
        original_button.setEnabled(True)
        self.view.set_check_enabled(len(self.selected_words) > 0)

    def reset_for_next_question(self):
        self.view.show_input_footer()

        if getattr(self, "is_correct", False):
            current_vi_text = self.view.vietnamese_text.text()
            self.manager.remove_question(current_vi_text)

            self.view.clear_selected_words(restore_original_buttons=False)

            self.selected_words.clear()
            self.view.set_check_enabled(False)
            self.load_new_question()
        else:
            self.view.clear_selected_words(restore_original_buttons=True)

            self.selected_words.clear()
            self.view.set_check_enabled(False)

    def check_answer(self):
        user_answer = " ".join(self.selected_words)
        correct_answer = self.current_correct_answer.strip()

        if user_answer.strip() == correct_answer:
            self.is_correct = True
        else:
            self.is_correct = False
        self.view.show_result(self.is_correct, correct_answer)

    def closeEvent(self, event):
        minutes_spent = (time.time() - self.start_time) / 60.0

        if minutes_spent > 0.1 and self.current_user:
            success = add_learning_time(self.current_user, minutes_spent)
            if success:
                print(f"Đã lưu thành công {minutes_spent:.2f} phút cho user '{self.current_user}'")
            else:
                print("Lỗi: Không thể lưu thời gian học!")

        event.accept()