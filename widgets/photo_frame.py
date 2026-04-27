from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap

from constants import GREEN_COLOR, RED_COLOR
from random import randint

class PhotoFrame(QLabel):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.adjustSize() # widget has photo size
        
    def set_photo(self, photo_path):
        pixmap = QPixmap(photo_path)
        self.setPixmap(pixmap)
        
        # special logic for posture detection
        random_number = randint(0, 1)
        if random_number:
            self.__set_border_color(GREEN_COLOR)
        else:
            self.__set_border_color(RED_COLOR)
        
    def __set_border_color(self, color):
        self.setStyleSheet(f"border: 5px solid {color.name()};")