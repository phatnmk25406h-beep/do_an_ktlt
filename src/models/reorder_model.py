import random
import pandas as pd


class LessonManager:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.data = self.df.to_dict("records")

    def get_question(self, topic):
        # 2. Tự động quét tên cột Topic (đề phòng Excel có dấu cách ẩn như "Topic ")
        topic_col_name = "Topic"
        if self.data:
            for key in self.data[0].keys():
                if "topic" in str(key).lower():
                    topic_col_name = key
                    break

        # 3. Chuẩn hóa và lọc
        topic_clean = str(topic).strip().lower()
        filtered_data = [d for d in self.data if str(d.get(topic_col_name, "")).strip().lower() == topic_clean]
        
        if not filtered_data:
            print(f"--- DEBUG 3: Lọc xong không thấy câu nào cho chủ đề '{topic_clean}'! ---")
            return None

        # --- TỪ ĐÂY TRỞ XUỐNG GIỮ NGUYÊN CODE CŨ CỦA BẠN ---
        question_data = random.choice(filtered_data)
        vietnamese = question_data["Đoạn tiếng việt"]
        english = question_data["Đoạn tiếng anh"]

        words = english.split()
        all_words = []
        for entry in self.data:
            all_words.extend(entry["Đoạn tiếng anh"].split())

        distractors = random.sample(list(set(all_words) - set(words)), 2)
        word_bank = words + distractors
        random.shuffle(word_bank)

        return {
            "vi": vietnamese,
            "en_correct": english,
            "word_bank": word_bank,
        }

    def remove_question(self, vi_text):
        self.data = [d for d in self.data if d["Đoạn tiếng việt"] != vi_text]
