import os
from copy import deepcopy
from datetime import datetime
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QProgressBar,
)

from src.models.vocab_model import VocabRepository
from src.view.giaodien_vocab_ui import Ui_MainWindow, G1, G2, GL, BDR, WH, TXT, SUB
def get_image_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    return os.path.join(project_root, "trang_tri", "images", filename)
PG_CREATE = 0
PG_SAVED = 1
PG_STUDY = 2
PG_DONE = 3


class CardRow(QFrame):
    def __init__(self, parent, index, term="", definition="", on_delete=None):
        super().__init__(parent=parent)
        self._on_delete = on_delete
        self.idx = index

        self.setStyleSheet(
            f"""
            QFrame {{ background:{WH}; border:1px solid {BDR}; border-radius:10px; }}
            """
        )

        main = QVBoxLayout(self)
        main.setContentsMargins(20, 16, 20, 16)
        main.setSpacing(12)

        top = QHBoxLayout()
        self.lbl_n = QLabel(str(index), parent=self)
        self.lbl_n.setFixedWidth(28)
        self.lbl_n.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_n.setStyleSheet(
            f"background:{G1}; color:white; border-radius:9px; font-weight:bold; font-size:11px; padding:2px 0;"
        )

        self.btn_del = QPushButton("🗑", parent=self)
        self.btn_del.setFixedSize(28, 28)
        self.btn_del.setStyleSheet("background:transparent; border:none; color:#F44336; font-size:16px;")
        self.btn_del.clicked.connect(lambda: (on_delete(self) if on_delete else None))

        top.addWidget(self.lbl_n)
        top.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        top.addWidget(self.btn_del)
        main.addLayout(top)

        cols = QHBoxLayout()
        cols.setSpacing(16)

        def _column(label_text, placeholder, field):
            column_layout = QVBoxLayout()
            label = QLabel(label_text, parent=self)
            label.setStyleSheet(f"color:{SUB}; font-size:11px; font-weight:bold; border: none; background: transparent;")
            line_edit = QLineEdit(parent=self)
            line_edit.setPlaceholderText(placeholder)
            line_edit.setText(term if field == "term" else definition)
            line_edit.setMinimumHeight(40)
            setattr(self, f"txt_{field}", line_edit)
            column_layout.addWidget(label)
            column_layout.addWidget(line_edit)
            return column_layout

        cols.addLayout(_column("Term / New Word", "e.g., Collaborate", "term"))
        cols.addLayout(_column("Definition / Meaning", "e.g., Work together on a project", "definition"))
        main.addLayout(cols)

    def set_num(self, number):
        self.idx = number
        self.lbl_n.setText(str(number))

    def data(self):
        return {
            "term": self.txt_term.text().strip(),
            "definition": self.txt_definition.text().strip(),
        }


