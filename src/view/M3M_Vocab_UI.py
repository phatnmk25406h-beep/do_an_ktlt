# M3M_Vocab_UI.py  –  M3M English · My Vocabulary
# Matches Figma design exactly (PDF pages 14-18, 37)

from PyQt6 import QtCore, QtGui, QtWidgets
import os
# --- TẠO HÀM LẤY ĐƯỜNG DẪN ẢNH CHUẨN ---
def get_image_path(filename):
    # Lấy đường dẫn thư mục hiện tại của file M3M_Vocab_UI.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Đi lùi lên 2 cấp (view -> src -> Gốc) để tìm thư mục 'trang_tri'
    project_root = os.path.dirname(os.path.dirname(current_dir))
    # Nối đường dẫn lại
    return os.path.join(project_root, "trang_tri", "images", filename)
# ── Figma colours ─────────────────────────────────────────────
G1  = "#4CAF50"   # primary green button
G2  = "#388E3C"   # dark green hover
GL  = "#E8F5E9"   # light green bg
GX  = "#8BC34A"   # yellow-green (gradient stop)
WH  = "#FFFFFF"
BDR = "#E0E0E0"
TXT = "#212121"
SUB = "#757575"
RED = "#F44336"
RDL = "#FFEBEE"
YEL = "#FFC107"

