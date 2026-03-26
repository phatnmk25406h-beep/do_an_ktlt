# Workflow:
#   1. Bạn tự chạy:  pyuic6 MainWindow.ui -o ui_mainwindow.py
#   2. File này import Ui_MainWindow từ ui_mainwindow.py đó
#   3. Chạy main.py là xong
#
# Widget names lấy từ MainWindow.ui:
#   self.ui.label               — tiêu đề topic
#   self.ui.label_3             — icon cờ
#   self.ui.pic                 — ảnh minh hoạ (mặt trước)
#   self.ui.label_definition1   — từ tiếng Anh (mặt trước)
#   self.ui.label_phienam       — phiên âm (mặt trước)
#   self.ui.button_back_2       — nút 🔊 phát âm
#   self.ui.pushButton          — transparent overlay flip (mặt trước)
#   self.ui.frame_2             — khung ảnh (mặt trước)
#   self.ui.frame_3             — toàn bộ mặt sau
#   self.ui.label_definitionTV  — nghĩa tiếng Việt (mặt sau)
#   self.ui.label_definition2   — từ tiếng Anh (mặt sau)
#   self.ui.label_phienam2      — phiên âm (mặt sau)
#   self.ui.label_ex            — câu ví dụ (mặt sau)
#   self.ui.pushButton_3        — transparent overlay flip (mặt sau)
#   self.ui.button_back         — nút ◀ Back
#   self.ui.button_continue_2   — nút ▶ Next
import os
import sys
import threading
from PyQt6.QtWidgets import QMainWindow, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, QEasingCurve
from PyQt6.QtTextToSpeech import QTextToSpeech
from PyQt6.QtCore import QLocale
from ui_mainwindow import Ui_MainWindow   

class MainWindow(QMainWindow):
    """
    Cửa sổ chính kế thừa Ui_MainWindow (generated bởi pyuic6).

    Nhận vào:
        cards (list[dict])  —  danh sách flashcard, mỗi card gồm:
            {
                "word":       str,   # từ tiếng Anh
                "phonetic":   str,   # phiên âm IPA
                "meaning":    str,   # nghĩa tiếng Việt
                "example":    str,   # câu ví dụ
                "image_path": str,   # đường dẫn ảnh, "" nếu không có
                "topic":      str,   # chủ đề hiển thị ở header
            }

    DEV NOTE — cách nối data:
        Truyền list cards từ bất kỳ nguồn nào vào constructor.

        JSON:
            import json
            cards = json.load(open("cards.json", encoding="utf-8"))
            window = MainWindow(cards=cards)
    """

    def __init__(self, cards: list, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cards     = cards
        self.index     = 0
        self._is_front = True

        self._connect_signals()
        self._load_card(self.index)
        self._show_front(animated=False)

        self.tts = QTextToSpeech(self)
        self.tts.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        self.tts.setRate(0.0)      # -1.0 tới 1.0
        self.tts.setPitch(0.0)     # -1.0 tới 1.0
        self.tts.setVolume(1.0)    # 0.0 tới 1.0

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self._flip)            # flip mặt trước
        self.ui.pushButton_3.clicked.connect(self._flip)          # flip mặt sau
        self.ui.button_back_2.clicked.connect(lambda: self.speak_word(self.ui.label_definition1.text())) #button phát âm
        self.ui.button_back.clicked.connect(self._go_back)        # nút ◀
        self.ui.button_continue_2.clicked.connect(self._go_next)  # nút ▶


    def _load_card(self, idx: int):
        data = self.cards[idx]
        # Header
        self.ui.label.setText(f"Topic: {data.get('topic', '')}")
        # Mặt trước
        self.ui.label_definition1.setText(data.get("word", ""))
        self.ui.label_phienam.setText(data.get("phonetic", ""))
        # Mặt sau
        self.ui.label_definitionTV.setText(data.get("meaning", ""))
        self.ui.label_definition2.setText(data.get("word", ""))
        self.ui.label_phienam2.setText(data.get("phonetic", ""))
        self.ui.label_ex.setText(f"Eg: {data.get('example', '')}")

        # Ảnh
        img_path = data.get("image_path", "").strip()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_img_path = os.path.join(base_dir, img_path) if img_path else "" #lấy thư mục của file Python hiện tại
        if full_img_path and os.path.exists(full_img_path):
            px = QPixmap(full_img_path).scaled(
            251, 151,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
            )
            self.ui.pic.setPixmap(px)
        else:
            self.ui.pic.clear()
        # Disable nút khi ở đầu / cuối danh sách
        self.ui.button_back.setEnabled(self.index > 0)
        self.ui.button_continue_2.setEnabled(self.index < len(self.cards) - 1)
        self.ui.button_back.setHidden(self.index <= 0)
        self.ui.button_continue_2.setHidden(self.index >= len(self.cards) - 1)
        # setHidden vs setEnable là hai hàm nhận tham số True/False
        # để đặt đk cần dùng 2 hàm này chứ k phải hide/show

        # Lun reset về mặt trc khi đổi card
        self._show_front(animated=False)

    # Lật
    def _flip(self):
        effect = QGraphicsOpacityEffect(self.ui.frame) #QGraphicOpacity để can thiệp opacity của qt
        self.ui.frame.setGraphicsEffect(effect)

        fade_out = QPropertyAnimation(effect, b"opacity", self)
        fade_out.setDuration(120)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InQuad) # chậm đầu nhanh cuối 

        fade_in = QPropertyAnimation(effect, b"opacity", self)
        fade_in.setDuration(120)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutQuad) # nhanh đầu chậm cúi

        self._anim = QSequentialAnimationGroup(self) # nối 2 thành 1
        self._anim.addAnimation(fade_out)
        self._anim.addAnimation(fade_in)

        if self._is_front:
            fade_out.finished.connect(lambda: self._show_back())
        else:
            fade_out.finished.connect(lambda: self._show_front())

        self._anim.start()

    def _show_front(self, animated=True):
        self._is_front = True
        self.ui.frame_3.hide()
        self.ui.frame_2.show()
        self.ui.label_definition1.show()
        self.ui.label_phienam.show()
        self.ui.button_back_2.show()
        self.ui.button_back_2.raise_()
        self.ui.pushButton.raise_()

    def _show_back(self, animated=True):
        self._is_front = False
        self.ui.frame_2.hide()
        self.ui.label_definition1.hide()
        self.ui.label_phienam.hide()
        self.ui.frame_3.show()
        self.ui.layoutWidget.raise_()

    # Pát âm
    def speak_word(self, word: str):
        self.tts.stop()
        self.tts.say(word)


    # back với next
    def _go_next(self):
        if self.index < len(self.cards) - 1:
            self.index += 1
            self._load_card(self.index)

    def _go_back(self):
        if self.index > 0:
            self.index -= 1
            self._load_card(self.index)
