from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCharts import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush
from datetime import datetime
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
            axis_y = QValueAxis()
            axis_y.setRange(0, max(self.__seconds_list) * 1.2) # 20% longer for text
            axis_y.setVisible(False)
            
            self.__chart.addAxis(axis_y, Qt.AlignmentFlag.AlignBottom)
            self.__bar_series.attachAxis(axis_y)
            
            # OY
            axis_y = QBarCategoryAxis()
            axis_y.append(self.__days_of_week)
            axis_y.setLabelsFont(font)
            axis_y.setLabelsBrush(brush)
            
            self.__chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            self.__bar_series.attachAxis(axis_y)
            
            self.__chart_view = QChartView(self.__chart)
            
            layout.addWidget(self.__chart_view, 0)
        
        self.setLayout(layout)
        
    def set_values_per_week(self, list_values):
        self.__barset.remove(0, self.__barset.count())
        seconds_values = self.__calculate_time_seconds(list_values)
        for i in seconds_values:
            self.__barset << i
            
    def __calculate_time_seconds(self, list_time_str):
        seconds_list = []
        for i in range (0, len(list_time_str)):
            if self.__is_correct_time(list_time_str[i]):
                time = datetime.strptime(list_time_str[i], '%H:%M:%S')
                seconds_list.append(time.hour * 3600 + time.minute * 60 + time.second)
        return seconds_list
    
    def __is_correct_time(self, time_str):
        try:
            datetime.strptime(time_str, '%H:%M:%S')
            return True
        except ValueError:
            return False