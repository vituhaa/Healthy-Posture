from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from widgets.photo_frame import PhotoFrame
from constants import MAX_PADDING, MIN_PADDING, GREEN_COLOR, RED_COLOR, WHITE_COLOR, FONT

class PhotoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.__photo_frame = PhotoFrame()
        self.__wait_photo_label = QLabel("Настройка камеры. Пожалуйста, подождите...")
        self.__text_font = FONT
        self.__info = QLabel()
        self.__layout = None
        self.__create_main_layout()
    
    def __create_main_layout(self):
        self.__text_font.setPointSize(12)
        self.__wait_photo_label.setFont(self.__text_font)  
        self.__info.setFont(self.__text_font)  
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(MIN_PADDING, MAX_PADDING, MIN_PADDING, MAX_PADDING)
        self.__layout.setSpacing(MAX_PADDING)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__wait_photo_label, 0, Qt.AlignmentFlag.AlignHCenter)
        self.__layout.addWidget(self.__info, 0, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.__layout)
        
    def set_photo(self, photo_path): # slot for photo
        if self.__wait_photo_label and self.__layout:
            if self.__layout.indexOf(self.__wait_photo_label) != -1:
                self.__layout.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.__layout.replaceWidget(self.__wait_photo_label, self.__photo_frame)
                self.__wait_photo_label.hide()
                self.__wait_photo_label = None

        self.__photo_frame.set_photo(photo_path)
        self.__clear_info()
        
    def update_info(self, answer, is_correct_pose): # slot for model answer
        if is_correct_pose:
            self.__photo_frame.set_border_color(GREEN_COLOR)
        else:
            self.__photo_frame.set_border_color(RED_COLOR)
        self.__info.setText(answer)
        
    def __clear_info(self):
        self.__photo_frame.set_border_color(WHITE_COLOR)
        self.__info.setText("")