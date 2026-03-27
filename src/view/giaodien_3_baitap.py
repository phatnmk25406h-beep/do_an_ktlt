# giaodien.py
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal
import os

#Thêm class khiến cho dòng chữ có thể có sự kiện được ( signal)

class ClickableFrame(QtWidgets.QFrame):
    clicked = pyqtSignal()
    def mousePressEvent(self,event):
        self.clicked.emit() # phát signal "clicked" khi bi nhan
        super().mousePressEvent(event)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "trang_tri", "images")

        # 1. Đường dẫn cho ảnh Flashcard
        path_flashcard = os.path.join(image_dir, "Flashcard.png")
        # Thay QPixmap("images/Flashcard.png") thành QPixmap(path_flashcard)

        # 2. Đường dẫn cho ảnh Điền từ vào chỗ trống
        path_duclo = os.path.join(image_dir, "duc_lo.png")
        # Thay QPixmap("images/duc_lo.png") thành QPixmap(path_duclo)

        # 3. Đường dẫn cho ảnh Xếp thứ tự
        path_xeptu = os.path.join(image_dir, "xep_thu_tu.png")

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        # Nền màu xám nhạt như trong ảnh
        MainWindow.setStyleSheet("background-color: #F4F5F8;")

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout chính của cửa sổ
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(50, 50, 50, 50)
        self.verticalLayout.setSpacing(50)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Layout ngang cho 2 lựa chọn đầu tiên
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.horizontalLayoutTop.setSpacing(150)
        self.horizontalLayoutTop.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # 1. Widget Study Flashcards
        self.widgetFlashcards = self.create_option_widget(
            "Study Flashcards",
            "Engage with interactive cards.",
            path_flashcard,
        )
        self.horizontalLayoutTop.addWidget(self.widgetFlashcards)

        # 2. Widget Fill-in-the-Blanks
        self.widgetFillBlanks = self.create_option_widget(
            "Fill-in-the-Blanks",
            "Test your knowledge.",
            path_duclo,
        )
        self.horizontalLayoutTop.addWidget(self.widgetFillBlanks)

        self.verticalLayout.addLayout(self.horizontalLayoutTop)

        # 3. Widget Sentence Reordering (Căn giữa)
        self.widgetReorder = self.create_option_widget(
            "Sentence Reordering",
            "Arrange words correctly.",
            path_xeptu,
        )
        self.verticalLayout.addWidget(self.widgetReorder, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # 4. Nút Close
        self.btnClose = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnClose.setFixedSize(250, 45)
        font = QtGui.QFont()
        font.setBold(True)
        self.btnClose.setFont(font)
        self.btnClose.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnClose.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2D2D2D;
            }
        """)
        self.btnClose.setText("Close")
        self.verticalLayout.addWidget(self.btnClose, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_option_widget(self, title_text, desc_text, icon_path):
        """Hàm tạo một nhóm chức năng gồm Icon, Tiêu đề và Mô tả"""
        frame = ClickableFrame() # sử dụng class Clickable để bấm được vào chữ
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)

        # Phần Icon (Sử dụng nhãn tròn tạm thời, bạn có thể gán QPixmap vào đây)
        icon_label = QtWidgets.QLabel()
        icon_label.setFixedSize(80, 80)
        icon_label.setStyleSheet("background-color: #E2E8F0; border-radius: 40px;")
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        #Thêm hình ảnh vào
        pixmap = QtGui.QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio,            QtCore.Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        else:
            icon_label.setText("Lỗi ảnh")  # Cảnh báo nếu không tìm thấy đường dẫn ảnh
        # ----------------------------------------------

        layout.addWidget(icon_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        # Tiêu đề
        title_label = QtWidgets.QLabel(title_text)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #111827; margin-top: 10px;")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Mô tả
        desc_label = QtWidgets.QLabel(desc_text)
        desc_label.setStyleSheet("font-size: 13px; color: #6B7280;")
        desc_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Thay đổi con trỏ chuột khi hover qua
        frame.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        return frame

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Menu Ứng Dụng Học Tập"))