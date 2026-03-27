from PyQt6.QtWidgets import QMainWindow

from src.controllers.flashcard_controller import FlashcardApp
from src.controllers.fill_blank_controller import FillBlankApp
from src.controllers.reorder_controller import LessonApp
from src.view.giaodien_3_baitap import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, topic_name=None):
        super().__init__()
        self.topic_name = topic_name

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnClose.clicked.connect(self.close)
        self.ui.widgetFlashcards.clicked.connect(self.mo_trang_flashcard)
        self.ui.widgetReorder.clicked.connect(self.mo_trang_sap_xep)
        self.ui.widgetFillBlanks.clicked.connect(self.mo_trang_duc_lo)

    def mo_trang_flashcard(self):
        self.trang_flashcard_ui = FlashcardApp(topic_name=self.topic_name)
        self.trang_flashcard_ui.show()

    def mo_trang_sap_xep(self):
        self.trang_sap_xep_ui = LessonApp(self.topic_name)
        self.trang_sap_xep_ui.show()

    def mo_trang_duc_lo(self):
        self.trang_duc_lo_ui = FillBlankApp(self.topic_name)
        self.trang_duc_lo_ui.show()
