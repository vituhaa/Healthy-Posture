import tensorflow as tf
import tensorflow_hub as tf_hub
import joblib
import numpy as np

# модель movenet lightning
model_lightning = tf_hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
size_lightning = 192

mlp_lightning = joblib.load('model/mlp_lightning.joblib')
mlp_scaler_lightning = joblib.load('model/scaler_lightning.joblib')

# модель movenet thunder
model_thunder = tf_hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
size_thunder = 256

mlp_thunder = joblib.load('model/mlp_thunder.joblib')
mlp_scaler_thunder = joblib.load('model/scaler_thunder.joblib')

categories = ['head_left', 'head_right', 'correct', 'bend_over', 'body_left', 'body_right', 'tilt_back', 'too_close']

def detection(image_path, model, input_size):
  image = tf.io.read_file(image_path)
  image = tf.image.decode_jpeg(image)
  img = tf.expand_dims(image, axis=0)
  resized_img = tf.image.resize_with_pad(img, input_size, input_size)
  img_np = resized_img.numpy().astype(np.int32)
  output = model.signatures["serving_default"](tf.constant(img_np))
  keypoints = output['output_0'].numpy()
  return keypoints


def make_predictions(model, model_size, image_path): # подаю датасет, получаю точки от модели
  pairs_xy = []
  photo_keypoints = detection(image_path, model, model_size)
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


def check_mlp_on_test_ds(mlp, scaler):
  # предсказания MoveNet на новых фотографиях, получение данных в нужном формате
  path_example = r'photos/photo_8.jpg' # фото
  arr_new_photos = []
  photos_kpts = make_predictions(model_thunder, size_thunder, path_example)
  arr_new_photos.append(photos_kpts)

  # беру координаты для всех тестовых фотографий, урезаю до 7
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

  # проверка предсказанной категории для каждой новой фотографии
  y_pred_arr = []
  for frame in X_test:
    features = np.array(frame).reshape(1, -1)
    X_new_scaled = scaler.transform(features)
    pred_new = mlp.predict(X_new_scaled)
    y_pred_arr.append(pred_new.item())
    # prob_new = mlp.predict_proba(X_new_scaled)

  return y_pred_arr

# pred_lightning = check_mlp_on_test_ds(mlp_lightning, mlp_scaler_lightning)
# for i in range(len(categories)):
#   if (pred_lightning[0] == i):
#     print(f"Lightning model prediction: {categories[i]}")

pred_thunder = check_mlp_on_test_ds(mlp_thunder, mlp_scaler_thunder)
for i in range(len(categories)):
  if (pred_thunder[0] == i):
    print(f"Thunder model prediction: {categories[i]}")