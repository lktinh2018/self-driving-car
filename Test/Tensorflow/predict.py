import os
import glob
import cv2
import math
import numpy as np 
import tensorflow as tf
from keras.datasets import mnist
from keras import backend as K
import keras


def get_image(path):
    #img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # resized = cv2.resize(img, (128, 128))
    resized = cv2.resize(img, (img_rows, img_cols))
    return resized

def load_train():
    print("Read train images...")
    x_train = []
    y_train = []
    for i in range(3):
        path = os.path.join('..', '..', 'train_data', str(i), '*.jpg')
        files = glob.glob(path)
        for fl in files:
            img = get_image(fl)
            x_train.append(img)
            y_train.append(i)
    return (x_train, y_train)

def load_test():
    print("Read test images...")
    x_test = []
    y_test = []
    path = os.path.join("..","..", "test_data", "*.jpg")
    files = glob.glob(path)
    for fl in files:
        img = get_image(fl)
        x_test.append(img)
        y_test.append(1)
    return (x_test, y_test)

# Input image dimensions
EPOCHS = 1
img_rows, img_cols = 28, 28
num_classes = 10

(x_train, y_train), (x_test, y_test) = mnist.load_data()
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

new_model = tf.keras.models.load_model('MNIST.h5')
new_model.summary()
loss, acc = new_model.evaluate(x_test, y_test)
print("Restored model, accuracy: {:5.2f}%".format(100*acc))

# print(x_test.shape)
# print(x_test[0].shape)
# result = new_model.predict_classes(x_test, verbose=1)
# print(result)