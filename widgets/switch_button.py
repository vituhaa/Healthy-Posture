from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor
from constants import WHITE_COLOR, GREEN_COLOR, RED_COLOR

class SwitchButton(QWidget):
    switch_button_on = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.__off_button = QPushButton("ВЫКЛ")
        self.__on_button = QPushButton("ВКЛ")
        self.__darker_white = QColor((WHITE_COLOR.darker(101))) # 1.01 times darker
        self.__lighter_black = QColor((WHITE_COLOR.darker(120))) # 1.2 times darker
        self.__create_main_layout()
        
    def __create_main_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
         
        layout.addWidget(self.__off_button)
        layout.addWidget(self.__on_button)
        
        self.setLayout(layout)
        
        self.__off_button.clicked.connect(self.__push_off)
        self.__on_button.clicked.connect(self.__push_on)
        self.__push_on()
        
    def __push_on(self):
        self.__on_button.setEnabled(False)
        self.__off_button.setEnabled(True)
        self.__on_button.setStyleSheet(f"QPushButton {{ background-color: {GREEN_COLOR.name()}; }}")
        self.__off_button.setStyleSheet(f"QPushButton {{ background-color: {WHITE_COLOR.name()}; color: black; }}"
                                        f"QPushButton::hover {{ background-color: {self.__darker_white.name()}; color: black; }}"
                                        f"QPushButton::pressed {{ background-color: {WHITE_COLOR.name()}; color: {self.__lighter_black.name()} }}")
        self.switch_button_on.emit(True)
        
    def __push_off(self):
        self.__off_button.setEnabled(False)
        self.__on_button.setEnabled(True)
        self.__off_button.setStyleSheet(f"QPushButton {{ background-color: {RED_COLOR.name()}; }}")
        self.__on_button.setStyleSheet(f"QPushButton {{ background-color: {WHITE_COLOR.name()}; color: black; }}"
                                       f"QPushButton::hover {{ background-color: {self.__darker_white.name()}; color: black; }}"
                                        f"QPushButton::pressed {{ background-color: {WHITE_COLOR.name()}; color: {self.__lighter_black.name()} }}")
        self.switch_button_on.emit(False)
    
    def get_state(self):
        return not self.__on_button.isEnabled()
       
    def set_state(self, is_on):
        if is_on:
            self.__push_on()
        else:
            self.__push_off()