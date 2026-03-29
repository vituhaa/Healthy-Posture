from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QThread
from widgets.photo_frame import PhotoFrame
from take_photo import CameraManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Healthy Posture")
        self.setMinimumSize(800, 600)
        
        self.__photo_frame = PhotoFrame()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.__photo_frame, Qt.AlignmentFlag.AlignLeft)
        
        self.camera_thread = QThread()
        self.camera_manager = CameraManager()
        self.camera_manager.moveToThread(self.camera_thread)
        
        self.camera_thread.started.connect(self.camera_manager.start)
        self.camera_manager.new_photo_signal.connect(self.__photo_frame.set_photo) # connect signal with slot
        
        self.camera_thread.finished.connect(self.camera_manager.stop)
        
        self.camera_thread.start()
        
    def closeEvent(self, event):
        self.camera_manager.stop()
        self.camera_thread.quit()
        self.camera_thread.wait()
        event.accept()