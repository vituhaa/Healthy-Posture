from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(200)
        
        self.tab_manager = QListWidget(self)
        tabs = ["Главное окно", "Профилактика", "Аналитика", "О себе", "Настройки"]
        self.tab_manager.addItems(tabs)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.tab_manager)
        self.setLayout(layout)
        
        
        