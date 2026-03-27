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
import requests
import pandas as pd
from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QThread, pyqtSignal, QLocale
from PyQt6.QtGui import QPixmap
from PyQt6.QtTextToSpeech import QTextToSpeech

from .ui_mainwindow import Ui_MainWindow
class ImageLoaderThread(QThread):
    # Cập nhật: Tín hiệu giờ sẽ trả về cả (Dữ liệu ảnh, Đường link)
    image_loaded = pyqtSignal(bytes, str) 
    error_occurred = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            # Cập nhật: Phóng tín hiệu đi kèm theo cả self.url
            self.image_loaded.emit(response.content, self.url)
        except Exception as e:
            self.error_occurred.emit(str(e))
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

        self.cards     = cards if cards else [
            {
                "topic": "System",
                "word": "No Data",
                "phonetic": "",
                "meaning": "Chưa có dữ liệu flashcard",
                "example": "Hãy kiểm tra file Flashcard.xlsx",
                "image_path": ""
            }
        ]
        self.index     = 0
        self._is_front = True
        # Thêm dòng này: Khởi tạo bộ nhớ tạm (Cache) để lưu ảnh
        self.image_cache = {}
        self._connect_signals()
        self._load_card(self.index)
        self._show_front(animated=False)

        self.tts = QTextToSpeech(self)
        self.tts.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        self.tts.setRate(0.0)      # -1.0 tới 1.0
        self.tts.setPitch(0.0)     # -1.0 tới 1.0
        self.tts.setVolume(1.0)    # 0.0 tới 1.0
        # Thêm vào trong hàm __init__ của MainWindow nếu chưa có:
        try:
            self.df = pd.read_excel("Flashcard.xlsx") # Đường dẫn tới file Excel của bạn
        except Exception as e:
            print("Chưa load được file Excel:", e)

    def on_image_loaded(self, image_data, url):
        # LƯU VÀO RAM: Nhét dữ liệu ảnh vào từ điển với chìa khóa là url
        self.image_cache[url] = image_data

        # Phần hiển thị ảnh giữ nguyên
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        scaled_pixmap = pixmap.scaled(
            self.ui.pic.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.ui.pic.setPixmap(scaled_pixmap)
        self.ui.pic.setStyleSheet("background: transparent;")

    def on_image_error(self, error_msg):
        self.ui.pic.setText("Lỗi tải ảnh ❌")
        print(f"Lỗi tải ảnh: {error_msg}")

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self._flip)            # flip mặt trước
        self.ui.pushButton_3.clicked.connect(self._flip)          # flip mặt sau
        self.ui.button_back_2.clicked.connect(lambda: self.speak_word(self.ui.label_definition1.text())) #button phát âm
        self.ui.button_back.clicked.connect(self._go_back)        # nút ◀
        self.ui.button_continue_2.clicked.connect(self._go_next)  # nút ▶


    def _load_card(self, idx: int):
        if not self.cards or idx < 0 or idx >= len(self.cards):
            return

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
        image_path = str(data.get("image_path", "")).strip()
        self.ui.pic.clear()

        if hasattr(self, 'image_thread') and self.image_thread is not None:
            try:
                self.image_thread.image_loaded.disconnect()
                self.image_thread.error_occurred.disconnect()
            except TypeError:
                pass

        # Chuẩn hóa biến đường dẫn ảnh cho thống nhất
        image_url = str(image_path).strip() if image_path else ""

        if image_url and image_url != "nan":
            if image_url.startswith("http"):
                # --- TRƯỜNG HỢP 1: ẢNH TỪ MẠNG (WEB) ---
                if image_url in self.image_cache:
                    # Đã có trong Cache -> Gọi hàm hiển thị ảnh luôn (KHÔNG DÙNG return ở đây)
                    self.on_image_loaded(self.image_cache[image_url], image_url)
                else:
                    # Chưa có trong Cache -> Setup giao diện chờ và tải
                    self.ui.pic.setText("⏳ Đang tải ảnh...")
                    self.ui.pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.pic.setStyleSheet("background-color: #E0E0E0; color: #757575; border-radius: 12px; font-weight: bold;")

                    # Khởi tạo và chạy luồng phụ (Chỉ 1 lần duy nhất)
                    self.image_thread = ImageLoaderThread(image_url)
                    self.image_thread.image_loaded.connect(self.on_image_loaded)
                    self.image_thread.error_occurred.connect(self.on_image_error)
                    self.image_thread.start()
            else:
                # --- TRƯỜNG HỢP 2: ẢNH LOCAL (TRONG MÁY) ---
                base_dir = os.path.dirname(os.path.abspath(__file__))
                full_img_path = os.path.join(base_dir, image_url)
                
                if os.path.exists(full_img_path):
                    px = QPixmap(full_img_path).scaled(
                        251, 151,
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    self.ui.pic.setPixmap(px)
                    self.ui.pic.setStyleSheet("background: transparent;") # Xóa nền xám nếu có ảnh
                else:
                    self.ui.pic.setText("Không tìm thấy ảnh trong máy 😢")
                    self.ui.pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.pic.setStyleSheet("background-color: #E0E0E0; color: #757575; border-radius: 12px; font-weight: bold;")
        else:
            # --- TRƯỜNG HỢP 3: KHÔNG CÓ DATA ẢNH ---
            self.ui.pic.setText("Không có ảnh minh họa 😢")
            self.ui.pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.pic.setStyleSheet("background-color: #E0E0E0; color: #757575; border-radius: 12px; font-weight: bold;")

        # --- XỬ LÝ NÚT BẤM VÀ MẶT THẺ (Luôn được chạy vì đã bỏ cái return sai lầm) ---
        # Disable nút khi ở đầu / cuối danh sách
        self.ui.button_back.setEnabled(self.index > 0)
        self.ui.button_continue_2.setEnabled(self.index < len(self.cards) - 1)
        self.ui.button_back.setHidden(self.index <= 0)
        self.ui.button_continue_2.setHidden(self.index >= len(self.cards) - 1)
        
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


def _load_cards_from_excel() -> list:
    danh_sach_tu = []
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(base_dir, "Flashcard.xlsx")
        df = pd.read_excel(excel_path)
        danh_sach_tu = df.to_dict('records')
    except Exception as e:
        print("Lỗi khi đọc file Excel:", e)
        danh_sach_tu = [
            {
                "topic": "System",
                "word": "Error",
                "phonetic": "/ˈer.ɚ/",
                "meaning": "Lỗi hệ thống",
                "example": "Không tìm thấy file Excel.",
                "image_path": ""
            }
        ]
    return danh_sach_tu


def open_flashcard_ui(cards: list | None = None):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    if cards is None:
        cards = _load_cards_from_excel()

    window = MainWindow(cards=cards)
    window.show()
    return app, window


if __name__ == "__main__":
    app, window = open_flashcard_ui()
    sys.exit(app.exec())