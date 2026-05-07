from PyQt6.QtWidgets import QWidget, QVBoxLayout, QButtonGroup
from PyQt6.QtCore import Qt, pyqtSignal
from constants import MAX_PADDING
from widgets.music_button import MusicButton

class MusicGroup(QWidget):
    def __init__(self):
        super().__init__()
        self.__layout = self.__create_main_layout()
        self.setLayout(self.__layout)
        self.__music_group = QButtonGroup()
        self.__button_count = 0
        
    def __create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return layout
    
    def add_music_button(self, music_button):
        self.__music_group.addButton(music_button)
        self.__layout.addWidget(music_button, 0, Qt.AlignmentFlag.AlignLeft)
        self.__button_count += 1
        if self.__button_count == 1:
            music_button.setChecked(True)