class CollCard(QFrame):
    def __init__(self, parent, vs, on_study, on_review):
        super().__init__(parent=parent)
        self.setObjectName("coll_card")
        self.setMinimumHeight(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        term_count = len(vs.get("cards", []))
        pct = vs.get("progress_pct", 0)

        top = QHBoxLayout()
        lbl_n = QLabel(f"+ {term_count} terms", parent=self)
        lbl_n.setStyleSheet(f"color:{G1}; font-weight:bold; font-size:12px;")
        progress = QProgressBar(parent=self)
        progress.setRange(0, 100)
        progress.setValue(pct)
        progress.setFixedHeight(6)
        progress.setTextVisible(False)
        progress.setFixedWidth(80)
        lbl_pct = QLabel(f"{pct}%", parent=self)
        lbl_pct.setStyleSheet(f"color:{G1}; font-size:11px; font-weight:bold;")

        top.addWidget(lbl_n)
        top.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        top.addWidget(progress)
        top.addWidget(lbl_pct)
        layout.addLayout(top)

        lbl_title = QLabel(vs.get("title", "Untitled"), parent=self)
        title_font = lbl_title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        lbl_title.setFont(title_font)
        lbl_title.setWordWrap(True)
        layout.addWidget(lbl_title)

        lbl_topic = QLabel(vs.get("topic", ""), parent=self)
        lbl_topic.setStyleSheet(f"color:{SUB}; font-size:12px;")
        lbl_topic.setWordWrap(True)
        layout.addWidget(lbl_topic)

        last_studied = vs.get("last_studied", "Never")
        lbl_last = QLabel(f"⏱  Last studied {last_studied}", parent=self)
        lbl_last.setStyleSheet(f"color:{SUB}; font-size:11px;")
        layout.addWidget(lbl_last)

        action_row = QHBoxLayout()
        # Xóa chữ "✏" đi, để ngoặc kép rỗng
        btn_edit = QPushButton("", parent=self) 
        btn_edit.setFixedSize(34, 34)
        btn_edit.setStyleSheet(f"background:transparent; border:1px solid {BDR}; border-radius:8px;")
        
        # Gắn icon cây bút vào nút
        icon_pen = QIcon(get_image_path("caybut.png"))
        btn_edit.setIcon(icon_pen)
        btn_edit.setIconSize(QSize(16, 16)) # Căn chỉnh kích thước cho vừa vặn
        
        btn_edit.clicked.connect(lambda: on_review(vs, "edit"))

        btn_review = QPushButton("Review", parent=self)
        btn_review.setMinimumHeight(34)
        btn_review.setStyleSheet(f"background:white; color:{TXT}; border:1.5px solid {BDR}; border-radius:8px;")
        btn_review.clicked.connect(lambda: on_review(vs, "review"))

        btn_study = QPushButton("▶  Study", parent=self)
        btn_study.setMinimumHeight(34)
        btn_study.setStyleSheet(f"background:{G1}; color:white; border:none; border-radius:8px; font-weight:bold;")
        btn_study.clicked.connect(lambda: on_study(vs))

        action_row.addWidget(btn_edit)
        action_row.addWidget(btn_review)
        action_row.addWidget(btn_study)
        layout.addLayout(action_row)


class M3M_Vocab_Ext(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_path = os.path.join(base_dir, "data", "vocab_sets.xlsx")
        self.repository = VocabRepository(data_path)

        self._sets = []
        self._editing_id = None
        self._card_rows = []
        self._study_set = None
        self._study_words = []
        self._study_idx = 0
        self._flipped = False

        self._bind()
        self._sets = self.repository.load()
        self._go(PG_CREATE)
        self._open_create()

    def _go(self, page_index):
        self.ui.stack.setCurrentIndex(page_index)

    def _bind(self):
        self.ui.btn_nav_create.clicked.connect(self._open_create)
        self.ui.btn_nav_saved.clicked.connect(self._open_saved)
        self.ui.btn_save_set.clicked.connect(self._save_set)
        self.ui.btn_add_card.clicked.connect(lambda: self._add_row())
        self.ui.txt_search_saved.textChanged.connect(self._filter_saved)
        self.ui.cmb_sort.currentIndexChanged.connect(self._filter_saved)
        self.ui.btn_fc_prev.clicked.connect(self._fc_prev)
        self.ui.btn_fc_next.clicked.connect(self._fc_next)
        self.ui.btn_tap_flip.clicked.connect(self._fc_flip)
        self.ui.btn_close_study.clicked.connect(self._close_study)
        self.ui.btn_learn_again.clicked.connect(self._restart_study)
        self.ui.btn_continue.clicked.connect(self._open_saved)

    def _open_create(self, edit_set=None):
        self._editing_id = edit_set["id"] if edit_set else None
        self._clear_rows()

        if edit_set:
            self.ui.lbl_form_h.setText("✏  Edit Vocabulary Set")
            self.ui.txt_set_title.setText(edit_set.get("title", ""))
            self.ui.txt_topic.setText(edit_set.get("topic", ""))
            for card in edit_set.get("cards", []):
                self._add_row(card.get("term", ""), card.get("definition", ""))
        else:
            self.ui.lbl_form_h.setText("✨  Create a New Vocabulary Set")
            self.ui.txt_set_title.clear()
            self.ui.txt_topic.clear()
            for _ in range(3):
                self._add_row()

        self._update_count()
        self._go(PG_CREATE)
        self.ui.txt_set_title.setFocus()

    def _add_row(self, term="", definition=""):
        row = CardRow(self.ui.cards_widget, len(self._card_rows) + 1, term, definition, on_delete=self._del_row)
        self.ui.cards_vl.addWidget(row)
        self._card_rows.append(row)
        self._update_count()

    def _del_row(self, row):
        if len(self._card_rows) <= 1:
            QMessageBox.information(self, "Info", "Minimum 1 card required.")
            return
        self._card_rows.remove(row)
        row.deleteLater()
        for index, item in enumerate(self._card_rows, start=1):
            item.set_num(index)
        self._update_count()

    def _clear_rows(self):
        for row in self._card_rows:
            row.deleteLater()
        self._card_rows = []

    def _update_count(self):
        count = len(self._card_rows)
        self.ui.lbl_cnt.setText(f"{count} card{'s' if count != 1 else ''}")

    def _set_err(self, widget, is_error, placeholder=""):
        widget.setProperty("err", "true" if is_error else "false")
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        if is_error and placeholder:
            widget.setPlaceholderText(placeholder)

    def _save_set(self):
        title = self.ui.txt_set_title.text().strip()
        topic = self.ui.txt_topic.text().strip()

        valid = True
        if not title:
            self._set_err(self.ui.txt_set_title, True, "⚠ This field is required.")
            valid = False
        else:
            self._set_err(self.ui.txt_set_title, False)

        if not topic:
            self._set_err(self.ui.txt_topic, True, "⚠ This field is required.")
            valid = False
        else:
            self._set_err(self.ui.txt_topic, False)

        if not valid:
            return

        cards = [row.data() for row in self._card_rows if row.data()["term"] or row.data()["definition"]]
        if not cards:
            QMessageBox.warning(self, "Error", "Add at least one vocabulary card.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        updated_sets = deepcopy(self._sets)

        if self._editing_id:
            for vocab_set in updated_sets:
                if vocab_set["id"] == self._editing_id:
                    vocab_set.update({"title": title, "topic": topic, "cards": cards, "updated": now})
                    break
            msg = f"✅ '{title}' updated!"
        else:
            updated_sets.append(
                {
                    "id": VocabRepository.generate_id(),
                    "title": title,
                    "topic": topic,
                    "cards": cards,
                    "created": now,
                    "updated": now,
                    "last_studied": "Never",
                    "progress_pct": 0,
                }
            )
            msg = "🎉 Saved Successfully! 🎊"

        if not self._persist_sets(updated_sets):
            return

        self._show_toast(msg)
        QTimer.singleShot(1400, self._open_saved)

    def _persist_sets(self, updated_sets):
        try:
            self.repository.save(updated_sets)
        except PermissionError:
            QMessageBox.warning(
                self,
                "Save failed",
                "Không thể ghi file Excel vì file đang được ứng dụng khác sử dụng.\n"
                "Hãy đóng file 'vocab_sets.xlsx' rồi thử lại.",
            )
            return False
        except Exception as exc:
            QMessageBox.critical(self, "Save failed", f"Lỗi khi lưu dữ liệu: {exc}")
            return False

        self._sets = updated_sets
        return True

    def _show_toast(self, message):
        toast = QLabel(message, parent=self)
        toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toast.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #8BC34A,stop:1 #4CAF50);"
            "color:white; border-radius:12px; font-size:15px; font-weight:bold; padding:14px 28px;"
        )
        toast.adjustSize()
        toast.move((self.width() - toast.width()) // 2, (self.height() - toast.height()) // 2)
        toast.show()
        QTimer.singleShot(1300, toast.deleteLater)

    def _open_saved(self):
        self._render_grid(self._sets)
        self._go(PG_SAVED)

    def _filter_saved(self):
        query = self.ui.txt_search_saved.text().strip().lower()
        filtered = [
            vocab_set
            for vocab_set in self._sets
            if query in vocab_set.get("title", "").lower() or query in vocab_set.get("topic", "").lower()
        ]

        sort_index = self.ui.cmb_sort.currentIndex()
        if sort_index == 0:
            filtered.sort(key=lambda item: item.get("updated", ""), reverse=True)
        elif sort_index == 1:
            filtered.sort(key=lambda item: item.get("title", "").lower())

        self._render_grid(filtered)

    def _render_grid(self, sets):
        while self.ui.grid_layout.count():
            item = self.ui.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not sets:
            empty_label = QLabel("No vocabulary sets yet.\nClick 'Create' to get started! 🌱")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet(f"color:{SUB}; font-size:14px; padding:40px;")
            self.ui.grid_layout.addWidget(empty_label, 0, 0, 1, 3)
            return

        cols = 3
        for index, vs in enumerate(sets):
            card = CollCard(self.ui.grid_widget, vs, on_study=self._start_study, on_review=self._review_action)
            self.ui.grid_layout.addWidget(card, index // cols, index % cols)

    def _review_action(self, vs, action):
        if action == "edit":
            self._open_create(edit_set=vs)
        elif action == "review":
            reply = QMessageBox.question(
                self,
                "Delete",
                f"Delete '{vs['title']}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                updated_sets = [s for s in self._sets if s["id"] != vs["id"]]
                if not self._persist_sets(updated_sets):
                    return
                self._render_grid(self._sets)

    def _start_study(self, vs):
        cards = vs.get("cards", [])
        if not cards:
            QMessageBox.information(self, "Empty", "No cards in this set.")
            return

        self._study_set = vs
        self._study_words = list(cards)
        self._study_idx = 0
        self._flipped = False

        self.ui.lbl_study_topic.setText(f"🇬🇧  Topic: {vs.get('title', '')}")
        self.ui.prog_study.setMaximum(len(cards))
        self._show_card()
        self._go(PG_STUDY)

    def _show_card(self):
        total = len(self._study_words)
        idx = self._study_idx
        card = self._study_words[idx]

        self._flipped = False
        self.ui.lbl_fc_prog.setText(f"{idx + 1} / {total}")
        self.ui.prog_study.setValue(idx + 1)

        self.ui.lbl_word_big.setText(card.get("term", ""))
        self.ui.lbl_phonetic.setText(card.get("phonetic", ""))
        self.ui.lbl_meaning_vi.setText("")
        self.ui.lbl_example.setText("")
        self.ui.btn_tap_flip.setText("🔄  TAP TO FLIP")
        self.ui.word_card.setStyleSheet(f"QFrame#word_card {{background:{WH}; border-radius:16px; border:1px solid {BDR};}}")

    def _fc_flip(self):
        if not self._study_words:
            return

        card = self._study_words[self._study_idx]
        if not self._flipped:
            self.ui.lbl_meaning_vi.setText(card.get("definition", ""))
            self.ui.lbl_example.setText(card.get("example", ""))
            self.ui.btn_tap_flip.setText("🔄  NEXT WORD")
            self._flipped = True
            self.ui.word_card.setStyleSheet(f"QFrame#word_card {{background:#E8F5E9; border-radius:16px; border:2px solid {G1};}}")
        else:
            self._fc_next()

    def _fc_prev(self):
        if self._study_idx > 0:
            self._study_idx -= 1
            self._show_card()

    def _fc_next(self):
        if self._study_idx < len(self._study_words) - 1:
            self._study_idx += 1
            self._show_card()
        else:
            self._finish_study()

    def _finish_study(self):
        total = len(self._study_words)
        pct = 100
        self.ui.lbl_pct.setText(f"{pct}%")
        self.ui.lbl_done_frame_correct_n.setText(str(total))
        self.ui.lbl_done_frame_wrong_n.setText("0")

        if self._study_set:
            updated_sets = deepcopy(self._sets)
            for vocab_set in updated_sets:
                if vocab_set["id"] == self._study_set["id"]:
                    vocab_set["last_studied"] = "just now"
                    vocab_set["progress_pct"] = pct
                    break
            self._persist_sets(updated_sets)

        self._go(PG_DONE)

    def _restart_study(self):
        if self._study_set:
            self._start_study(self._study_set)

    def _close_study(self):
        self._open_saved()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Exit M3M Vocabulary?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
