from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from constants import PHOTO_SIZE
class PhotoFrame(QLabel):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.adjustSize() # widget has photo size
        
    def set_photo(self, photo_path):
        pixmap = QPixmap(photo_path)
        
        scaled_pixmap = pixmap.scaled(PHOTO_SIZE
                                      , Qt.AspectRatioMode.KeepAspectRatio  # save proportions
                                      , Qt.TransformationMode.SmoothTransformation)
        
        self.setPixmap(scaled_pixmap)
        
    def set_border_color(self, color):
        self.setStyleSheet(f"border: 5px solid {color.name()};")