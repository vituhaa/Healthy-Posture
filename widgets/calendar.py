from PyQt6.QtWidgets import QWidget, QLabel, QDateEdit, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from constants import MAX_PADDING, FONT

class Calendar(QWidget):
    def __init__(self):
        super().__init__()
        self.__start_date = QDate(2026, 5, 1)
        self.__end_date = QDate(2026, 5, 31)
        self.__current_date = QDate(2026, 5, 14)
        self.__calendar = None
        self.__title = QLabel("Выберите день для показа статистики")
        self.__show_button = QPushButton("Показать")
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
        
        self.__calendar = QDateEdit(self.__current_date)
        self.__calendar.setDateRange(self.__start_date, self.__end_date)
        self.__calendar.setCalendarPopup(True)
        self.__calendar.dateChanged.connect(self.__update_show_button)
        
        layout.addWidget(self.__calendar, 0, Qt.AlignmentFlag.AlignHCenter)
        
        self.__show_button.setEnabled(False)
        layout.addWidget(self.__show_button, 0, Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(layout)
        
    def set_date_range(self, start, end):
        if self.__calendar:
            self.__calendar.setDateRange(start, end)
        
    def set_current_date(self, date):
        if self.__calendar:
            self.__current_date = date
            self.__calendar.setDate(date)
            
    def __update_show_button(self, date):
        if date != self.__current_date:
            self.__show_button.setEnabled(True)
        else:
            self.__show_button.setEnabled(False)