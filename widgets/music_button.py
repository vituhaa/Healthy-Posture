from PyQt6.QtWidgets import QRadioButton
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QFile, pyqtSignal

class MusicButton(QRadioButton):
    music_checked = pyqtSignal(str)
    def __init__(self, path_to_music_file):
        super().__init__()
        
        self.__file = QFile(path_to_music_file)
        if self.__file.exists:
            self.setText(self.__get_file_name(path_to_music_file))
            self.__audio_output = QAudioOutput()
            self.__audio_output.setVolume(1)
            self.__music = QMediaPlayer()
            self.__music.setAudioOutput(self.__audio_output)
            self.__music.setSource(QUrl.fromLocalFile(path_to_music_file))
            self.clicked.connect(lambda: (self.__music.play(),
                                        self.setChecked(True)))
            self.toggled.connect(lambda checked: self.music_checked.emit(path_to_music_file))
        
    def __get_file_name(self, file):
        start_index = 0
        if '/' in file:
            start_index = file.rfind('/') + 1
        elif '\\' in file:
            start_index = file.rfind('\\') + 1
        end_index = file.rfind('.')
        return file[start_index:end_index]
    
    def get_music(self):
        if self.__file.exists():
            return self.__file.fileName()
        else:
            return
        