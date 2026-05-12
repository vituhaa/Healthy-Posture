from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from constants import MAX_PADDING, FONT

class DaysCounter(QWidget):
    def __init__(self):
        super().__init__()
        self.__title = QLabel("Дней в приложении")
        self.__days_count = QLabel("1")
        self.__create_main_layout()
        
    def __create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        font = QFont(FONT)
        font.setPointSize(12)
        self.__title.setFont(font)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        layout.addWidget(self.__title, 0, Qt.AlignmentFlag.AlignHCenter)
        
        font.setPointSize(24)
        font.setBold(True)
        self.__days_count.setFont(font)
        self.__days_count.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        layout.addWidget(self.__days_count, 0, Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(layout)
        
    def set_count(self, count):
        self.__days_count.setText(str(count))