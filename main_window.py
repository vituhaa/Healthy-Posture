from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QThread
from widgets.photo_frame import PhotoFrame
from widgets.main_menu import MainMenu
from take_photo import CameraManager

class MainWindow(QMainWindow):
    stop_requested = pyqtSignal() # signal for stop camera thread
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Healthy Posture")
        self.setMinimumSize(800, 600)
        
        self.__main_menu = MainMenu()
        self.__photo_frame = PhotoFrame()
        
        self.__stacked_widget = QStackedWidget() # all tabs
        
        # photo frame widget
        photo_widget = QWidget()
        photo_widget.setStyleSheet("background-color: white;")
        photo_layout = QVBoxLayout(photo_widget)
        photo_layout.setContentsMargins(10, 30, 10, 0)
        photo_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        horizontal_container = QHBoxLayout()
        horizontal_container.addStretch()
        horizontal_container.addWidget(self.__photo_frame)
        horizontal_container.addStretch()
        photo_layout.addLayout(horizontal_container)
        
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
        self.__stacked_widget.addWidget(photo_widget)
        self.__stacked_widget.addWidget(prevention)
        self.__stacked_widget.addWidget(analytics)
        self.__stacked_widget.addWidget(about)
        self.__stacked_widget.addWidget(settings)
        
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.__main_menu)
        layout.addWidget(self.__stacked_widget)
        self.setCentralWidget(central_widget)
        
        self.__main_menu.tab_manager.currentRowChanged.connect(self.__stacked_widget.setCurrentIndex)
        self.__main_menu.tab_manager.setCurrentRow(0)
        
        self.camera_thread = QThread()
        self.camera_manager = CameraManager()
        self.camera_manager.moveToThread(self.camera_thread)
        
        self.camera_thread.started.connect(self.camera_manager.start, Qt.ConnectionType.QueuedConnection)
        
        self.stop_requested.connect(self.camera_manager.stop, Qt.ConnectionType.QueuedConnection)
        
        self.camera_manager.new_photo_signal.connect(self.__photo_frame.set_photo, Qt.ConnectionType.QueuedConnection)
        
        self.camera_thread.finished.connect(self.camera_manager.deleteLater)
        
        self.camera_thread.start()
        
    def closeEvent(self, event):
        self.stop_requested.emit()
        self.camera_thread.quit()
        self.camera_thread.wait()
        event.accept()