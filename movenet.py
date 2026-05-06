from PyQt6.QtCore import QObject, pyqtSignal
import tensorflow as tf
import tensorflow_hub as tf_hub
import joblib
import numpy as np

class Movenet(QObject):
    model_result_signal = pyqtSignal(str, bool) # signal
    
    def __init__(self):
        super().__init__()
        
        # movenet thunder
        self.__model_thunder = None
        self.__size_thunder = None

        self.__mlp_thunder = None
        self.__mlp_scaler_thunder = None

        self.__categories = {'head_left': "Голова наклонена влево"
                             , 'head_right': "Голова наклонена вправо"
                             , 'correct': "Осанка ровная"
                             , 'bend_over': "Осанка сутулая"
                             , 'body_left': "Тело наклонено влево"
                             , 'body_right': "Тело наклонено вправо"
                             , 'tilt_back': "Тело отклонено назад"
                             , 'too_close': "Близко к экрану"}
        
        self.__image_path = None

    def start(self):
        # movenet thunder
        #self.__model_thunder = tf_hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
        self.__model_thunder = tf_hub.load('model/movenet_model')
        self.__size_thunder = 256

        self.__mlp_thunder = joblib.load('model/mlp_thunder.joblib')
        self.__mlp_scaler_thunder = joblib.load('model/scaler_thunder.joblib')
        
    def __detection(self, image_path, model, input_size):
        if image_path:
            image = tf.io.read_file(image_path)
            image = tf.image.decode_jpeg(image)
            img = tf.expand_dims(image, axis=0)
            resized_img = tf.image.resize_with_pad(img, input_size, input_size)
            img_np = resized_img.numpy().astype(np.int32)
            output = model.signatures["serving_default"](tf.constant(img_np))
            keypoints = output['output_0'].numpy()
            return keypoints
        return


    def __make_predictions(self, model, model_size, image_path): # get model points
        pairs_xy = []
        if image_path:
            photo_keypoints = self.__detection(image_path, model, model_size)
            input_image = tf.io.read_file(image_path)
            input_image = tf.image.decode_jpeg(input_image)
            height, width, _ = input_image.shape
            if (len(photo_keypoints.shape) == 4):
                resized_x = photo_keypoints[0, 0, :, 1] * width
                resized_y = photo_keypoints[0, 0, :, 0] * height
            elif (len(photo_keypoints.shape) == 3):
                print(photo_keypoints)
                print(photo_keypoints[0, :, 0])
                print(photo_keypoints[0, :, 1])
                resized_x = photo_keypoints[0, :, 1] * width
                resized_y = photo_keypoints[0, :, 0] * height
            for i in range(0, 7):
                pairs_xy.append((resized_x[i], resized_y[i]))
            return (pairs_xy)
        
        return


    def __check_mlp_on_test_ds(self, mlp, scaler):
        # MoveNet predictions on new photos in necessary format
        path_example = self.__image_path # photo
        if path_example and self.__model_thunder and self.__size_thunder:
            arr_new_photos = []
            photos_kpts = self.__make_predictions(self.__model_thunder, self.__size_thunder, path_example)
            arr_new_photos.append(photos_kpts)

            # cut test photo coordinates to 7
            X_test = []
            for x in arr_new_photos:
                arr_new = [tuple(float(a) for a in b) for b in x]
                for i in range(0, len(arr_new), 7):
                    arr_seven = []
                    arr_seven = arr_new[i:i+7]
                    X_new = []
                    for x_coord, y_coord in arr_seven:
                        X_new.append(x_coord)
                        X_new.append(y_coord)
                    X_test.append(X_new)

            # checking predicted category for a new photo
            y_pred_arr = []
            for frame in X_test:
                features = np.array(frame).reshape(1, -1)
                X_new_scaled = scaler.transform(features)
                pred_new = mlp.predict(X_new_scaled)
                y_pred_arr.append(pred_new.item())
                # prob_new = mlp.predict_proba(X_new_scaled)

            return y_pred_arr
        
        return

    def get_model_result(self, photo_path): # slot for photo
        is_correct_pose = False
        self.__image_path = photo_path
        if self.__mlp_thunder and self.__mlp_scaler_thunder:
            pred_thunder = self.__check_mlp_on_test_ds(self.__mlp_thunder, self.__mlp_scaler_thunder)
            for i, (key, value) in enumerate(self.__categories.items()):
                if (pred_thunder[0] == i):
                    #print(f"Thunder model prediction: {key}")
                    if (key == "correct"):
                        is_correct_pose = True
                    self.model_result_signal.emit(value, is_correct_pose) # send a signal