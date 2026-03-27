import sys

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QGraphicsOpacityEffect, QMainWindow

from .giaodien_flashcard_ui import Ui_MainWindow


class FlashcardView(QMainWindow):
    """Presentation-only view for Flashcard screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._is_front = True
        self.show_front()

    def bind_handlers(self, on_flip, on_prev, on_next, on_speak):
        self.ui.pushButton.clicked.connect(on_flip)
        self.ui.pushButton_3.clicked.connect(on_flip)
        self.ui.button_back.clicked.connect(on_prev)
        self.ui.button_continue_2.clicked.connect(on_next)
        self.ui.button_back_2.clicked.connect(lambda: on_speak(self.ui.label_definition1.text()))

    @property
    def is_front(self):
        return self._is_front

    def render_card_text(self, card: dict):
        self.ui.label.setText(f"Topic: {card.get('topic', '')}")
        self.ui.label_definition1.setText(card.get("word", ""))
        self.ui.label_phienam.setText(card.get("phonetic", ""))
        self.ui.label_definitionTV.setText(card.get("meaning", ""))
        self.ui.label_definition2.setText(card.get("word", ""))
        self.ui.label_phienam2.setText(card.get("phonetic", ""))
        self.ui.label_ex.setText(f"Eg: {card.get('example', '')}")

    def set_navigation_state(self, index: int, total: int):
        at_start = index <= 0
        at_end = index >= (total - 1)
        self.ui.button_back.setEnabled(not at_start)
        self.ui.button_continue_2.setEnabled(not at_end)
        self.ui.button_back.setHidden(at_start)
        self.ui.button_continue_2.setHidden(at_end)

    def set_image_pixmap(self, pixmap: QPixmap):
        scaled = pixmap.scaled(
            self.ui.pic.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.ui.pic.setPixmap(scaled)
        self.ui.pic.setStyleSheet("background: transparent;")

    def show_loading_image(self):
        self.ui.pic.clear()
        self.ui.pic.setText("Dang tai anh...")
        self.ui.pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.pic.setStyleSheet("background-color: #E0E0E0; color: #757575; border-radius: 12px; font-weight: bold;")

    def show_image_error(self):
        self.ui.pic.clear()
        self.ui.pic.setText("Loi tai anh")
        self.ui.pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.pic.setStyleSheet("background-color: #E0E0E0; color: #757575; border-radius: 12px; font-weight: bold;")

    def show_no_image(self):
        self.ui.pic.clear()
        self.ui.pic.setText("Khong co anh minh hoa")
        self.ui.pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.pic.setStyleSheet("background-color: #E0E0E0; color: #757575; border-radius: 12px; font-weight: bold;")

    def show_front(self):
        self._is_front = True
        self.ui.frame_3.hide()
        self.ui.frame_2.show()
        self.ui.label_definition1.show()
        self.ui.label_phienam.show()
        self.ui.button_back_2.show()
        self.ui.button_back_2.raise_()
        self.ui.pushButton.raise_()

    def show_back(self):
        self._is_front = False
        self.ui.frame_2.hide()
        self.ui.label_definition1.hide()
        self.ui.label_phienam.hide()
        self.ui.frame_3.show()
        self.ui.layoutWidget.raise_()

    def animate_flip(self, on_midpoint):
        effect = QGraphicsOpacityEffect(self.ui.frame)
        self.ui.frame.setGraphicsEffect(effect)

        fade_out = QPropertyAnimation(effect, b"opacity", self)
        fade_out.setDuration(120)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InQuad)

        fade_in = QPropertyAnimation(effect, b"opacity", self)
        fade_in.setDuration(120)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutQuad)

        self._anim = QSequentialAnimationGroup(self)
        self._anim.addAnimation(fade_out)
        self._anim.addAnimation(fade_in)
        fade_out.finished.connect(on_midpoint)
        self._anim.start()


def open_flashcard_ui(cards: list | None = None):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = FlashcardView()
    window.show()
    return app, window


if __name__ == "__main__":
    app, window = open_flashcard_ui()
    sys.exit(app.exec())