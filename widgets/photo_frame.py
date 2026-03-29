from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap

from constants import GREEN_COLOR, RED_COLOR

class PhotoFrame(QLabel):
    def __init__(self):
        super().__init__()
        #self.__photoWindow = QLabel(self)
        #self.__photoWindow.setScaledContents(True)
        self.setScaledContents(True) # widget has photo size
        self.set_photo("photos/photo.png")
        self.set_border_color(GREEN_COLOR)
        
    def set_photo(self, photo_path):
        pixmap = QPixmap(photo_path)
        #self.__photoWindow.setPixmap(pixmap)
        self.setPixmap(pixmap)
        
    def set_border_color(self, color):
        #self.__photoWindow.setStyleSheet(f"border: 3px solid {color.};")
        self.setStyleSheet(f"border: 5px solid {color.name()};")