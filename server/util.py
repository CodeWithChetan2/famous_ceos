import joblib
import json
import tensorflow as tf
import keras
import numpy as np
import base64
import cv2
from wavelet import w2d

__class_name_to_number = {}
__class_number_to_name = {}

__model = None

def classify_image(image_base64_data, file_path=None):

    imgs = get_cropped_image_if_1_face(file_path, image_base64_data)


    arr=[]
    for img in imgs:
        scaled_img = cv2.resize(img, (224, 224))
        img_har = w2d(img, 'db1', 5)


        len_image_array = (448,224,3)
        scaled_image_har = cv2.resize(img_har, (224, 224))
        scaled_img = scaled_img.reshape(224, 224, 3)  # Reshape scaled_img to (224, 224, 3)

        scaled_image_har = scaled_image_har.reshape(224, 224, 1)
        scaled_image_har = np.repeat(scaled_image_har, 3, axis=2)
        # Reshape scaled_image_har to (224, 224, 1)
        combined_img = np.vstack((scaled_img, scaled_image_har))
        combined_img=combined_img/255.0
        final = combined_img.reshape((1,)+len_image_array)
        result_arr = np.array(__model.predict(final)[0])
        result = np.argmax(result_arr)

        arr.append({
               'class': class_number_to_name(result),
               "class_probability":(__model.predict(final)[0]*100).tolist(),
               "class_dictionary":__class_name_to_number


        })

    return arr

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    with open("./artifacts/ceo_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}

    global __model
    if __model is None:

       __model = tf.keras.models.load_model('./artifacts/imageclassifier.h5')
    print("loading saved artifacts...done")


def get_cv2_image_from_base64_string(b64str):
    '''
    credit: https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    :param uri:
    :return:
    '''
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_image_if_1_face(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(faces) >=1:
                cropped_faces.append(roi_color)
    return cropped_faces

def get_b64_test_image_for_elon_musk():
    with open("./images/sundar_pichai6.jpg") as f:
        return f.read()

if __name__ == '__main__':
    load_saved_artifacts()

    print(classify_image(None, "./test_images/elon_musk25.jpg"))

    # print(classify_image(None, "./test_images/federer1.jpg"))
    # print(classify_image(None, "./test_images/federer2.jpg"))
    # print(classify_image(None, "./test_images/virat1.jpg"))
    # print(classify_image(None, "./test_images/virat2.jpg"))
    # print(classify_image(None, "./test_images/virat3.jpg")) # Inconsistent result could be due to https://github.com/scikit-learn/scikit-learn/issues/13211
    # print(classify_image(None, "./test_images/serena1.jpg"))
    # print(classify_image(None, "./test_images/serena2.jpg"))
    # print(classify_image(None, "./test_images/sharapova1.jpg"))
