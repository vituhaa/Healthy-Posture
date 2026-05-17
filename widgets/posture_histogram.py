from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush
from constants import FONT, GREEN_COLOR

class PostureHistogram(QWidget):
    def __init__(self):
        super().__init__()
        self.__days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self.__results = [10, 30, 50, 0, 80, 0, 0] # percents per days
        self.__barset = None
        self.__bar_series = None
        self.__chart = None
        self.__chart_view = None
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
        
        self.__chart = QChart()
        self.__chart.setTitle("Ровность осанки в течение недели")
        self.__chart.setTitleFont(font)
        self.__chart.setTitleBrush(brush)
        self.__chart.legend().setVisible(False)
        
        self.__bar_series = QBarSeries()
        self.__barset = QBarSet("")
        self.__barset.setLabelFont(font)
        self.__barset.setLabelBrush(brush)
        self.__barset.setColor(GREEN_COLOR)
        
        for i in self.__results:
            self.__barset << i
            
        self.__bar_series.append(self.__barset)

        self.__bar_series.setLabelsVisible(True)
        self.__bar_series.setLabelsPosition(QBarSeries.LabelsPosition.LabelsOutsideEnd)
        self.__bar_series.setLabelsFormat("@value%")
        
        self.__chart.addSeries(self.__bar_series)
        
        # OX
        self.__axis_x = QBarCategoryAxis()
        self.__axis_x.append(self.__days_of_week)
        self.__axis_x.setLabelsFont(font)
        self.__axis_x.setLabelsBrush(brush)
        
        self.__chart.addAxis(self.__axis_x, Qt.AlignmentFlag.AlignBottom)
        self.__bar_series.attachAxis(self.__axis_x)
        
        # OY
        axis_y = QValueAxis()
        max_value = 100 * 1.2
        axis_y.setVisible(False)
        axis_y.setRange(0, max_value)
        
        self.__chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        self.__bar_series.attachAxis(axis_y)
        
        self.__chart_view = QChartView(self.__chart)
        
        layout.addWidget(self.__chart_view, 0)
        
        self.setLayout(layout)
        
    def set_values_per_week(self, list_values):
        self.__barset.remove(0, self.__barset.count())
        self.__results = list_values
        
        for i in self.__results:
            self.__barset << i
            
    def set_value_for_day(self, day_index, value):
        self.__barset.remove(0, self.__barset.count())
        self.__results[day_index] = value
        days_of_week = list(self.__days_of_week)
        days_of_week[day_index] += '*' # today
        
        for i in self.__results:
            self.__barset << i
            
        self.__axis_x.clear()
        self.__axis_x.append(days_of_week)
            
        
            
        
        