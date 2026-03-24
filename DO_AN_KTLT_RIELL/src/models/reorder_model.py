import random
import pandas as pd


class LessonManager:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.data = self.df.to_dict("records")

    def get_question(self, topic):
        filtered_data = [d for d in self.data if d["Topic"] == topic]
        if not filtered_data:
            return None

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
