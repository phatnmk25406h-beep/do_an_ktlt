from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import QPropertyAnimation, QRect, QTimer, pyqtSignal, QEasingCurve
from PyQt6.QtGui import QPainter, QColor, QFont, QLinearGradient
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtProperty

class SplashScreen(QWidget):
    finished = pyqtSignal()  # Báo hiệu xong để chuyển sang page login

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 500) 
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Bỏ thanh tiêu đề cho bớt giả trân
        self.circle_size = 0   # Kích thước ban đầu của animation
        self._start_animation()

    def _start_animation(self):
        self.anim = QPropertyAnimation(self, b"circle_radius")
        self.anim.setStartValue(0)
        self.anim.setEndValue(1200)        # Phình to đến khi che hết màn hình
        self.anim.setDuration(1500)        # 1.5 giây
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)  # Chậm dần ở cuối animation
        self.anim.finished.connect(self._on_finish)
        self.anim.start()

    def _on_finish(self):
        QTimer.singleShot(500, self.finished.emit)  # Chờ 0.5s rồi chuyển màn hình

    @pyqtProperty(int)
    def circle_radius(self):
     return self.circle_size

    @circle_radius.setter
    def circle_radius(self, value):
     self.circle_size = value
     self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set bg trắng
        painter.fillRect(self.rect(), QColor("white"))

        # Vẽ circle ở góc trái bên dứ
        cx, cy = 0, self.height()
        r = self.circle_size
        gradient = QLinearGradient(cx - r, cy - r, cx + r, cy + r)
        gradient.setColorAt(0, QColor("#c8e635"))  
        gradient.setColorAt(1, QColor("#1da830"))  
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        cx, cy = 0, self.height()   # Set tâm 
        r = self.circle_size
        painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        # Hiện logo 
        if self.circle_size > 600:
            painter.setPen(QColor("white"))
            font = QFont("Arial", 28, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "M3M English")