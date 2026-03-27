from src.models.flashcard_model import FlashcardModel
from src.view.giaodien_Flashcard import open_flashcard_ui


class FlashcardApp:
    def __init__(self, topic_name=None):
        self.window = None
        self.topic_name = topic_name
    def show(self):
        cards = FlashcardModel.load_cards(self.topic_name)
        _, self.window = open_flashcard_ui(cards)
