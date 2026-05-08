from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette
from constants import MAX_PADDING, MIN_PADDING, FONT, WHITE_COLOR
from widgets.time_counter import TimeCounter
from widgets.music_button import MusicButton
from widgets.music_group import MusicGroup

class SettingsPage(QWidget):
    analysis_frequency_set = pyqtSignal(int)
    preventive_frequency_set = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.__posture_analysis_frequency = None
        self.__preventive_notification_frequency = None
        self.__posture_music_widget = None
        self.__preventive_music_widget = None
        self.__posture_notification_group = None
        self.__preventive_notification_group = None
        self.__apply_button = None
        self.__cancel_button = None
        self.__create_main_layout()
        
    def __create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.__create_settings_content())
        scroll_area.setWidgetResizable(True) 
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)        
        
    def __create_settings_content(self):
        widget = QWidget()
        widget.setAutoFillBackground(True) # use own color
        palette = widget.palette() # get current widget palette
        palette.setColor(QPalette.ColorRole.Window, WHITE_COLOR) # background color
        widget.setPalette(palette) # apply
       
        text_font = QFont(FONT)
        text_font.setPointSize(12)
        text_font.setBold(True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(MIN_PADDING, MAX_PADDING, MIN_PADDING, MAX_PADDING)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # main settings sections
        analysis_label = QLabel("Анализ осанки")
        analysis_label.setFont(text_font)
        notification_label = QLabel("Уведомления")
        notification_label.setFont(text_font)
        layout.addWidget(analysis_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        # analysis settings
        text_font.setBold(False)
        frequent_label = QLabel("Частота")
        frequent_label.setFont(text_font)
        layout.addWidget(frequent_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.__posture_analysis_frequency = TimeCounter(False, True, True)
        self.__posture_analysis_frequency.set_interval("0:0:5", "0:10:0")
        self.__posture_analysis_frequency.set_value("0:0:5")
        layout.addWidget(self.__posture_analysis_frequency, 0, Qt.AlignmentFlag.AlignLeft)
        
        # notification settings
        layout.addWidget(notification_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        posture_notification = QLabel("Нарушение осанки")
        posture_notification.setFont(text_font)
        layout.addWidget(posture_notification, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.__posture_notification_group = self.__create_posture_notification_group()
        layout.addWidget(self.__posture_notification_group, 0, Qt.AlignmentFlag.AlignLeft)
        
        preventive_notification = QLabel("Напоминание о перерыве")
        preventive_notification.setFont(text_font)
        layout.addWidget(preventive_notification, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.__preventive_notification_group = self.__create_preventive_notification_group()
        layout.addWidget(self.__preventive_notification_group, 0, Qt.AlignmentFlag.AlignLeft)
        
        # buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(MAX_PADDING)
        
        self.__apply_button = QPushButton("Применить")
        buttons_layout.addWidget(self.__apply_button)
        
        self.__cancel_button = QPushButton("Отменить")
        buttons_layout.addWidget(self.__cancel_button)
        
        layout.addLayout(buttons_layout, 0)
        
        
        widget.setLayout(layout)
        
        return widget
        
            
    def __create_music_choice(self, widget):
        widget.add_music_button(MusicButton("audio/Track1.mp3"))
        widget.add_music_button(MusicButton("audio/Track2.mp3"))
        widget.add_music_button(MusicButton("audio/Track3.mp3"))
        widget.add_music_button(MusicButton("audio/Track4.mp3"))
        
    def __create_posture_notification_group(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        text_font = QFont(FONT)
        text_font.setPointSize(11)
        
        audio_label = QLabel("Звук")
        audio_label.setFont(text_font)
        layout.addWidget(audio_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.__posture_music_widget = MusicGroup()
        self.__create_music_choice(self.__posture_music_widget)
        layout.addWidget(self.__posture_music_widget, 0, Qt.AlignmentFlag.AlignLeft)
        
        widget.setLayout(layout)
        
        return widget
    
    def __create_preventive_notification_group(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        text_font = QFont(FONT)
        text_font.setPointSize(11)
        
        frequent_label = QLabel("Частота")
        frequent_label.setFont(text_font)
        layout.addWidget(frequent_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.__preventive_notification_frequency = TimeCounter(True, True, False)
        self.__preventive_notification_frequency.set_interval("0:15:0", "2:0:0")
        self.__preventive_notification_frequency.set_value("0:15:0")
        layout.addWidget(self.__preventive_notification_frequency, 0, Qt.AlignmentFlag.AlignLeft)
        
        audio_label = QLabel("Звук")
        audio_label.setFont(text_font)
        layout.addWidget(audio_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.__preventive_music_widget = MusicGroup()
        self.__create_music_choice(self.__preventive_music_widget)
        layout.addWidget(self.__preventive_music_widget, 0, Qt.AlignmentFlag.AlignLeft)
        
        widget.setLayout(layout)
        
        return widget
        
        
        
        
        
        
        