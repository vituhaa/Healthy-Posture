from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCharts import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush
from datetime import datetime, timedelta
from constants import FONT, GREEN_COLOR

class TimeHistogram(QWidget):
    def __init__(self):
        super().__init__()
        self.__days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self.__time_str = ["01:00:00", "00:40:00", "00:30:00", "00:00:00", "00:10:00", "00:00:00", "00:00:00"] # time per days
        self.__seconds_list = self.__calculate_time_seconds(self.__time_str)
        self.__barset = None
        self.__bar_series = None
        self.__chart = None
        self.__chart_view = None
        self.__axis_y = None
        self.__axis_x = None
        self.__create_main_layout()
        
    def __create_main_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        font = QFont(FONT)
        font.setPointSize(12)
        brush = QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern)
        
        if len(self.__seconds_list) != 0:
            self.__chart = QChart()
            self.__chart.setTitle("Время использования за неделю")
            self.__chart.setTitleFont(font)
            self.__chart.setTitleBrush(brush)
            self.__chart.legend().setVisible(False)
            
            self.__bar_series = QHorizontalBarSeries()
            self.__barset = QBarSet("")
            self.__barset.setLabelFont(font)
            self.__barset.setLabelBrush(brush)
            self.__barset.setColor(GREEN_COLOR)
            
            for i in self.__seconds_list:
                self.__barset << i
                
            self.__bar_series.append(self.__barset)

            self.__bar_series.setLabelsVisible(True)
            self.__bar_series.setLabelsPosition(QHorizontalBarSeries.LabelsPosition.LabelsOutsideEnd)
            self.__bar_series.setLabelsFormat("@value сек.")
            
            self.__chart.addSeries(self.__bar_series)
            
            # OX
            self.__axis_x = QValueAxis()
            self.__axis_x.setRange(0, max(self.__seconds_list) * 1.2) # 20% longer for text
            self.__axis_x.setVisible(False)
            
            self.__chart.addAxis(self.__axis_x, Qt.AlignmentFlag.AlignBottom)
            self.__bar_series.attachAxis(self.__axis_x)
            
            # OY
            self.__axis_y = QBarCategoryAxis()
            self.__axis_y.append(self.__days_of_week)
            self.__axis_y.setLabelsFont(font)
            self.__axis_y.setLabelsBrush(brush)
            
            self.__chart.addAxis(self.__axis_y, Qt.AlignmentFlag.AlignLeft)
            self.__bar_series.attachAxis(self.__axis_y)
            
            self.__chart_view = QChartView(self.__chart)
            
            layout.addWidget(self.__chart_view, 0)
        
        self.setLayout(layout)
        
    def set_values_per_week(self, day_index, list_values):
        self.__barset.remove(0, self.__barset.count())
        self.__time_str = self.__calculate_time_strs(list_values)
        days_of_week = list(self.__days_of_week)
        days_of_week[day_index] += '*' # today
        
        for i in list_values:
            self.__barset << i
        
        self.__axis_x.setRange(0, max(list_values) * 1.2) # 20% longer for text    
        self.__axis_y.clear()
        self.__axis_y.append(days_of_week)
            
    def set_value_for_day(self, day_index, value):
        self.__barset.remove(0, self.__barset.count())
        self.__time_str[day_index] = value
        days_of_week = list(self.__days_of_week)
        days_of_week[day_index] += '*' # today
        
        seconds_value = self.__calculate_time_seconds(self.__time_str)
        for i in seconds_value:
            self.__barset << i
            
        self.__axis_x.setRange(0, max(seconds_value) * 1.2) # 20% longer for text    
        self.__axis_y.clear()
        self.__axis_y.append(days_of_week)
            
    def __calculate_time_seconds(self, list_time_str):
        seconds_list = []
        for i in range (0, len(list_time_str)):
            if self.__is_correct_time(list_time_str[i]):
                time = datetime.strptime(list_time_str[i], '%H:%M:%S')
                seconds_list.append(time.hour * 3600 + time.minute * 60 + time.second)
        return seconds_list
    
    def __calculate_time_strs(self, list_time_seconds):
        time_strs = []
        for seconds in list_time_seconds:
            td = timedelta(seconds=seconds)
            total_seconds = int(td.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            secs = total_seconds % 60
            time_strs.append(f"{hours:02d}:{minutes:02d}:{secs:02d}")
        return time_strs
        
    
    def __is_correct_time(self, time_str):
        try:
            datetime.strptime(time_str, '%H:%M:%S')
            return True
        except ValueError:
            return False