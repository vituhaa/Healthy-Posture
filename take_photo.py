import cv2

camera = cv2.VideoCapture(0) # default camera

while True:
    retval, image = camera.read() # get an image
    
    if retval:
        cv2.imwrite("photos/photo.png", image) # save an image in a file by path
    else:
        print("Failed to take a photo")
        break
        
    cv2.waitKey(5000) # wait before the next frame



