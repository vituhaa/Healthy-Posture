from PyQt6.QtWidgets import QToolButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform, QIcon, QColor
from constants import WHITE_COLOR

class ArrowButton(QToolButton):
    def __init__(self):
        super().__init__()
        self.__pixmap = QPixmap("icons/up_down_icon.png")
        self.__is_expanded = False
        self.setIcon(QIcon(self.__pixmap))
        self.__darker_white = QColor((WHITE_COLOR.darker(102))) # 1.02 times darker
        self.setStyleSheet("QToolButton { border: none; }"
                           f"QToolButton:hover {{ background: {self.__darker_white.name()}; }}"
                           f"QToolButton:pressed {{ background: {WHITE_COLOR.name()}; }}")
        self.clicked.connect(self.__rotate_icon)
        
    def __rotate_icon(self):
        self.__is_expanded = not self.__is_expanded
        if self.__is_expanded:
            rotated_pixmap = self.__pixmap.transformed(QTransform().rotate(180))
        else:
            rotated_pixmap = self.__pixmap
        self.setIcon(QIcon(rotated_pixmap))