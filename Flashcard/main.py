
# DEV NOTE — cách nối database:
#   Thay list FLASHCARDS bên dưới bằng data thật của bạn.
#   Mỗi phần tử là dict với các key:
#       "word"       : str  — từ tiếng Anh
#       "phonetic"   : str  — phiên âm IPA
#       "meaning"    : str  — nghĩa tiếng Việt
#       "example"    : str  — câu ví dụ
#       "image_path" : str  — đường dẫn ảnh (để "" nếu không có)
#       "topic"      : str  — chủ đề
#
#   Ví dụ SQLite:
#       import sqlite3
#       conn  = sqlite3.connect("vocab.db")
#       rows  = conn.execute("SELECT word,phonetic,meaning,example,image_path,topic FROM cards").fetchall()
#       cards = [dict(zip(["word","phonetic","meaning","example","image_path","topic"], r)) for r in rows]
#
#   Ví dụ JSON:
#       import json
#       cards = json.load(open("cards.json", encoding="utf-8"))
#
#   Sau đó truyền vào: MainWindow(cards=cards)
# =============================================================

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from main_window import MainWindow

FLASHCARDS = [
    {
        "word":       "Breathtaking",
        "phonetic":   "/ˈbreθˌteɪ.kɪŋ/",
        "meaning":    "Ngoạn mục, đẹp đến ngạt thở",
        "example":    "The view from the mountain was breathtaking.",
        "image_path": "Ảnh/Untitleddesign.png",
        "topic":      "Travel & Culture",
    },
    {
        "word":       "Itinerary",
        "phonetic":   "/aɪˈtɪn.ə.rer.i/",
        "meaning":    "Lịch trình chuyến đi",
        "example":    "She planned a detailed itinerary for the trip.",
        "image_path": "Ảnh/hihi.jpg",
        "topic":      "Travel & Culture",
    },
    {
        "word":       "Souvenir",
        "phonetic":   "/ˌsuː.vəˈnɪər/",
        "meaning":    "Đồ lưu niệm",
        "example":    "He bought a souvenir from every city he visited.",
        "image_path": "",
        "topic":      "Travel & Culture",
    },
    {
        "word":       "Wanderlust",
        "phonetic":   "/ˈwɒn.də.lʌst/",
        "meaning":    "Khao khát được đi du lịch",
        "example":    "Her wanderlust led her to visit 30 countries.",
        "image_path": "",
        "topic":      "Travel & Culture",
    },
    {
        "word":       "Hospitality",
        "phonetic":   "/ˌhɒs.pɪˈtæl.ɪ.ti/",
        "meaning":    "Lòng hiếu khách",
        "example":    "The locals showed great hospitality to the tourists.",
        "image_path": "",
        "topic":      "Travel & Culture",
    },
]


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow(cards=FLASHCARDS)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
