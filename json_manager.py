from PyQt6.QtCore import QObject, QFile
import json
from datetime import datetime, timedelta

class JSonManager(QObject):
    def __init__(self, json_file):
        super().__init__()
        self.__filename = json_file
        self.__file = QFile(self.__filename)
        self.__data = {}
        self.load_data()
        
    def load_data(self):
        if self.__file.exists:
            with open(self.__filename, 'r') as f:
                self.__data = json.load(f)
            
    def save_data(self):
        if self.__file.exists:
            with open(self.__filename, 'w') as f:
                json.dump(self.__data, f, ensure_ascii=False, indent=2)
            
    def get_value(self, key):
        if key in self.__data:
            return self.__data.get(key)
        return
    
    def set_value(self, key, value):
        self.__data[key] = value
        
    def add_new_day_stat(self, day_key):
        self.__data["month_stat"][day_key] = {
            "day_number": None,
            "daily_posture_mark": None,
            "weekly_posture_stat": None,
            "weekly_hours_stat": None,
            "daily_posture_time_stat": None
        }
        if len(self.__data["month_stat"]) > 31:
            first_day = self.get_first_day_key()
            self.remove_day(first_day)
            
        self.__load_weekly_stat(day_key)
        
    def remove_day(self, day_key):
        if day_key in self.__data["month_stat"]:
            del self.__data["month_stat"][day_key]
            
    def get_first_day_key(self):
        return next(iter(self.__data["month_stat"]))
    
    def set_month_stat_value(self, day_key, feature_key, value):
        if day_key in self.__data["month_stat"] and feature_key in self.__data["month_stat"][day_key]:
            self.__data["month_stat"][day_key][feature_key] = value
            
    def get_month_stat_value(self, day_key, feature_key):
        if day_key in self.__data["month_stat"] and feature_key in self.__data["month_stat"][day_key]:
            return self.__data["month_stat"][day_key][feature_key]
        return
            
    def __load_weekly_stat(self, date_str):
        dt = datetime.strptime(date_str, "%d.%m.%Y")
        start = dt - timedelta(days=dt.weekday())
        
        near_dt = dt
        near_date_str = None
        while near_dt >= start:
            date_string = near_dt.strftime("%d.%m.%Y")
            
            if date_string in self.__data["month_stat"] and date_string != date_str:
                near_date_str = date_string
                break
            
            near_dt -= timedelta(days=1)
              
        if near_date_str and near_date_str != date_str:
            self.__data["month_stat"][date_str]["weekly_posture_stat"] = self.get_month_stat_value(near_date_str, "weekly_posture_stat")
            self.__data["month_stat"][date_str]["weekly_hours_stat"] = self.get_month_stat_value(near_date_str, "weekly_hours_stat")
        else:
            self.__data["month_stat"][date_str]["weekly_posture_stat"] = [0, 0, 0, 0, 0, 0, 0]
            self.__data["month_stat"][date_str]["weekly_hours_stat"] = [0, 0, 0, 0, 0, 0, 0]