from src.view.giaodien_Flashcard import _load_cards_from_excel


class FlashcardModel:
    @staticmethod
    def load_cards(topic_name=None) -> list:
        return _load_cards_from_excel(topic_name=topic_name)
