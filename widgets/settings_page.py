from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette
from constants import MAX_PADDING, MIN_PADDING, FONT, WHITE_COLOR
from widgets.time_counter import TimeCounter
from widgets.music_button import MusicButton
from widgets.music_group import MusicGroup
from widgets.switch_button import SwitchButton

class SettingsPage(QWidget):
    analysis_frequency_set = pyqtSignal(int) # in milliseconds
    preventive_frequency_set = pyqtSignal(int) # in milliseconds
    posture_music_set = pyqtSignal(str)
    preventive_music_set = pyqtSignal(str)
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
        self.__posture_notification_switch = None
        self.__posture_music_switch = None
        self.__preventive_notification_switch = None
        self.__preventive_music_switch = None
        
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
        
        posture_layout = QHBoxLayout()
        posture_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        posture_layout.setContentsMargins(0, 0, 0, 0)
        posture_layout.setSpacing(MAX_PADDING)
        
        posture_notification = QLabel("Нарушение осанки")
        posture_notification.setFont(text_font)
        posture_layout.addWidget(posture_notification)
        
        self.__posture_notification_switch = SwitchButton()
        posture_layout.addWidget(self.__posture_notification_switch)
        self.__settings["is_posture_notifications_on"] = self.__posture_notification_switch.get_state()
        self.__posture_notification_switch.switch_button_on.connect(lambda is_on: self.__switch_button_react(is_on, self.__posture_notification_group))
        
        layout.addLayout(posture_layout, 0)
        
        self.__posture_notification_group = self.__create_posture_notification_group()
        layout.addWidget(self.__posture_notification_group, 0, Qt.AlignmentFlag.AlignLeft)
        
        preventive_layout = QHBoxLayout()
        preventive_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        preventive_layout.setContentsMargins(0, 0, 0, 0)
        preventive_layout.setSpacing(MAX_PADDING)
        
        preventive_notification = QLabel("Напоминание о перерыве")
        preventive_notification.setFont(text_font)
        preventive_layout.addWidget(preventive_notification)
        
        self.__preventive_notification_switch = SwitchButton()
        preventive_layout.addWidget(self.__preventive_notification_switch)
        self.__settings["is_preventive_notifications_on"] = self.__preventive_notification_switch.get_state()
        self.__preventive_notification_switch.switch_button_on.connect(lambda is_on: self.__switch_button_react(is_on, self.__preventive_notification_group))
        
        layout.addLayout(preventive_layout, 0)
        
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
        
        sound_layout = QHBoxLayout()
        sound_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sound_layout.setContentsMargins(0, 0, 0, 0)
        sound_layout.setSpacing(MAX_PADDING)
        
        audio_label = QLabel("Звук")
        audio_label.setFont(text_font)
        sound_layout.addWidget(audio_label)
        
        self.__posture_music_switch = SwitchButton()
        sound_layout.addWidget(self.__posture_music_switch)
        self.__settings["is_posture_music_on"] = self.__posture_music_switch.get_state()
        self.__posture_music_switch.switch_button_on.connect(lambda is_on: self.__switch_button_react(is_on, self.__posture_music_widget))
        
        layout.addLayout(sound_layout, 0)
        
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
        
        sound_layout = QHBoxLayout()
        sound_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sound_layout.setContentsMargins(0, 0, 0, 0)
        sound_layout.setSpacing(MAX_PADDING)
        
        audio_label = QLabel("Звук")
        audio_label.setFont(text_font)
        sound_layout.addWidget(audio_label)
        
        self.__preventive_music_switch = SwitchButton()
        sound_layout.addWidget(self.__preventive_music_switch)
        self.__settings["is_preventive_music_on"] = self.__preventive_music_switch.get_state()
        self.__preventive_music_switch.switch_button_on.connect(lambda is_on: self.__switch_button_react(is_on, self.__preventive_music_widget))
        
        layout.addLayout(sound_layout, 0)
        
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
            self.analysis_frequency_set.emit(posture_total_seconds * 1000) # in milliseconds
            
        is_posture_notifications_on = self.__settings["is_posture_notifications_on"]
        if self.__posture_notification_switch.get_state() != is_posture_notifications_on:
            self.__posture_notification_switch.set_state(is_posture_notifications_on)
            
        is_preventive_notifications_on = self.__settings["is_preventive_notifications_on"]
        if self.__preventive_notification_switch.get_state() != is_preventive_notifications_on:
            self.__preventive_notification_switch.set_state(is_preventive_notifications_on)
            
        preventive_total_seconds = self.__settings["preventive_notification_frequency"]
        if self.__preventive_notification_frequency.get_total_seconds() != preventive_total_seconds:
            self.__preventive_notification_frequency.set_total_seconds_value(preventive_total_seconds)
            self.preventive_frequency_set.emit(preventive_total_seconds * 1000) # in milliseconds
        
        is_posture_music_on = self.__settings["is_posture_music_on"]
        if self.__posture_music_switch.get_state() != is_posture_music_on:
            self.__posture_music_switch.set_state(is_posture_music_on)
            
        is_preventive_music_on = self.__settings["is_preventive_music_on"]
        if self.__preventive_music_switch.get_state() != is_preventive_music_on:
            self.__preventive_music_switch.set_state(is_preventive_music_on)
            
        posture_track = self.__settings["posture_music"]
        if self.__posture_music_widget.get_current_track() != posture_track:
            self.__posture_music_widget.set_track(posture_track)
            self.posture_music_set.emit(posture_track)
            
        preventive_track = self.__settings["preventive_music"]
        if self.__preventive_music_widget.get_current_track() != preventive_track:
            self.__preventive_music_widget.set_track(preventive_track)
            self.preventive_music_set.emit(preventive_track)
            
        self.__cancel_button.setEnabled(False)
        self.__apply_button.setEnabled(False)
        
        
    def __settings_changes_apply(self):
        posture_analysis_new = self.__posture_analysis_frequency.get_total_seconds()
        if posture_analysis_new != self.__settings["posture_analysis_frequency"]:
            self.__settings["posture_analysis_frequency"] = posture_analysis_new
            self.analysis_frequency_set.emit(posture_analysis_new * 1000) # in milliseconds
        
        is_posture_notifications_on = self.__posture_notification_switch.get_state()
        if is_posture_notifications_on != self.__settings["is_posture_notifications_on"]:
            self.__posture_notification_switch.set_state(is_posture_notifications_on)
            
        is_preventive_notifications_on = self.__preventive_notification_switch.get_state()
        if is_preventive_notifications_on != self.__settings["is_preventive_notifications_on"]:
            self.__preventive_notification_switch.set_state(is_preventive_notifications_on)
                
        preventive_frequency_new = self.__preventive_notification_frequency.get_total_seconds()
        if  preventive_frequency_new != self.__settings["preventive_notification_frequency"]:
            self.__settings["preventive_notification_frequency"] = preventive_frequency_new
            self.preventive_frequency_set.emit(preventive_frequency_new * 1000) # in milliseconds
        
        is_posture_music_on = self.__posture_music_switch.get_state()
        if is_posture_music_on != self.__settings["is_posture_music_on"]:
            self.__posture_music_switch.set_state(is_posture_music_on)
            
        is_preventive_music_on = self.__preventive_music_switch.get_state()
        if is_preventive_music_on != self.__settings["is_preventive_music_on"]:
            self.__preventive_music_switch.set_state(is_preventive_music_on)
            
        posture_track_new = self.__posture_music_widget.get_current_track()
        if posture_track_new != self.__settings["posture_music"]:
            self.__settings["posture_music"] = posture_track_new
            self.posture_music_set.emit(posture_track_new)
            
        preventive_track_new = self.__preventive_music_widget.get_current_track()
        if preventive_track_new != self.__settings["preventive_music"]:
            self.__settings["preventive_music"] = preventive_track_new
            self.preventive_music_set.emit(preventive_track_new)
            
        self.__cancel_button.setEnabled(False)
        self.__apply_button.setEnabled(False)
        
    def set_start_settings(self):
        self.analysis_frequency_set.emit(self.__settings["posture_analysis_frequency"] * 1000) # in milliseconds
        self.preventive_frequency_set.emit(self.__settings["preventive_notification_frequency"] * 1000) # in milliseconds
        self.posture_music_set.emit(self.__settings["posture_music"])
        self.preventive_music_set.emit(self.__settings["preventive_music"])
        
    def __switch_button_react(self, is_on, widget):
        if is_on:
            widget.show()
        else:
            widget.hide()
        self.__settings_changed()