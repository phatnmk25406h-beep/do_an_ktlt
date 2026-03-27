import os

import pandas as pd

from src.config.settings import BASE_DIR


class FlashcardModel:
    @staticmethod
    def load_cards(topic_name=None) -> list:
        cards = []
        try:
            excel_path = os.path.join(BASE_DIR, "data", "Flashcard.xlsx")
            df = pd.read_excel(excel_path)
            cards = df.to_dict("records")
            if topic_name:
                normalized_topic = str(topic_name).strip().lower()
                cards = [
                    item
                    for item in cards
                    if str(item.get("topic", "")).strip().lower() == normalized_topic
                ]
        except Exception as exc:
            print("Loi khi doc Flashcard.xlsx:", exc)
        return cards
