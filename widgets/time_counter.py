from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from datetime import datetime, timedelta

class TimeCounter(QWidget):
    time_changed = pyqtSignal(int)
    def __init__(self, hours_need, minutes_need, seconds_need):
        super().__init__()
        self.__hours = None
        self.__minutes = None
        self.__seconds = None
        self.__create_main_layout(hours_need, minutes_need, seconds_need)
        self.__min_time_s = None # in seconds
        self.__max_time_s = None # in seconds
        self.__min_time = None # datetime
        self.__max_time = None # datetime
        
    def __create_main_layout(self, hours_need, minutes_need, seconds_need):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        if hours_need:
            self.__hours = QSpinBox()
            self.__hours.setRange(0, 23)
            hours_label = QLabel("ч.")
            layout.addWidget(self.__hours)
            layout.addWidget(hours_label)
            self.__hours.valueChanged.connect(self.__validate_enter)
            
        if minutes_need:
            self.__minutes = QSpinBox()
            self.__minutes.setRange(0, 59)
            minutes_label = QLabel("мин.")
            layout.addWidget(self.__minutes)
            layout.addWidget(minutes_label)
            self.__minutes.valueChanged.connect(self.__validate_enter)
            
        if seconds_need:
            self.__seconds = QSpinBox()
            self.__seconds.setRange(0, 59)
            seconds_label = QLabel("сек.")
            layout.addWidget(self.__seconds)
            layout.addWidget(seconds_label)
            self.__seconds.valueChanged.connect(self.__validate_enter)
            
        self.setLayout(layout)
        
    def set_interval(self, start_str, end_str): # h:m:s
        if self.__is_correct_time(start_str) and self.__is_correct_time(end_str):
            start_time = datetime.strptime(start_str, '%H:%M:%S')
            end_time = datetime.strptime(end_str, '%H:%M:%S')
            if start_time < end_time:
                self.__min_time_s = self.__time_to_seconds(start_time)
                self.__max_time_s = self.__time_to_seconds(end_time)
                self.__min_time = start_time
                self.__max_time = end_time
                
    def set_value(self, time_str): # h:m:s
        if self.__is_correct_time(time_str):
            time = datetime.strptime(time_str, '%H:%M:%S')
            actual_time = self.__time_to_seconds(time)
            if self.__is_time_in_interval(time):
                if self.__hours:
                    self.__hours.setValue(time.hour)
                if self.__minutes:
                    self.__minutes.setValue(time.minute)
                if self.__seconds:
                    self.__seconds.setValue(time.second)
                self.time_changed.emit(actual_time)
               
    def __is_correct_time(self, time_str):
        try:
            datetime.strptime(time_str, '%H:%M:%S')
            return True
        except ValueError:
            return False
        
    def __is_time_in_interval(self, time):
        total_seconds = self.__time_to_seconds(time)
        if self.__min_time_s and self.__max_time_s:
            if self.__min_time_s <= total_seconds <= self.__max_time_s:
                return True
            return False
        return True
            
    def __validate_enter(self, num):
        time_str = ""
        if self.__hours:
            time_str += f'{self.__hours.value()}:'
        else:
            time_str += '0:'
        if self.__minutes:
            time_str += f'{self.__minutes.value()}:'
        else:
            time_str += '0:'
        if self.__seconds:
            time_str += f'{self.__seconds.value()}'
        else:
            time_str += '0'
        
        time = datetime.strptime(time_str, '%H:%M:%S')
        actual_time = self.__time_to_seconds(time)
        
        if not self.__is_time_in_interval(time):
            time_seconds = self.__time_to_seconds(time) 
            if time_seconds < self.__min_time_s:
                if self.__hours:
                    self.__hours.blockSignals(True)
                    self.__hours.setValue(self.__min_time.hour)
                    self.__hours.blockSignals(False)
                if self.__minutes:
                    self.__minutes.blockSignals(True)
                    self.__minutes.setValue(self.__min_time.minute)
                    self.__minutes.blockSignals(False)
                if self.__seconds:
                    self.__seconds.blockSignals(True)
                    self.__seconds.setValue(self.__min_time.second)
                    self.__seconds.blockSignals(False)
                actual_time = self.__min_time_s
            else:
                if self.__hours:
                    self.__hours.blockSignals(True)
                    self.__hours.setValue(self.__max_time.hour)
                    self.__hours.blockSignals(False)
                if self.__minutes:
                    self.__minutes.blockSignals(True)
                    self.__minutes.setValue(self.__max_time.minute)
                    self.__minutes.blockSignals(False)
                if self.__seconds:
                    self.__seconds.blockSignals(True)
                    self.__seconds.setValue(self.__max_time.second)
                    self.__seconds.blockSignals(False)
                actual_time = self.__max_time_s
        
        self.time_changed.emit(actual_time)    
        
    def __time_to_seconds(self, time):
        return time.hour * 3600 + time.minute * 60 + time.second
    
    def get_total_seconds(self):
        time_str = ""
        if self.__hours:
            time_str += f'{self.__hours.value()}:'
        else:
            time_str += '0:'
        if self.__minutes:
            time_str += f'{self.__minutes.value()}:'
        else:
            time_str += '0:'
        if self.__seconds:
            time_str += f'{self.__seconds.value()}'
        else:
            time_str += '0'
        
        time = datetime.strptime(time_str, '%H:%M:%S')
        return self.__time_to_seconds(time)
    
    def set_total_seconds_value(self, seconds):
        time_str = str(timedelta(seconds=seconds))
        self.set_value(time_str)
        
        