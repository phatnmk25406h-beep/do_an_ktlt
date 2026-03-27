import random
import pandas as pd


class FillBlankManager:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.data = self.df.to_dict("records")
        self.current_question = None

    def get_question(self, topic):
        # 1. Nếu không có topic thì bỏ qua
        if not topic:
            return None

        # 2. Chuẩn hóa chuỗi (đưa về chữ thường, cắt khoảng trắng)
        topic_clean = str(topic).strip().lower()

        # 3. Lọc dữ liệu, chú ý xử lý tên cột an toàn
        filtered_data = [
            d for d in self.data 
            if str(d.get("Topic", "")).strip().lower() == topic_clean
        ]
        
        if not filtered_data:
            return None

        self.current_question = random.choice(filtered_data)

        part1 = str(self.current_question["Đoạn đầu"]).strip()
        correct_blank = str(self.current_question["Ô trống"]).strip()
        part2 = str(self.current_question["Đoạn cuối"]).strip()
        vi_trans = str(self.current_question["Dịch nghĩa"]).strip()

        all_blanks = [str(d["Ô trống"]).strip() for d in self.data]
        distractors = list(set(all_blanks) - {correct_blank})
        distractors = distractors[:5]

        if len(distractors) < 5:
            words_in_sentence = (part1 + " " + part2).replace('"', "").replace(".", "").split()
            extra_words = list(set(words_in_sentence) - set(distractors) - {correct_blank})
            for word in extra_words:
                if len(distractors) >= 5:
                    break
                distractors.append(word)

        word_bank = [correct_blank] + distractors
        random.shuffle(word_bank)

        return {
            "part1": part1,
            "blank_correct": correct_blank,
            "part2": part2,
            "vi_trans": vi_trans,
            "word_bank": word_bank,
        }

    def remove_current_question(self):
        if self.current_question in self.data:
            self.data.remove(self.current_question)
