from PyQt6.QtCore import QObject, QFile
import json

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
            "weelky_posture_stat": None,
            "weekly_hours_stat": None,
            "daily_posture_time_stat": None
        }
        if len(self.__data["month_stat"]) > 31:
            first_day = self.get_first_day_key()
            self.remove_day(first_day)
        
    def remove_day(self, day_key):
        if day_key in self.__data["month_stat"]:
            del self.__data["month_stat"][day_key]
            
    def get_first_day_key(self):
        return next(iter(self.__data["month_stat"]))