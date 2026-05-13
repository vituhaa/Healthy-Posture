from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette
from widgets.posture_pie_chart import PosturePieChart
from widgets.days_counter import DaysCounter
from widgets.posture_histogram import PostureHistogram
from widgets.time_histogram import TimeHistogram
from widgets.posture_bar_chart import PostureBarChart
from widgets.calendar import Calendar
from constants import MIN_PADDING, MAX_PADDING, WHITE_COLOR

class AnalysisPage(QWidget):
    def __init__(self):
        super().__init__()
        self.__days_in_app = DaysCounter()
        self.__daily_posture_mark = PosturePieChart(30)
        self.__weekly_posture_stat = PostureHistogram()
        self.__weekly_hours_stat = TimeHistogram()
        self.__daily_posture_time_stat = PostureBarChart()
        self.__calendar = Calendar()
        self.__create_main_layout()
        
    def __create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.__create_content())
        scroll_area.setWidgetResizable(True) 
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        
    def __create_content(self):
        widget = QWidget()
        widget.setAutoFillBackground(True) # use own color
        palette = widget.palette() # get current widget palette
        palette.setColor(QPalette.ColorRole.Window, WHITE_COLOR) # background color
        widget.setPalette(palette) # apply
        
        layout = QGridLayout()
        layout.setContentsMargins(MIN_PADDING, MAX_PADDING, MIN_PADDING, MAX_PADDING)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        layout.addWidget(self.__days_in_app, 0, 0)
        layout.addWidget(self.__calendar, 0, 1)
        layout.addWidget(self.__daily_posture_time_stat, 1, 0)
        layout.addWidget(self.__daily_posture_mark, 1, 1)
        layout.addWidget(self.__weekly_posture_stat, 2, 0)
        layout.addWidget(self.__weekly_hours_stat, 2, 1)
        
        widget.setLayout(layout)
        
        return widget