from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor
from constants import FONT, GREEN_COLOR, WHITE_COLOR

class PosturePieChart(QWidget):
    def __init__(self, percentage_ideal_posture=0):
        super().__init__()
        self.__good_posture_pie_slice = None
        self.__bad_posture_pie_slice = None
        self.__pie_chart = None
        self.__chart_view = None
        self.__create_main_layout(percentage_ideal_posture)
        self.adjustSize()
        
    def __create_main_layout(self, percentage_mark):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        font = QFont(FONT)
        font.setPointSize(12)
        font.setBold(True)
        
        brush = QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern)
        darker_white = QColor((WHITE_COLOR.darker(110)))
        
        self.__good_posture_pie_slice = QPieSlice(f"{percentage_mark}% ровная осанка", percentage_mark)
        self.__good_posture_pie_slice.setColor(GREEN_COLOR)
        self.__good_posture_pie_slice.setLabelFont(font)
        self.__good_posture_pie_slice.setLabelPosition(QPieSlice.LabelPosition.LabelOutside)
        self.__good_posture_pie_slice.setLabelBrush(brush)
        self.__good_posture_pie_slice.setLabelVisible(True)
        
        self.__bad_posture_pie_slice = QPieSlice("", 100 - percentage_mark)
        self.__bad_posture_pie_slice.setColor(darker_white)
        
        font.setBold(False)
        
        self.__pie_chart = QPieSeries()
        self.__pie_chart.append(self.__good_posture_pie_slice)
        self.__pie_chart.append(self.__bad_posture_pie_slice)
        
        self.__chart = QChart()
        self.__chart.setTitle("Оценка ровности осанки")
        self.__chart.setTitleFont(font)
        self.__chart.setTitleBrush(brush)
        self.__chart.addSeries(self.__pie_chart)
        self.__chart.legend().setVisible(False)
        
        self.__chart_view = QChartView(self.__chart)
        
        layout.addWidget(self.__chart_view, 0)
        
        self.setLayout(layout)
        
    def set_posture_mark(self, mark):
        self.__good_posture_pie_slice.setValue(mark)
        self.__bad_posture_pie_slice.setValue(100 - mark)
        self.__good_posture_pie_slice.setLabel(f"{mark}% ровная осанка")