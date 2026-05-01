from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import cv2

class CameraManager(QObject):
    new_photo_signal = pyqtSignal(str) # signal
    
    def __init__(self):
        super().__init__()
        self.camera = None
        self.timer = None
        self.__photo_counter = 0
        
    def start(self):
        self.camera = cv2.VideoCapture(0) # default camera   
        self.take_photo() # first photo
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.take_photo) # connect function with timer
        self.timer.start(5000) # 5 seconds delay
        
    def stop(self):
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        
        if self.camera:
            self.camera.release() # close a camera
            self.camera = None
        
    def take_photo(self):
        if not self.camera:
            return
        
        retval, image = self.camera.read() # get an image
            
        if retval:
            self.__photo_counter += 1
            photo_path = f"photos/photo_{self.__photo_counter}.jpg"
            cv2.imwrite(photo_path, image) # save an image in a file by path
            self.new_photo_signal.emit(photo_path) # send a signal
            
        else:
            print("Failed to take a photo")
            self.stop()



