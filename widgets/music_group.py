from PyQt6.QtWidgets import QWidget, QVBoxLayout, QButtonGroup
from PyQt6.QtCore import Qt, pyqtSignal, QFile
from constants import MAX_PADDING
from widgets.music_button import MusicButton

class MusicGroup(QWidget):
    music_chose = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.__layout = self.__create_main_layout()
        self.setLayout(self.__layout)
        self.__music_group = QButtonGroup()
        self.__button_count = 0
        self.__current_track = None
        self.__music_storage = {}
        
    def __create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return layout
    
    def add_music_button(self, music_button):
        self.__music_group.addButton(music_button)
        self.__layout.addWidget(music_button, 0, Qt.AlignmentFlag.AlignLeft)
        self.__music_storage[music_button.get_music()] = music_button
        music_button.music_checked.connect(self.__current_track_changed)
        self.__button_count += 1
        if self.__button_count == 1:
            music_button.setChecked(True)
            
    def __current_track_changed(self, music_file):
        self.__current_track = music_file
        self.music_chose.emit(music_file)
        
    def get_current_track(self):
        if self.__current_track:
            return self.__current_track
        return
    
    def set_track(self, music_file):
        file = QFile(music_file)
        if file.exists() and music_file in self.__music_storage:
            self.__music_storage[music_file].setChecked(True)
