from PyQt6.QtCore import QObject, pyqtSignal
import cv2

class CameraManager(QObject):
    new_photo_signal = pyqtSignal(str) # signal
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def start(self):
        camera = cv2.VideoCapture(0) # default camera

        while self.running:
            retval, image = camera.read() # get an image
            
            if retval:
                photo_path = "photos/photo.png"
                cv2.imwrite(photo_path, image) # save an image in a file by path
                self.new_photo_signal.emit(photo_path) # send a signal
                
            else:
                print("Failed to take a photo")
                break
                
            cv2.waitKey(5000) # wait before the next frame
            
        camera.release() # close a camera
        
    def stop(self):
        self.running = False



