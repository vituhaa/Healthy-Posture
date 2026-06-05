from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPalette
from datetime import datetime
from widgets.posture_pie_chart import PosturePieChart
from widgets.days_counter import DaysCounter
from widgets.posture_histogram import PostureHistogram
from widgets.time_histogram import TimeHistogram
from widgets.posture_bar_chart import PostureBarChart
from widgets.calendar import Calendar
from json_manager import JSonManager
from constants import MIN_PADDING, MAX_PADDING, WHITE_COLOR

class AnalysisPage(QWidget):
    def __init__(self):
        super().__init__()
        self.__statistics = JSonManager("statistics.json")
        self.__days_in_app = DaysCounter()
        self.__daily_posture_mark = PosturePieChart(30)
        self.__weekly_posture_stat = PostureHistogram()
        self.__weekly_hours_stat = TimeHistogram()
        self.__daily_posture_time_stat = PostureBarChart()
        self.__calendar = Calendar()
        self.__updating_interval = 10 # in model results
        self.__total_results_count = 0
        self.__good_results_count = 0
        self.__bad_results_count = 0
        self.__interval_results_count = 0
        self.__periods_count = 0 # count of intervals for dynamic bar chart
        self.__measurements_count = 0 # count of measurements for 1 period of dynamic bar chart
        self.__periods_count_new = 0 # copy
        self.__measurements_count_new = 0 # copy
        self.__current_periods_count = 0
        self.__current_measurements_count = 0
        self.__period_good_results = 0
        self.__period_time_start = None
        self.__period_time_end = None
        self.__day_of_week = 0
        self.__time_start = None # today using app in seconds
        self.__bar_chart_dict = {} # dict for daily posture time stat
        self.__is_current_stat = True
        self.__create_main_layout()
        self.__update_days_count()
        
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
    
    def __update_days_count(self):
        today = datetime.now()
        date_str = today.strftime("%d.%m.%Y")
        self.__day_of_week = today.weekday()
        self.__time_start = today
        
        days_count = int(self.__statistics.get_value("days_count"))
        
        if self.__statistics.get_value("current_date") != date_str:
            self.__statistics.set_value("current_date", date_str)
            days_count += 1
            self.__statistics.set_value("days_count", days_count)
            self.__statistics.add_new_day_stat(date_str)
            self.__statistics.set_month_stat_value(date_str, "day_number", self.__day_of_week)
            self.__statistics.save_data()
            
        self.__days_in_app.set_count(days_count)
        
        first_date = self.__statistics.get_first_day_key()
        first_date_list = first_date.split(".")
        y_1 = int(first_date_list[2])
        m_1 = int(first_date_list[1])
        d_1 = int(first_date_list[0])
        
        date_list = date_str.split(".")
        y = int(date_list[2])
        m = int(date_list[1])
        d = int(date_list[0])
        self.__calendar.set_date_range(QDate(y_1, m_1, d_1), QDate(y, m, d))
        self.__calendar.set_current_date(QDate(y, m, d))
        
        daily_posture_mark = self.__statistics.get_month_stat_value(date_str, "daily_posture_mark")
        if daily_posture_mark:
            self.__daily_posture_mark.set_posture_mark(daily_posture_mark)
        else:
            self.__daily_posture_mark.set_posture_mark(0)
            
        weekly_posture_stat = self.__statistics.get_month_stat_value(date_str, "weekly_posture_stat")
        if weekly_posture_stat:
            self.__weekly_posture_stat.set_values_per_week(self.__day_of_week, weekly_posture_stat)
            
        weekly_hours_stat = self.__statistics.get_month_stat_value(date_str, "weekly_hours_stat")
        if weekly_hours_stat:
            self.__weekly_hours_stat.set_values_per_week(self.__day_of_week, weekly_hours_stat)
            
        daily_posture_time_stat = self.__statistics.get_month_stat_value(date_str, "daily_posture_time_stat")
        self.__daily_posture_time_stat.set_values_per_interval(daily_posture_time_stat)
        
        self.__total_results_count = self.__statistics.get_month_stat_value(date_str, "total_results")
        self.__good_results_count = self.__statistics.get_month_stat_value(date_str, "good_posture_results")
        
        self.__calendar.date_chose.connect(self.__update_stat_by_date)
            
    def __update_daily_posture_mark(self):
        good_posture_percent = int(self.__good_results_count / self.__total_results_count * 100)
        today = self.__statistics.get_value("current_date")
        self.__statistics.set_month_stat_value(today, "daily_posture_mark", good_posture_percent)
        self.__statistics.set_month_stat_value(today, "total_results", self.__total_results_count)
        self.__statistics.set_month_stat_value(today, "good_posture_results", self.__good_results_count)
        if self.__is_current_stat:
            self.__daily_posture_mark.set_posture_mark(good_posture_percent)
        
    def __update_weekly_posture_stat(self):
        good_posture_percent = int(self.__good_results_count / self.__total_results_count * 100)
        today = self.__statistics.get_value("current_date")
        marks_list = self.__statistics.get_month_stat_value(today, "weekly_posture_stat")
        marks_list[self.__day_of_week] = good_posture_percent
        self.__statistics.set_month_stat_value(today, "weekly_posture_stat", marks_list)
        if self.__is_current_stat:
            self.__weekly_posture_stat.set_value_for_day(self.__day_of_week, good_posture_percent)
        
    def __update_weekly_hours_stat(self):
        time_end = datetime.now()
        delta = time_end - self.__time_start
        seconds_str = str(delta).split('.')[0]
        today = self.__statistics.get_value("current_date")
        hours_list = self.__statistics.get_month_stat_value(today, "weekly_hours_stat")
        hours_list[self.__day_of_week] += int(delta.total_seconds())
        self.__statistics.set_month_stat_value(today, "weekly_hours_stat", hours_list)
        if self.__is_current_stat:
            self.__weekly_hours_stat.set_values_per_week(self.__day_of_week, hours_list)
            
    def __update_stat_by_date(self, date_str):
        today = self.__statistics.get_value("current_date")
        if date_str != today:
            self.__is_current_stat = False
        else:
            self.__is_current_stat = True
            
        day_number = self.__statistics.get_month_stat_value(date_str, "day_number")
        daily_posture_mark = self.__statistics.get_month_stat_value(date_str, "daily_posture_mark")
        daily_posture_time_stat = self.__statistics.get_month_stat_value(date_str, "daily_posture_time_stat")
        weekly_posture_stat = self.__statistics.get_month_stat_value(date_str, "weekly_posture_stat")
        weekly_hours_stat = self.__statistics.get_month_stat_value(date_str, "weekly_hours_stat")
        
        self.__daily_posture_mark.set_posture_mark(daily_posture_mark)
        self.__daily_posture_time_stat.set_values_per_interval(daily_posture_time_stat)
        self.__weekly_posture_stat.set_values_per_week(day_number, weekly_posture_stat)
        self.__weekly_hours_stat.set_values_per_week(day_number, weekly_hours_stat)
            
    def set_updating_interval(self, ms):
        seconds = ms // 1000
        if seconds < 30:
            self.__updating_interval = 10
        elif 30 <= seconds < 60:
            self.__updating_interval = 5
        elif 60 <= seconds < 120:
            self.__updating_interval = 4
        else:
            self.__updating_interval = 3
            
        # for dynamic bar chart
        if seconds <= 60:
            self.__periods_count = 6
            self.__measurements_count = 600 // seconds
        elif 60 < seconds <= 180:
            self.__periods_count = 4
            self.__measurements_count = 5
        elif 180 < seconds <= 240:
            self.__periods_count = 3
            self.__measurements_count = 5
        elif 240 < seconds <= 300:
            self.__periods_count = 3
            self.__measurements_count = 4
        elif 300 < seconds <= 360:
            self.__periods_count = 2
            self.__measurements_count = 4
        else:
            self.__periods_count = 2
            self.__measurements_count = 3
            
        if self.__periods_count_new == 0 and self.__measurements_count_new == 0:
            self.__periods_count_new = self.__periods_count
            self.__measurements_count_new = self.__measurements_count
        
        if self.__periods_count != self.__periods_count_new and self.__measurements_count != self.__measurements_count_new:
            self.__periods_count, self.__periods_count_new = self.__periods_count_new, self.__periods_count
            self.__measurements_count, self.__measurements_count_new = self.__measurements_count_new, self.__measurements_count   
            
        if self.__interval_results_count >= self.__updating_interval:
            self.__interval_results_count = 0
            # update statistics
            self.__update_daily_posture_mark()
            self.__update_weekly_posture_stat()
            self.__update_weekly_hours_stat()
            self.__statistics.save_data()
            
    def update_results_counters(self, is_correct_pose):
        if is_correct_pose:
            self.__good_results_count += 1
        else:
            self.__bad_results_count += 1
        self.__total_results_count += 1
        self.__interval_results_count += 1
        
        if self.__interval_results_count == self.__updating_interval:
            self.__interval_results_count = 0
            # update statistics
            self.__update_daily_posture_mark()
            self.__update_weekly_posture_stat()
            self.__update_weekly_hours_stat()
            self.__statistics.save_data()
        
        if self.__current_periods_count < self.__periods_count:
            if self.__current_measurements_count < self.__measurements_count:
                if self.__current_measurements_count == 0:
                    self.__period_time_start = datetime.now()
                if is_correct_pose:
                    self.__period_good_results += 1
                self.__current_measurements_count += 1
            if self.__current_measurements_count == self.__measurements_count:
                self.__period_time_end = datetime.now()
                timing = self.__period_time_start.strftime("%H:%M") + "-" + self.__period_time_end.strftime("%H:%M")
                percent = self.__period_good_results / self.__current_measurements_count * 100
                self.__bar_chart_dict[timing] = percent
                self.__current_measurements_count = 0
                self.__period_good_results = 0
                self.__period_time_start = None
                self.__period_time_end = None
                self.__current_periods_count += 1
        if self.__current_periods_count == self.__periods_count:
            self.__current_periods_count = 0
            if self.__periods_count_new != self.__periods_count and self.__measurements_count_new != self.__measurements_count:
                self.__periods_count = self.__periods_count_new
                self.__measurements_count = self.__measurements_count_new
            # update dynamic bar chart
            today = self.__statistics.get_value("current_date")
            self.__statistics.set_month_stat_value(today, "daily_posture_time_stat", self.__bar_chart_dict)
            if self.__is_current_stat:
                self.__daily_posture_time_stat.set_values_per_interval(self.__bar_chart_dict)
                self.__bar_chart_dict.clear()
            self.__statistics.save_data()