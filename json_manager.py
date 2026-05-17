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