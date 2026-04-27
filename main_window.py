from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from widgets.photo_page import PhotoPage
from widgets.main_menu import MainMenu
from take_photo import CameraManager
from constants import MAIN_WINDOW_SIZE, WHITE_COLOR

class MainWindow(QMainWindow):
    stop_requested = pyqtSignal() # signal for stop camera thread
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Healthy Posture")
        self.setMinimumSize(MAIN_WINDOW_SIZE)
        self.setStyleSheet(f"background-color: {WHITE_COLOR.name()};")
        
        self.__main_menu = MainMenu()
        self.__photo_page = PhotoPage()
        self.__stacked_widget = QStackedWidget() # all tabs
        
        self.__insert_tabs()
        self.__create_main_layout()
        self.__create_camera_thread()
        
    def __insert_tabs(self):    
        # test tabs widgets
        prevention = QWidget()
        prevention.setStyleSheet("background-color: white;")
        analytics = QWidget()
        analytics.setStyleSheet("background-color: white;")
        about = QWidget()
        about.setStyleSheet("background-color: white;")
        settings = QWidget()
        settings.setStyleSheet("background-color: white;")
        
        # all tabs insertion
        self.__stacked_widget.addWidget(self.__photo_page)
        self.__stacked_widget.addWidget(prevention)
        self.__stacked_widget.addWidget(analytics)
        self.__stacked_widget.addWidget(about)
        self.__stacked_widget.addWidget(settings)
        
    def __create_main_layout(self):
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.__main_menu)
        layout.addWidget(self.__stacked_widget)
        self.setCentralWidget(central_widget)
        
        self.__main_menu.connect_tab_changed(self.__stacked_widget.setCurrentIndex)
        self.__main_menu.set_current_tab(0)
        
    def __create_camera_thread(self):
        self.camera_thread = QThread()
        self.camera_manager = CameraManager()
        self.camera_manager.moveToThread(self.camera_thread)
        
        self.camera_thread.started.connect(self.camera_manager.start, Qt.ConnectionType.QueuedConnection)
        
        self.stop_requested.connect(self.camera_manager.stop, Qt.ConnectionType.QueuedConnection)
        
        self.camera_manager.new_photo_signal.connect(self.__photo_page.set_photo, Qt.ConnectionType.QueuedConnection)
        
        self.camera_thread.finished.connect(self.camera_manager.deleteLater)
        
        self.camera_thread.start()
        
    def closeEvent(self, event):
        self.stop_requested.emit()
        self.camera_thread.quit()
        self.camera_thread.wait()
        event.accept()