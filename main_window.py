from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from widgets.photo_page import PhotoPage
from widgets.settings_page import SettingsPage
from widgets.main_menu import MainMenu
from notification_manager import NotificationManager
from take_photo import CameraManager
from movenet import Movenet
from constants import MAIN_WINDOW_SIZE, WHITE_COLOR

class MainWindow(QMainWindow):
    stop_requested = pyqtSignal() # signal for stop camera thread
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Healthy Posture")
        self.setMinimumSize(MAIN_WINDOW_SIZE)
        self.setStyleSheet(f"QMainWindow {{ background-color: {WHITE_COLOR.name()} }};")
        
        self.__main_menu = MainMenu()
        self.__photo_page = PhotoPage()
        self.__settings_page = SettingsPage()
        self.__stacked_widget = QStackedWidget() # all tabs
        self.__notification_manager = NotificationManager()
        self.__preventive_notification_timer = QTimer(self)
        
        self.__insert_tabs()
        self.__create_main_layout()
        self.__create_threads()
        self.__add_notifications()
        self.__connect_settings_signals()
        self.__settings_page.set_start_settings()
        
    def __insert_tabs(self):    
        # test tabs widgets
        prevention = QWidget()
        prevention.setStyleSheet("background-color: white;")
        analytics = QWidget()
        analytics.setStyleSheet("background-color: white;")
        about = QWidget()
        about.setStyleSheet("background-color: white;")
        
        # all tabs insertion
        self.__stacked_widget.addWidget(self.__photo_page)
        self.__stacked_widget.addWidget(prevention)
        self.__stacked_widget.addWidget(analytics)
        self.__stacked_widget.addWidget(about)
        self.__stacked_widget.addWidget(self.__settings_page)
        
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
        
    def __create_threads(self):
        # init camera thread
        self.camera_thread = QThread()
        self.camera_manager = CameraManager()
        self.camera_manager.moveToThread(self.camera_thread)
        
        self.camera_thread.started.connect(self.camera_manager.start, Qt.ConnectionType.QueuedConnection)
        
        self.stop_requested.connect(self.camera_manager.stop, Qt.ConnectionType.BlockingQueuedConnection)
        
        self.camera_manager.new_photo_signal.connect(self.__photo_page.set_photo, Qt.ConnectionType.QueuedConnection)
        
        self.camera_thread.finished.connect(self.camera_manager.deleteLater)
        
        # init movenet thread
        self.movenet_thread = QThread()
        self.movenet = Movenet()
        self.movenet.moveToThread(self.movenet_thread)
        
        self.movenet_thread.started.connect(self.movenet.start, Qt.ConnectionType.QueuedConnection)
        
        self.camera_manager.new_photo_signal.connect(self.movenet.get_model_result, Qt.ConnectionType.QueuedConnection)
        
        self.movenet.model_result_signal.connect(self.__photo_page.update_info, Qt.ConnectionType.QueuedConnection)
        self.movenet.model_result_signal.connect(
            lambda answer, is_correct_pose: (
                self.__show_notification("Нарушение осанки", answer)
                if not is_correct_pose
                else None
            ), Qt.ConnectionType.QueuedConnection)
        
        self.movenet_thread.finished.connect(self.movenet.deleteLater)
        
        # run threads
        self.camera_thread.start()
        self.movenet_thread.start()
    
    def __add_notifications(self):
        self.__notification_manager.add_notification_category("Нарушение осанки")
        self.__notification_manager.add_notification_category("Напоминание")
        self.__notification_manager.notification_clicked.connect(lambda: self.__go_to_page(0))
        self.__init_preventive_notification_timer()
            
    def __init_preventive_notification_timer(self):
        self.__preventive_notification_timer.timeout.connect(lambda: self.__show_notification("Напоминание", "Пора отдохнуть"))
        self.__preventive_notification_timer.start(60000) # 60 sec
        
    def __connect_settings_signals(self):
        if self.__settings_page:
            if self.camera_manager:
                self.__settings_page.analysis_frequency_set.connect(self.camera_manager.change_photo_inteval)
            if self.__notification_manager:
                self.__settings_page.posture_music_set.connect(lambda music_file:
                    self.__notification_manager.set_music_notification_category("Нарушение осанки", music_file))
                
                self.__settings_page.preventive_music_set.connect(lambda music_file:
                    self.__notification_manager.set_music_notification_category("Напоминание", music_file))
                
                self.__settings_page.preventive_frequency_set.connect(lambda interval: (
                    self.__preventive_notification_timer.stop(),
                    self.__preventive_notification_timer.start(interval)))
        
    def closeEvent(self, event):
        self.__preventive_notification_timer.stop()
        self.stop_requested.emit()
        self.camera_thread.quit()
        self.camera_thread.wait()
        self.movenet_thread.quit()
        self.movenet_thread.wait()
        
        # remove notification windows
        self.__notification_manager.close_all_notifications()
        self.__notification_manager = None
        event.accept()
    
    def __show_notification(self, category, text):
        if self.__notification_manager:
            self.__notification_manager.show_notification(category, text)
            
    def __go_to_page(self, index):
        self.__main_menu.set_current_tab(index)
        self.showNormal() # show widget if it was minimized
        self.raise_()