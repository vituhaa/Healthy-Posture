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
        
        self.__settings = {"posture_analysis_frequency": 0 # in seconds
                           , "is_posture_notifications_on": True
                           , "is_posture_music_on": True
                           , "posture_music": "" # path to music file
                           , "is_preventive_notifications_on": True
                           , "preventive_notification_frequency": 0 # in seconds
                           , "is_preventive_music_on": True
                           , "preventive_music": ""} # path to music file
        
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
        self.__settings["posture_analysis_frequency"] = 5
        self.__posture_analysis_frequency.time_changed.connect(lambda time: self.__settings_changed())
        
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
        self.__apply_button.setEnabled(False)
        buttons_layout.addWidget(self.__apply_button)
        self.__apply_button.clicked.connect(self.__settings_changes_apply)
        
        self.__cancel_button = QPushButton("Отменить")
        self.__cancel_button.setEnabled(False)
        buttons_layout.addWidget(self.__cancel_button)
        self.__cancel_button.clicked.connect(self.__settings_changes_cancel)
        
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
        self.__settings["posture_music"] = self.__posture_music_widget.get_current_track()
        self.__posture_music_widget.music_chose.connect(lambda music: self.__settings_changed())
        
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
        self.__settings["preventive_notification_frequency"] = 15 * 60
        self.__preventive_notification_frequency.time_changed.connect(lambda time: self.__settings_changed())
        
        audio_label = QLabel("Звук")
        audio_label.setFont(text_font)
        layout.addWidget(audio_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.__preventive_music_widget = MusicGroup()
        self.__create_music_choice(self.__preventive_music_widget)
        layout.addWidget(self.__preventive_music_widget, 0, Qt.AlignmentFlag.AlignLeft)
        self.__settings["preventive_music"] = self.__preventive_music_widget.get_current_track()
        self.__preventive_music_widget.music_chose.connect(lambda music: self.__settings_changed())
        
        widget.setLayout(layout)
        
        return widget
    
    def __settings_changed(self):
        if not self.__apply_button.isEnabled():
            self.__apply_button.setEnabled(True)
            self.__cancel_button.setEnabled(True)
            
    def __settings_changes_cancel(self):
        posture_total_seconds = self.__settings["posture_analysis_frequency"]
        if self.__posture_analysis_frequency.get_total_seconds() != posture_total_seconds:
            self.__posture_analysis_frequency.set_total_seconds_value(posture_total_seconds)
            
        preventive_total_seconds = self.__settings["preventive_notification_frequency"]
        if self.__preventive_notification_frequency.get_total_seconds() != preventive_total_seconds:
            self.__preventive_notification_frequency.set_total_seconds_value(preventive_total_seconds)
        posture_track = self.__settings["posture_music"]
        if self.__posture_music_widget.get_current_track() != posture_track:
            self.__posture_music_widget.set_track(posture_track)
        preventive_track = self.__settings["preventive_music"]
        if self.__preventive_music_widget.get_current_track() != preventive_track:
            self.__preventive_music_widget.set_track(preventive_track)
        self.__cancel_button.setEnabled(False)
        self.__apply_button.setEnabled(False)
        
        
    def __settings_changes_apply(self):
        posture_analysis_new = self.__posture_analysis_frequency.get_total_seconds()
        if posture_analysis_new != self.__settings["posture_analysis_frequency"]:
            self.__settings["posture_analysis_frequency"] = posture_analysis_new
            
        preventive_frequency_new = self.__preventive_notification_frequency.get_total_seconds()
        if  preventive_frequency_new != self.__settings["preventive_notification_frequency"]:
            self.__settings["preventive_notification_frequency"] = preventive_frequency_new
        posture_track_new = self.__posture_music_widget.get_current_track()
        if posture_track_new != self.__settings["posture_music"]:
            self.__settings["posture_music"] = posture_track_new
        preventive_track_new = self.__preventive_music_widget.get_current_track()
        if preventive_track_new != self.__settings["preventive_music"]:
            self.__settings["preventive_music"] = preventive_track_new
        self.__cancel_button.setEnabled(False)
        self.__apply_button.setEnabled(False)
        
        
        