APP_STYLE = f"""
* {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 13px; }}

QMainWindow {{ background: {GL}; }}
QWidget {{ color: {TXT}; }}

/* 1. Ép các trang chính hiển thị màu xanh nhạt */
QWidget#pg_create_bg, QWidget#pg_saved_bg,
QWidget#pg_study_bg, QWidget#pg_done_bg {{ 
    background: {GL}; 
}}

/* 2. Ép ScrollArea và LÕI CỦA NÓ trong suốt để lộ nền xanh nhạt ra */
QScrollArea {{ background: transparent; border: none; }}
QScrollArea QWidget {{ background: transparent; }}

/* 3. Đảm bảo các dòng text không bị tô nền đen */
QLabel {{ background: transparent; }}

/* ── nav bar ── */

/* ── nav bar ── */
QWidget#nav_bar {{
    background: transparent; /* Bỏ màu nền gradient, để lộ nền xanh nhạt ở dưới */
    border: none;
}}
QLabel#nav_logo  {{ color: {TXT}; font-size: 22px; font-weight: bold; }} /* Chữ đen, to hơn */
QLabel#nav_sub   {{ color: {SUB}; font-size: 12px; }} /* Chữ xám */

/* Nút Create (Màu xanh, chữ trắng) */
QPushButton#btn_nav_create {{
    background: {G1}; color: {WH}; border: none;
    border-radius: 8px; font-weight: bold; padding: 8px 20px;
}}
QPushButton#btn_nav_create:hover {{ background: {G2}; }}

/* Nút Saved List (Nền trắng, chữ đen, có viền) */
QPushButton#btn_nav_saved {{
    background: {WH}; color: {TXT}; border: 1px solid {BDR};
    border-radius: 8px; font-weight: bold; padding: 8px 20px;
}}
QPushButton#btn_nav_saved:hover {{ background: {GL}; border: 1px solid {G1}; }}
/* ── page backgrounds ── */
QWidget#pg_create_bg, QWidget#pg_saved_bg,
QWidget#pg_study_bg, QWidget#pg_done_bg  {{ background: {GL}; }}

/* ── white form card ── */
QFrame#form_card {{
    background: {WH}; border-radius: 14px;
    border: 1px solid {BDR};
}}
QLabel#lbl_form_h  {{ font-size: 20px; font-weight: bold; color: {TXT}; }}
QLabel#lbl_form_s  {{ font-size: 12px; color: {SUB}; }}
QLabel#lbl_field   {{ font-weight: bold; font-size: 12px; color: {TXT}; }}
QLabel#lbl_cards_h {{ font-size: 15px; font-weight: bold; color: {TXT}; }}
QLabel#lbl_cnt     {{
    background: {G1}; color: white; border-radius: 11px;
    padding: 2px 10px; font-size: 12px; font-weight: bold;
}}

/* inputs */
QLineEdit {{
    background: {WH}; border: 1.5px solid {BDR}; border-radius: 8px;
    padding: 10px 14px; color: {TXT};
}}
QLineEdit:focus {{ border: 2px solid {G1}; }}
QLineEdit[err=true] {{
    border: 2px solid {RED}; background: {RDL};
    color: {RED};
}}

/* save button */
QPushButton#btn_save_set {{
    background: {G1}; color: white; border: none;
    border-radius: 10px; font-weight: bold;
    font-size: 14px; padding: 10px 26px;
}}
QPushButton#btn_save_set:hover  {{ background: {G2}; }}

/* add card button */
QPushButton#btn_add_card {{
    background: {WH}; color: {G1};
    border: 1.5px solid {BDR}; /* Đổi dashed thành solid, dùng màu xám viền mặc định */
    border-radius: 10px;
    font-size: 15px; font-weight: bold; padding: 14px;
}}
QPushButton#btn_add_card:hover {{ 
    background: {GL}; border: 1.5px solid {G1}; /* Khi di chuột vào thì viền xanh */
}}

/* ── saved-list search ── */
QLineEdit#txt_search_saved {{
    background: {WH}; border: 1.5px solid {BDR}; border-radius: 22px;
    padding: 10px 18px; font-size: 13px;
}}
QComboBox#cmb_sort {{
    background: {WH}; border: 1.5px solid {BDR}; border-radius: 8px;
    padding: 8px 14px;
}}

/* ── collection card ── */
QFrame#coll_card {{
    background: {WH}; border-radius: 12px; border: 1px solid {BDR};
}}
QFrame#coll_card:hover {{ border: 1.5px solid {G1}; }}

/* ── study / word card ── */
QFrame#word_card {{
    background: {WH}; border-radius: 16px; border: 1px solid {BDR};
}}
QLabel#lbl_word_big   {{ font-size: 30px; font-weight: bold; color:{TXT}; }}
QLabel#lbl_phonetic   {{ font-size: 13px; color:{SUB}; font-style:italic; }}
QLabel#lbl_meaning_vi {{ font-size: 22px; font-weight: bold; color:{G1}; }}
QLabel#lbl_example    {{ font-size: 13px; color:{SUB}; font-style:italic; }}

QPushButton#btn_tap_flip {{
    background: {G1}; color: white; border: none;
    border-radius: 10px; font-weight: bold;
    font-size: 15px; padding: 14px;
}}
QPushButton#btn_tap_flip:hover {{ background: {G2}; }}

/* nav prev/next */
QPushButton#btn_fc_prev, QPushButton#btn_fc_next {{
    background: {WH}; color: {TXT}; border: 1.5px solid {BDR};
    border-radius: 8px; padding: 10px 22px;
}}
QPushButton#btn_fc_prev:hover, QPushButton#btn_fc_next:hover {{
    border: 1.5px solid {G1}; color: {G1};
}}

/* progress bar */
QProgressBar {{
    background: #E0E0E0; border-radius: 5px; border: none;
}}
QProgressBar::chunk {{ background: {G1}; border-radius: 5px; }}

/* ── done screen ── */
QLabel#lbl_done_title  {{ font-size: 28px; font-weight: bold; color: {TXT}; }}
QLabel#lbl_done_sub    {{ font-size: 14px; color: {SUB}; }}
QLabel#lbl_pct         {{ font-size: 36px; font-weight: bold; color: {G1}; }}
QPushButton#btn_learn_again {{
    background: {WH}; color: {TXT}; border: 1.5px solid {BDR};
    border-radius: 10px; font-size: 14px; font-weight: bold; padding: 12px 30px;
}}
QPushButton#btn_continue {{
    background: {G1}; color: white; border: none;
    border-radius: 10px; font-size: 14px; font-weight: bold; padding: 12px 30px;
}}
QPushButton#btn_continue:hover {{ background: {G2}; }}

/* general small buttons */
QPushButton {{
    background: {WH}; color: {TXT}; border: 1px solid {BDR};
    border-radius: 7px; padding: 7px 16px;
}}
QPushButton:hover {{ background: {GL}; border: 1px solid {G1}; }}
"""


