# -*- coding: utf-8 -*-
# main.py  –  Điểm khởi chạy
#
# Cấu trúc project:
#   account_page.ui   ← Qt Designer source (file gốc của bạn, đã nâng cấp)
#   ui_account.py     ← Bản dịch Python từ .ui (tương đương pyuic6)
#   ext_account.py    ← Logic: sidebar, matplotlib chart, export
#   main.py           ← File này
#
# Cài đặt:
#   pip install PyQt6 matplotlib numpy
#   pip install openpyxl   # chỉ cần nếu dùng export Excel

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ext_account import AccountWindow


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 9))

    win = AccountWindow()

    # ── (Tùy chọn) Dev inject data thực ──────────────────────────────────────
    # win.set_user_info("Nguyen Van A", "Level 3", 55, 12, 20)
    # win.set_lesson_info("Unit 5: Food & Cooking", 8, 25)
    # win.set_weekly_data(
    #     ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    #     [50, 70, 30, 90, 60, 80, 40],
    # )
    # win.set_vocab_data({"Mastered":120,"Learning":80,"New Words":40})
    # win.set_word_of_day(
    #     "Ephemeral", "/ɪˈfem.ər.əl/",
    #     "Lasting for a very short time.",
    #     "Social media trends are often ephemeral.",
    # )

    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
