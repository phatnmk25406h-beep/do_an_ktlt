import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from PyQt6.QtCore import QTimer

from account_page import Ui_MainWindow


_G_DARK  = "#16a34a"
_G_MAIN  = "#22c55e"
_G_LIGHT = "#4ade80"
_G_PALE  = "#86efac"
_G_GHOST = "#bbf7d0"
_GRAY    = "#6b7280"


class AccountWindow(QMainWindow):
    """
    Cửa sổ chính Account Page.

    Dev inject dữ liệu:
        win.set_user_info(username, level_text, level_pct, streak_n, best_n)
        win.set_lesson_info(unit_name, done, total)
        win.set_weekly_data(days, minutes)
        win.set_vocab_data({"Mastered":40,"Learning":35,"New Words":25})
        win.set_word_of_day(word, phonetic, definition, example)
    """

    CHART_BAR     = "bar"
    CHART_PIE     = "pie"
    CHART_SCATTER = "scatter"
    CHART_LINE    = "line"
    _STYLE_ERROR = """QLabel{
        border-radius:8px;
        background:#fff5f5;font-size:8px;color:red;
    }"""
    _STYLE_OKEE = """QLabel{color:#34C759;
    font-size:8px;
    background:transparent;border:none;font-weight:bold;
    }"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Dữ liệu mẫu 
        self._days    = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        self._minutes: list[float] = [30, 45, 60, 20, 80, 55, 40]
        self._vocab: dict[str, float] = {"Mastered":40,"Learning":35,"New Words":25}
        self._scatter_x: list[float] = list(range(1, 8))
        self._scatter_y: list[float] = [15, 40, 30, 55, 70, 50, 65]

        self._sidebar_open   = False
        self._current_chart  = self.CHART_BAR

        # Nhúng matplotlib vào khung frm_chart 
        self._fig    = Figure(facecolor="none", tight_layout=True)
        self._canvas = FigureCanvas(self._fig)
        self._canvas.setStyleSheet("background:transparent;")
        self.ui.frm_chart.layout().addWidget(self._canvas)

        # signals 
        self._connect()

        # Bar chart
        self._activate_chart_btn(self.ui.pushButton_2)
        self._draw()

    def _connect(self):
        ui = self.ui
        
        # Chart buttons
        ui.pushButton_2.clicked.connect(lambda: self._switch_chart(self.CHART_BAR,     ui.pushButton_2))
        ui.pushButton_3.clicked.connect(lambda: self._switch_chart(self.CHART_PIE,     ui.pushButton_3))
        ui.pushButton_4.clicked.connect(lambda: self._switch_chart(self.CHART_SCATTER, ui.pushButton_4))
        ui.pushButton_5.clicked.connect(lambda: self._switch_chart(self.CHART_LINE,    ui.pushButton_5))

        # Export
        ui.button_continue_2.clicked.connect(self._handle_export)

        # Continue lesson - nối vô đây nè P
        #ui.button_continue.clicked.connect(self._on_continue)

    # Chart switching
    _BTN_NORMAL = (
        "QPushButton{background:white;border:none;border-radius:6px;font-size:8px;color:#222;}"
        "QPushButton:hover{background:#e8fdf0;color:#22c55e;}"
        "QPushButton:checked{background:#dff1e6;color:#22c55e;font-weight:bold;border:1.5px solid #22c55e;}"
    )

    def _activate_chart_btn(self, active_btn):
        for btn in (self.ui.pushButton_2, self.ui.pushButton_3,
                    self.ui.pushButton_4, self.ui.pushButton_5):
            btn.setChecked(btn is active_btn)
            btn.setStyleSheet(self._BTN_NORMAL)  

    def _switch_chart(self, chart_type: str, btn):
        self._current_chart = chart_type
        self._activate_chart_btn(btn)

        # Cập nhật label phụ
        subtitles = {
            self.CHART_BAR:     "Weekly Study Time (minutes)",
            self.CHART_PIE:     "Word Mastery Distribution",
            self.CHART_SCATTER: "Progress Score vs Day",
            self.CHART_LINE:    "Weekly Study Trend",
        }
        self.ui.label_30.setText(subtitles[chart_type])
        self._draw()

    def _draw(self):
        self._fig.clear()
        ax = self._fig.add_subplot(111)
        ax.set_facecolor("#fafafa")
        self._fig.patch.set_facecolor("#fafafa")
        for sp in ax.spines.values():
            sp.set_color("#e5e5e5")
        ax.tick_params(colors=_GRAY, labelsize=8)

        ct = self._current_chart
        if   ct == self.CHART_BAR:     self._bar(ax)
        elif ct == self.CHART_PIE:     self._pie(ax)
        elif ct == self.CHART_SCATTER: self._scatter(ax)
        elif ct == self.CHART_LINE:    self._line(ax)

        self._canvas.draw()

    def _bar(self, ax):
        max_v = max(self._minutes) if self._minutes else 1
        colors = [_G_DARK if m == max_v else _G_LIGHT for m in self._minutes]
        bars = ax.bar(self._days, self._minutes, color=colors, width=0.5, zorder=2)
        ax.yaxis.grid(True, color="#e5e5e5", linestyle="--", linewidth=0.6, zorder=1)
        ax.set_axisbelow(True)
        ax.set_ylabel("min", color=_GRAY, fontsize=8)
        for b, v in zip(bars, self._minutes):
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.8,
                    str(int(v)), ha="center", va="bottom",
                    fontsize=7, color=_G_DARK, fontweight="bold")

    def _pie(self, ax):
        labels = list(self._vocab.keys())
        sizes  = list(self._vocab.values())
        colors = [_G_MAIN, _G_LIGHT, _G_GHOST]
        ax.pie(sizes, labels=labels, colors=colors, autopct="%1.0f%%",
               startangle=140,
               wedgeprops={"linewidth":1.5, "edgecolor":"#ffffff"},
               textprops={"color":"#374151", "fontsize":8})
        ax.axis("equal")

    def _scatter(self, ax):
        x, y = self._scatter_x, self._scatter_y
        ax.scatter(x, y, color=_G_MAIN, s=55, zorder=3,
                   edgecolors=_G_DARK, linewidths=0.7)
        z = np.polyfit(x, y, 1)
        xs = np.linspace(min(x), max(x), 100)
        ax.plot(xs, np.poly1d(z)(xs), color=_G_LIGHT, linewidth=1.4,
                linestyle="--", alpha=0.8)
        ax.yaxis.grid(True, color="#e5e5e5", linestyle="--", linewidth=0.6)
        ax.set_axisbelow(True)
        ax.set_xlabel("Day", color=_GRAY, fontsize=8)
        ax.set_ylabel("Score", color=_GRAY, fontsize=8)

    def _line(self, ax):
        xi = range(len(self._days))
        ax.plot(xi, self._minutes, color=_G_MAIN, linewidth=2,
                marker="o", markersize=5, markerfacecolor=_G_DARK)
        ax.fill_between(xi, self._minutes, alpha=0.12, color=_G_LIGHT)
        ax.set_xticks(list(xi))
        ax.set_xticklabels(self._days, fontsize=8)
        ax.yaxis.grid(True, color="#e5e5e5", linestyle="--", linewidth=0.6)
        ax.set_axisbelow(True)
        ax.set_ylabel("min", color=_GRAY, fontsize=8)
    
    def show_dow_error(self, msg: str): 
        self.ui.noti_dowload.setText(msg)
        self.ui.noti_dowload.setStyleSheet(self._STYLE_ERROR)
        QTimer.singleShot(3000, lambda: self.ui.noti_dowload.clear())
    
    def show_dow_okee(self, msg: str): 
        self.ui.noti_dowload.setText(msg)
        self.ui.noti_dowload.setStyleSheet(self._STYLE_OKEE)
        QTimer.singleShot(3000, lambda: self.ui.noti_dowload.clear())
    
    def _handle_export(self):
        ui = self.ui
        selected = {
            "csv":   ui.checkBox.isChecked(),
            "json":  ui.checkBox_2.isChecked(),
            "xml":   ui.checkBox_3.isChecked(),
            "excel": ui.checkBox_4.isChecked(),
        }
        fmts = [k for k, v in selected.items() if v]
        if not fmts:
            self.show_dow_error("Chọn ít nhất một định dạng nhé!")
            return

        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục xuất") # dùng để tải file về
        if not folder:
            return

        data = {
            "weekly_study_minutes": dict(zip(self._days, self._minutes)),
            "vocab_mastery": self._vocab,
        }
        done = []
        for fmt in fmts:
            try:
                path = self._export_fmt(fmt, data, folder)
                done.append(path)
            except Exception as e:
                self.show_dow_error("Lỗi", f"Lỗi xuất {fmt}:\n{e}")

        if done:
            self.show_dow_okee("Bạn đã xuất file thành công!")

    def _export_fmt(self, fmt: str, data: dict, folder: str) -> str:
        base = Path(folder) / "analytics_export"
        if fmt == "csv":
            p = base.with_suffix(".csv")
            with open(p, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["category","key","value"])
                for cat, rows in data.items():
                    if isinstance(rows, dict):
                        for k, v in rows.items():
                            w.writerow([cat, k, v])
            return str(p)

        if fmt == "json":
            p = base.with_suffix(".json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return str(p)

        if fmt == "xml":
            p = base.with_suffix(".xml")
            root = ET.Element("analytics")
            for cat, rows in data.items():
                el = ET.SubElement(root, cat.replace(" ","_"))
                if isinstance(rows, dict):
                    for k, v in rows.items():
                        item = ET.SubElement(el, "item")
                        item.set("key", str(k))
                        item.text = str(v)
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            tree.write(p, encoding="utf-8", xml_declaration=True)
            return str(p)

        if fmt == "excel":
            try:
                import openpyxl
            except ImportError:
                raise RuntimeError
            p = base.with_suffix(".xlsx")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Analytics"
            ws.append(["Category","Key","Value"])
            for cat, rows in data.items():
                if isinstance(rows, dict):
                    for k, v in rows.items():
                        ws.append([cat, str(k), v])
            wb.save(p)
            return str(p)

        raise ValueError(f"Định dạng không hỗ trợ: {fmt}")

   
    # CHỖ ĐÂY ĐỂ NỐI DATA
    def set_user_info(self, username="Username", level_text="Level 1",
                      level_pct=78, streak_n=7, best_n=14):
        ui = self.ui
        ui.label_2.setText(username)
        ui.label_3.setText(level_text)
        ui.label_6.setText(f"{level_pct}%")
        ui.progressBar.setValue(level_pct)
        ui.streak_day.setText(str(streak_n))
        ui.label_15.setText(f"Best: {best_n} days")

    def set_lesson_info(self, unit_name="Unit 3: Travel and culture",
                        done=13, total=20):
        pct = int(done / total * 100) if total else 0
        ui = self.ui
        ui.label_9.setText(unit_name)
        ui.label_progress.setText(f"{done} of {total} exercises")
        ui.label_12.setText(f"{pct}%")
        ui.progressBar_2.setValue(pct)

    def set_weekly_data(self, days: list[str], minutes: list[float]):
        self._days    = days
        self._minutes = minutes
        self._draw()

    def set_vocab_data(self, vocab: dict[str, float]):
        self._vocab = vocab
        mastered = vocab.get("Mastered", 0)
        total    = sum(vocab.values()) or 1
        self.ui.label_analytics.setText(f"{int(mastered/total*100)}%")
        # cập nhật % labels
        mapping = {
            "Mastered":  self.ui.lbl_mastered_pct,
            "Learning":  self.ui.lbl_learning_pct,
            "New Words": self.ui.lbl_new_pct,
        }
        for key, lbl in mapping.items():
            lbl.setText(f"{int(vocab.get(key,0)/total*100)}%")
        self._draw()

    def set_word_of_day(self, word="Serendipity",
                        phonetic="/ˌser.ənˈdɪp.ə.ti/",
                        definition="The occurrence of events by chance in a happy way",
                        example="Finding this app was pure serendipity!"):
        ui = self.ui
        ui.label_23.setText(word)
        ui.label_phienam.setText(phonetic)
        ui.label_defi.setText(definition)
        ui.label_ex2.setText(example)

    def refresh_chart(self):
        """Gọi khi muốn vẽ lại chart thủ công."""
        self._draw()