class Ui_MainWindow(object):
    def setupUi(self, w):
        w.setObjectName("MainWindow")
        w.setWindowTitle("M3M English – My Vocabulary")
        w.resize(1080, 760)
        w.setMinimumSize(900, 640)

        cw = QtWidgets.QWidget(parent=w)
        root = QtWidgets.QVBoxLayout(cw)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        w.setCentralWidget(cw)

        # ── Helpers ──────────────────────────────────────────
        C = QtCore.Qt.AlignmentFlag.AlignCenter
        H = QtWidgets.QHBoxLayout
        V = QtWidgets.QVBoxLayout
        SPH = lambda: QtWidgets.QSpacerItem(1, 1,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum)
        SPV = lambda: QtWidgets.QSpacerItem(1, 1,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding)

        def lbl(parent, name, txt, align=QtCore.Qt.AlignmentFlag.AlignLeft):
            lb = QtWidgets.QLabel(txt, parent=parent)
            lb.setObjectName(name); lb.setAlignment(align)
            return lb

        def btn(parent, name, txt, h=38, w_=0):
            b = QtWidgets.QPushButton(txt, parent=parent)
            b.setObjectName(name)
            b.setMinimumHeight(h)
            if w_: b.setMinimumWidth(w_)
            return b

        def lne(parent, name, ph="", pw=False):
            e = QtWidgets.QLineEdit(parent=parent)
            e.setObjectName(name)
            if ph: e.setPlaceholderText(ph)
            if pw: e.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            return e

        # ══════════════════════════════════════════════════
        # NAV BAR  (persistent top bar)
        # ══════════════════════════════════════════════════
        self.nav_bar = QtWidgets.QWidget(); self.nav_bar.setObjectName("nav_bar")
        self.nav_bar.setFixedHeight(85)
        nl = H(self.nav_bar); nl.setContentsMargins(40, 20, 40, 10); nl.setSpacing(15)

        # 1. Tạo cái nền xanh (my_vocab.png)
        self.lbl_logo_bg = QtWidgets.QLabel(parent=self.nav_bar)
        pixmap_bg = QtGui.QPixmap(get_image_path("my_vocab.png"))
        self.lbl_logo_bg.setPixmap(pixmap_bg.scaled(60, 60, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        
        # 2. Tạo một Layout ảo bên trong cái nền xanh để ép hình quyển sách vào chính giữa
        bg_layout = QtWidgets.QVBoxLayout(self.lbl_logo_bg)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # 3. Tạo hình quyển sách (quyensach.png) đè lên trên
        self.lbl_logo_book = QtWidgets.QLabel(parent=self.lbl_logo_bg)
        pixmap_book = QtGui.QPixmap(get_image_path("quyensach.png"))
        # (Thu nhỏ quyển sách lại cỡ 24x24 cho vừa lọt lòng cái nền 40x40)
        self.lbl_logo_book.setPixmap(pixmap_book.scaled(24, 24, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        
        # 4. Nhét quyển sách vào giữa nền xanh
        bg_layout.addWidget(self.lbl_logo_book)
        
        # 5. Đưa nguyên khối logo hoàn chỉnh vào thanh Nav Bar
        nl.addWidget(self.lbl_logo_bg)

        logo_txt = V(); logo_txt.setSpacing(0)
        self.lbl_nav_logo = lbl(self.nav_bar, "nav_logo", "My Vocabulary")
        self.lbl_nav_sub  = lbl(self.nav_bar, "nav_sub",  "Create, study, and master your word lists")
        logo_txt.addWidget(self.lbl_nav_logo)
        logo_txt.addWidget(self.lbl_nav_sub)
        nl.addLayout(logo_txt); nl.addItem(SPH())

        self.btn_nav_create = btn(self.nav_bar, "btn_nav_create", "Create",      38, 100)
        self.btn_nav_saved  = btn(self.nav_bar, "btn_nav_saved",  "Saved List",  38, 110)
        nl.addWidget(self.btn_nav_create); nl.addWidget(self.btn_nav_saved)
        root.addWidget(self.nav_bar)

        # ══════════════════════════════════════════════════
        # STACK
        # ══════════════════════════════════════════════════
        self.stack = QtWidgets.QStackedWidget()
        root.addWidget(self.stack)

        # ── PAGE 0  CREATE / EDIT ──────────────────────────
        pg0 = QtWidgets.QWidget(); pg0.setObjectName("pg_create_bg")
        self.pg_create = pg0
        sc = QtWidgets.QScrollArea(); sc.setWidgetResizable(True); sc.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        sc_w = QtWidgets.QWidget()
        sc_vl = V(sc_w); sc_vl.setContentsMargins(40, 28, 40, 40); sc_vl.setSpacing(20)
        sc.setWidget(sc_w)
        pg0_l = V(pg0); pg0_l.setContentsMargins(0,0,0,0); pg0_l.setSpacing(0)
        pg0_l.addWidget(sc)

        # form card
        self.form_card = QtWidgets.QFrame(); self.form_card.setObjectName("form_card")
        fc_vl = V(self.form_card); fc_vl.setContentsMargins(32, 28, 32, 28); fc_vl.setSpacing(20)

        # card top row
        top_h = H(); top_h.setSpacing(16)
        # Thêm cái ảnh tròn vào đây
        self.lbl_create_img = QtWidgets.QLabel(parent=self.form_card)
        pixmap_create = QtGui.QPixmap(get_image_path("create_vocab.png"))
        self.lbl_create_img.setPixmap(pixmap_create.scaled(80, 80, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        top_h.addWidget(self.lbl_create_img) # Chèn nó vào Layout ngang đầu tiên
        head_v = V(); head_v.setSpacing(4)
        self.lbl_form_h = lbl(self.form_card, "lbl_form_h", "Create a New Vocabulary Set")
        self.lbl_form_s = lbl(self.form_card, "lbl_form_s", "Build your personalized word collection")
        head_v.addWidget(self.lbl_form_h); head_v.addWidget(self.lbl_form_s)
        self.btn_save_set = btn(self.form_card, "btn_save_set", "  Save Set", 44, 140) # Nhớ bỏ bớt cái emoji cũ đi
        
        # Thêm 2 dòng này:
        icon_save = QtGui.QIcon(get_image_path("save_set.png"))
        self.btn_save_set.setIcon(icon_save)
        # Tùy chỉnh kích thước icon nếu cần
        self.btn_save_set.setIconSize(QtCore.QSize(30, 30))
        top_h.addLayout(head_v); top_h.addItem(SPH()); top_h.addWidget(self.btn_save_set)
        fc_vl.addLayout(top_h)

        # set title
        f1 = V(); f1.setSpacing(6)
        self.lbl_f_title = lbl(self.form_card, "lbl_field", "📖  Set Title *")
        self.txt_set_title = lne(self.form_card, "txt_set_title", "e.g., Business English Essentials")
        self.txt_set_title.setMinimumHeight(44)
        f1.addWidget(self.lbl_f_title); f1.addWidget(self.txt_set_title)
        fc_vl.addLayout(f1)

        # topic
        f2 = V(); f2.setSpacing(6)
        self.lbl_f_topic = lbl(self.form_card, "lbl_field", "💬  Topic / Description *")
        self.txt_topic = lne(self.form_card, "txt_topic", "e.g., Professional vocabulary for workplace communication")
        self.txt_topic.setMinimumHeight(44)
        f2.addWidget(self.lbl_f_topic); f2.addWidget(self.txt_topic)
        fc_vl.addLayout(f2)

        sep = QtWidgets.QFrame(); sep.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        sep.setStyleSheet("color:#E0E0E0;"); fc_vl.addWidget(sep)

        # cards header
        ch = H()
        self.lbl_cards_h = lbl(self.form_card, "lbl_cards_h", "Vocabulary Cards")
        self.lbl_cnt = lbl(self.form_card, "lbl_cnt", "0 cards")
        self.lbl_cnt.setFixedHeight(24)
        self.lbl_cnt.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.lbl_cnt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        ch.addWidget(self.lbl_cards_h); ch.addItem(SPH()); ch.addWidget(self.lbl_cnt)
        fc_vl.addLayout(ch)

        # cards container
        self.cards_widget = QtWidgets.QWidget(parent=self.form_card)
        self.cards_vl = V(self.cards_widget)
        self.cards_vl.setContentsMargins(0,0,0,0); self.cards_vl.setSpacing(14)
        fc_vl.addWidget(self.cards_widget)

        # 1. Khai báo lại nó là một Nút bấm (QPushButton), bỏ cái icon text ⊕ đi
        self.btn_add_card = btn(self.form_card, "btn_add_card", "  Add New Card", 50)
        
        # 2. Chèn cái ảnh icon dấu cộng vào trong nút
        icon_add = QtGui.QIcon(get_image_path("add_card.png"))
        self.btn_add_card.setIcon(icon_add)
        self.btn_add_card.setIconSize(QtCore.QSize(22, 22)) # Bạn có thể chỉnh số này to nhỏ tùy ý
        
        # 3. Thêm nút vào Layout (nhớ đảm bảo nó nằm TRÊN cái lò xo fc_vl.addStretch() nhé)
        fc_vl.addWidget(self.btn_add_card)
        fc_vl.addWidget(self.btn_add_card)
        fc_vl.addStretch()
        sc_vl.addWidget(self.form_card)
        self.stack.addWidget(pg0)

        # ── PAGE 1  SAVED COLLECTIONS ─────────────────────
        pg1 = QtWidgets.QWidget(); pg1.setObjectName("pg_saved_bg")
        self.pg_saved = pg1
        sc2 = QtWidgets.QScrollArea(); sc2.setWidgetResizable(True); sc2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        sc2_w = QtWidgets.QWidget()
        self.saved_vl = V(sc2_w); self.saved_vl.setContentsMargins(32, 24, 32, 32); self.saved_vl.setSpacing(20)
        sc2.setWidget(sc2_w)
        pg1_l = V(pg1); pg1_l.setContentsMargins(0,0,0,0); pg1_l.setSpacing(0)
        pg1_l.addWidget(sc2)

        # --- hero banner ---
        hero = QtWidgets.QFrame()
        # Đổi nền trắng thành trong suốt, bỏ viền để giống thiết kế gốc
        hero.setStyleSheet("background:transparent; border:none;")
        hero.setMinimumHeight(180) 
        hero_vl = V(hero); hero_vl.setAlignment(C); hero_vl.setSpacing(10)

        # 1. Thêm ảnh khủng long
        self.lbl_hero_img = QtWidgets.QLabel(parent=hero)
        pixmap_hero = QtGui.QPixmap(get_image_path("SAVED_COLLECTION.png"))
        self.lbl_hero_img.setPixmap(pixmap_hero.scaledToHeight(150, QtCore.Qt.TransformationMode.SmoothTransformation))
        self.lbl_hero_img.setAlignment(C)

        lbl_hero_h = lbl(hero, "", "Your Saved Collections", C)
        lbl_hero_h.setStyleSheet("font-size:24px; font-weight:bold; color:#212121;")
        lbl_hero_s = lbl(hero, "", "Access all your vocabulary lists in one place. Study, review, and track your progress.", C)
        lbl_hero_s.setStyleSheet("color:#757575; font-size:13px;")
        lbl_hero_s.setWordWrap(True)

        # 2. Xếp ảnh lên trước, rồi mới tới 2 dòng chữ
        hero_vl.addWidget(self.lbl_hero_img) 
        hero_vl.addWidget(lbl_hero_h); hero_vl.addWidget(lbl_hero_s)
        self.saved_vl.addWidget(hero)

        # search + sort
        ss_row = H(); ss_row.setSpacing(12)
        self.txt_search_saved = lne(sc2_w, "txt_search_saved", "🔍  Search your vocabulary lists...")
        self.txt_search_saved.setMinimumHeight(44)
        self.cmb_sort = QtWidgets.QComboBox(parent=sc2_w)
        self.cmb_sort.setObjectName("cmb_sort")
        self.cmb_sort.addItems(["Most Recent", "Alphabetical", "Most Studied"])
        self.cmb_sort.setMinimumHeight(44); self.cmb_sort.setMinimumWidth(160)
        ss_row.addWidget(self.txt_search_saved); ss_row.addWidget(self.cmb_sort)
        self.saved_vl.addLayout(ss_row)

        # grid container (3-column cards added dynamically)
        self.grid_widget = QtWidgets.QWidget(parent=sc2_w)
        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.saved_vl.addWidget(self.grid_widget)

        
        # ── study tips footer ──
        tips_container = QtWidgets.QWidget()
        tips_vl = V(tips_container)
        tips_vl.setContentsMargins(0, 20, 0, 0)
        tips_vl.setSpacing(20)

        # 1. Tiêu đề chính
        lbl_tips_h = lbl(tips_container, "", "Study Tips", C)
        lbl_tips_h.setStyleSheet("font-size:20px; font-weight:bold; color:#212121; border:none; background:transparent;")
        tips_vl.addWidget(lbl_tips_h)

        # 2. Hàng ngang chứa 3 thẻ
        tips_row = H()
        tips_row.setSpacing(20) # Khoảng cách giữa các thẻ

        # Dữ liệu của 3 Tips
        tips_data = [
            ("Review Daily", "Consistent daily practice helps reinforce memory and improve retention."),
            ("Use Flashcards", "Active recall with flashcards is one of the most effective study methods."),
            ("Track Progress", "Monitor your learning journey and celebrate your achievements along the way.")
        ]

        # Vòng lặp tự động tạo 3 thẻ
        for title, desc in tips_data:
            card = QtWidgets.QFrame()
            card.setStyleSheet("background:white; border-radius:12px; border:1px solid #E0E0E0;")
            card_vl = V(card)
            card_vl.setContentsMargins(24, 32, 24, 32) # Canh lề chữ bên trong thẻ
            card_vl.setSpacing(12)
            card_vl.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)

            # Tiêu đề thẻ
            lbl_t = lbl(card, "", title, C)
            lbl_t.setStyleSheet("font-size:15px; font-weight:bold; color:#212121; border:none; background:transparent;")
            
            # Nội dung thẻ
            lbl_d = lbl(card, "", desc, C)
            lbl_d.setStyleSheet("font-size:13px; color:#757575; border:none; background:transparent;")
            lbl_d.setWordWrap(True) # Cho phép rớt dòng nếu chữ quá dài

            card_vl.addWidget(lbl_t)
            card_vl.addWidget(lbl_d)
            tips_row.addWidget(card)

        tips_vl.addLayout(tips_row)
        self.saved_vl.addWidget(tips_container)
        self.stack.addWidget(pg1)

        # ── PAGE 2  FLASHCARD STUDY ───────────────────────
        pg2 = QtWidgets.QWidget(); pg2.setObjectName("pg_study_bg")
        self.pg_study = pg2
        pg2_vl = V(pg2); pg2_vl.setContentsMargins(0,0,0,0); pg2_vl.setSpacing(0)

        # topic header bar
        self.study_hdr = QtWidgets.QWidget()
        self.study_hdr.setStyleSheet("background:white; border-bottom:1px solid #E0E0E0;")
        sh_l = H(self.study_hdr); sh_l.setContentsMargins(24,12,24,12)
        self.lbl_study_topic = lbl(self.study_hdr, "", "🇬🇧  Topic: –")
        f = self.lbl_study_topic.font(); f.setPointSize(14); f.setBold(True)
        self.lbl_study_topic.setFont(f)
        self.btn_close_study = btn(self.study_hdr, "", "✕", 32, 32)
        sh_l.addWidget(self.lbl_study_topic); sh_l.addItem(SPH()); sh_l.addWidget(self.btn_close_study)
        pg2_vl.addWidget(self.study_hdr)

        inner = V(); inner.setContentsMargins(40, 20, 40, 30); inner.setSpacing(16)
        pg2_vl.addLayout(inner)

        self.prog_study = QtWidgets.QProgressBar()
        self.prog_study.setFixedHeight(10); self.prog_study.setTextVisible(False)
        inner.addWidget(self.prog_study)

        # word card
        self.word_card = QtWidgets.QFrame(); self.word_card.setObjectName("word_card")
        self.word_card.setMinimumHeight(340)
        wc_vl = V(self.word_card); wc_vl.setContentsMargins(40,40,40,32); wc_vl.setSpacing(10)
        wc_vl.addItem(SPV())
        self.lbl_word_big   = lbl(self.word_card, "lbl_word_big",   "—",  C)
        self.lbl_phonetic   = lbl(self.word_card, "lbl_phonetic",   "",   C)
        self.lbl_meaning_vi = lbl(self.word_card, "lbl_meaning_vi", "",   C)
        self.lbl_example    = lbl(self.word_card, "lbl_example",    "",   C)
        self.lbl_meaning_vi.setWordWrap(True)
        self.lbl_example.setWordWrap(True)
        for lb in (self.lbl_word_big, self.lbl_phonetic, self.lbl_meaning_vi, self.lbl_example):
            wc_vl.addWidget(lb)
        wc_vl.addItem(SPV())
        inner.addWidget(self.word_card)

        nav_h = H(); nav_h.setSpacing(12)
        self.btn_fc_prev  = btn(pg2, "btn_fc_prev",  "◀  Prev",       44, 120)
        self.lbl_fc_prog  = lbl(pg2, "",             "1 / 10",        C)
        self.lbl_fc_prog.setStyleSheet("font-weight:bold; font-size:14px;")
        self.btn_tap_flip = btn(pg2, "btn_tap_flip", "🔄  TAP TO FLIP", 52)
        self.btn_tap_flip.setMinimumWidth(220)
        self.btn_fc_next  = btn(pg2, "btn_fc_next",  "Next  ▶",       44, 120)
        nav_h.addWidget(self.btn_fc_prev); nav_h.addItem(SPH())
        nav_h.addWidget(self.lbl_fc_prog); nav_h.addItem(SPH())
        nav_h.addWidget(self.btn_tap_flip); nav_h.addItem(SPH())
        nav_h.addWidget(self.btn_fc_next)
        inner.addLayout(nav_h)

        self.stack.addWidget(pg2)

        # ── PAGE 3  LESSON COMPLETE ───────────────────────
        pg3 = QtWidgets.QWidget(); pg3.setObjectName("pg_done_bg")
        self.pg_done = pg3
        pg3_vl = V(pg3); pg3_vl.setAlignment(C); pg3_vl.setContentsMargins(60,40,60,40); pg3_vl.setSpacing(20)

        self.lbl_done_title = lbl(pg3, "lbl_done_title", "Lesson Complete! 🎉", C)
        self.lbl_done_sub   = lbl(pg3, "lbl_done_sub",   "Great job on finishing this lesson", C)
        pg3_vl.addWidget(self.lbl_done_title); pg3_vl.addWidget(self.lbl_done_sub)

        # circular progress (fake it with a styled label)
        circle_frame = QtWidgets.QFrame()
        circle_frame.setFixedSize(160, 160)
        circle_frame.setStyleSheet(f"""
            QFrame {{ background: white; border-radius: 80px;
                      border: 8px solid {G1}; }}
        """)
        cf_vl = V(circle_frame); cf_vl.setAlignment(C)
        self.lbl_pct = lbl(circle_frame, "lbl_pct", "0%", C)
        lbl_comp = lbl(circle_frame, "", "Complete", C)
        lbl_comp.setStyleSheet("color:#757575; font-size:12px;")
        cf_vl.addWidget(self.lbl_pct); cf_vl.addWidget(lbl_comp)
        pg3_vl.addWidget(circle_frame, alignment=C)

        # correct / incorrect boxes
        ci_row = H(); ci_row.setSpacing(20)
        for attr, icon, color, title in [
            ("frame_correct", "✓", G1,  "Correct"),
            ("frame_wrong",   "✗", RED, "Incorrect"),
        ]:
            fr = QtWidgets.QFrame()
            fr.setStyleSheet(f"background:white; border-radius:12px; border:1px solid #E0E0E0;")
            fr.setFixedSize(160, 100)
            fvl = V(fr); fvl.setAlignment(C)
            lic = lbl(fr, "", icon, C); lic.setStyleSheet(f"font-size:24px; color:{color};")
            self.__dict__[f"lbl_done_{attr}_n"] = lbl(fr, "", "0", C)
            self.__dict__[f"lbl_done_{attr}_n"].setStyleSheet("font-size:22px; font-weight:bold;")
            ltit = lbl(fr, "", title, C); ltit.setStyleSheet("color:#757575;")
            fvl.addWidget(lic)
            fvl.addWidget(self.__dict__[f"lbl_done_{attr}_n"])
            fvl.addWidget(ltit)
            setattr(self, attr, fr)
            ci_row.addWidget(fr)
        pg3_vl.addLayout(ci_row)

        # mascot quote card
        quote_fr = QtWidgets.QFrame()
        quote_fr.setStyleSheet(f"background:{GL}; border-radius:12px; border:1px solid #C8E6C9;")
        quote_fr.setFixedHeight(80)
        qh = H(quote_fr); qh.setContentsMargins(20,0,20,0)
        lbl_star = lbl(quote_fr, "", "⭐", C); lbl_star.setStyleSheet("font-size:22px;")
        self.lbl_done_quote = lbl(quote_fr, "", '"Perfect. Keep going!"', C)
        self.lbl_done_quote.setStyleSheet("font-style:italic; color:#388E3C; font-size:14px;")
        qh.addWidget(lbl_star); qh.addWidget(self.lbl_done_quote); qh.addItem(SPH())
        pg3_vl.addWidget(quote_fr)

        btn_row = H(); btn_row.setSpacing(16)
        self.btn_learn_again = btn(pg3, "btn_learn_again", "LEARN AGAIN",  50, 180)
        self.btn_continue    = btn(pg3, "btn_continue",    "CONTINUE",     50, 180)
        btn_row.addItem(SPH()); btn_row.addWidget(self.btn_learn_again); btn_row.addWidget(self.btn_continue); btn_row.addItem(SPH())
        pg3_vl.addLayout(btn_row)

        self.stack.addWidget(pg3)

        w.setStyleSheet(APP_STYLE)
        QtCore.QMetaObject.connectSlotsByName(w)

    def retranslateUi(self, w):
        w.setWindowTitle("M3M English – My Vocabulary")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())