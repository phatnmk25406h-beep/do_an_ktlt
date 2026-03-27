import os

import requests
from PyQt6.QtCore import QLocale, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtTextToSpeech import QTextToSpeech

from src.config.settings import BASE_DIR
from src.models.flashcard_model import FlashcardModel
from src.view.giaodien_flashcard_render import FlashcardView


class ImageLoaderThread(QThread):
    image_loaded = pyqtSignal(bytes, str)
    error_occurred = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            self.image_loaded.emit(response.content, self.url)
        except Exception as exc:
            self.error_occurred.emit(str(exc))


class FlashcardApp:
    def __init__(self, topic_name=None):
        self.window = None
        self.topic_name = topic_name
        self.cards = []
        self.index = 0
        self.image_cache = {}
        self._image_thread = None
        self.tts = None

    def show(self):
        self.cards = FlashcardModel.load_cards(self.topic_name)
        if not self.cards:
            self.cards = [
                {
                    "topic": "System",
                    "word": "No Data",
                    "phonetic": "",
                    "meaning": "Chua co du lieu flashcard",
                    "example": "Hay kiem tra file Flashcard.xlsx",
                    "image_path": "",
                }
            ]

        self.index = 0
        self.window = FlashcardView()
        self.window.bind_handlers(
            on_flip=self._flip,
            on_prev=self._go_back,
            on_next=self._go_next,
            on_speak=self._speak_word,
        )

        self.tts = QTextToSpeech(self.window)
        self.tts.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        self.tts.setRate(0.0)
        self.tts.setPitch(0.0)
        self.tts.setVolume(1.0)

        self._render_current_card()
        self.window.show()

    def _render_current_card(self):
        if not self.cards or self.index < 0 or self.index >= len(self.cards):
            return

        card = self.cards[self.index]
        self.window.render_card_text(card)
        self.window.show_front()
        self.window.set_navigation_state(self.index, len(self.cards))
        self._load_card_image(card.get("image_path", ""))

    def _load_card_image(self, image_path):
        image_url = str(image_path).strip()
        if not image_url or image_url.lower() == "nan":
            self.window.show_no_image()
            return

        if image_url.startswith("http"):
            if image_url in self.image_cache:
                self._set_image_from_bytes(self.image_cache[image_url])
                return

            self.window.show_loading_image()
            self._start_image_thread(image_url)
            return

        if os.path.isabs(image_url):
            file_path = image_url
        else:
            file_path = os.path.join(BASE_DIR, image_url)

        if os.path.exists(file_path):
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                self.window.show_image_error()
            else:
                self.window.set_image_pixmap(pixmap)
        else:
            self.window.show_image_error()

    def _start_image_thread(self, image_url):
        if self._image_thread and self._image_thread.isRunning():
            self._image_thread.quit()
            self._image_thread.wait()

        self._image_thread = ImageLoaderThread(image_url)
        self._image_thread.image_loaded.connect(self._on_image_loaded)
        self._image_thread.error_occurred.connect(self._on_image_error)
        self._image_thread.start()

    def _on_image_loaded(self, image_data, image_url):
        self.image_cache[image_url] = image_data
        self._set_image_from_bytes(image_data)

    def _on_image_error(self, error_message):
        print(f"Loi tai anh flashcard: {error_message}")
        self.window.show_image_error()

    def _set_image_from_bytes(self, image_data):
        pixmap = QPixmap()
        if not pixmap.loadFromData(image_data):
            self.window.show_image_error()
            return
        self.window.set_image_pixmap(pixmap)

    def _flip(self):
        if not self.window:
            return

        def _toggle_side():
            if self.window.is_front:
                self.window.show_back()
            else:
                self.window.show_front()

        self.window.animate_flip(_toggle_side)

    def _go_next(self):
        if self.index < len(self.cards) - 1:
            self.index += 1
            self._render_current_card()

    def _go_back(self):
        if self.index > 0:
            self.index -= 1
            self._render_current_card()

    def _speak_word(self, word):
        if not self.tts:
            return
        self.tts.stop()
        self.tts.say(word)
