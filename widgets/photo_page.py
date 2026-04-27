from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from widgets.photo_frame import PhotoFrame
from constants import MAX_PADDING, MIN_PADDING

class PhotoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.__photo_frame = PhotoFrame()
        self.__create_main_layout()
    
    def __create_main_layout(self):    
        layout = QVBoxLayout()
        layout.setContentsMargins(MIN_PADDING, MAX_PADDING, MIN_PADDING, MAX_PADDING)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.__photo_frame, 0, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)
        
    def set_photo(self, photo_path):
        self.__photo_frame.set_photo(photo_path)
        