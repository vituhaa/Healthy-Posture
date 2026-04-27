from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout
from constants import MENU_WIDTH

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(MENU_WIDTH)
        
        self.__tab_manager = QListWidget(self)
        self.__init_tabs()
        self.__create_main_layout()
        
    def __init_tabs(self):
        tabs = ["Главное окно", "Профилактика", "Аналитика", "О себе", "Настройки"]
        self.__tab_manager.addItems(tabs)
        
    def __create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.__tab_manager)
        self.setLayout(layout)
        
    def set_current_tab(self, index):
        self.__tab_manager.setCurrentRow(index)
        
    def connect_tab_changed(self, slot):
        self.__tab_manager.currentRowChanged.connect(slot)
        
        
        