from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from widgets.photo_frame import PhotoFrame
from constants import MAX_PADDING, MIN_PADDING

class PhotoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.__photo_frame = PhotoFrame()
        self.__wait_photo_label = QLabel("Настройкка камеры. Пожалуйста, подождите...")
        self.__layout = None
        self.__create_main_layout()
    
    def __create_main_layout(self):    
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(MIN_PADDING, MAX_PADDING, MIN_PADDING, MAX_PADDING)
        self.__layout.setSpacing(MAX_PADDING)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__layout.addWidget(self.__wait_photo_label, 0, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.__layout)
        
    def set_photo(self, photo_path):
        if self.__wait_photo_label and self.__layout:
            if self.__layout.indexOf(self.__wait_photo_label) != -1:
                self.__layout.replaceWidget(self.__wait_photo_label, self.__photo_frame)
                self.__wait_photo_label.hide()
                self.__wait_photo_label = None

        self.__photo_frame.set_photo(photo_path)
        