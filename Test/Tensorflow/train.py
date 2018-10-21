import os
import glob
import cv2
import math
import keras
import numpy as np 
import tensorflow as tf
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Lambda
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import Adam

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
EPOCHS = 10
img_rows, img_cols = 128, 128
num_classes = 3


#(x_train, y_train), (x_test, y_test) = mnist.load_data()
(x_train, y_train) = load_train()
(x_test,  y_test)  = load_test()
x_train = np.expand_dims(x_train, -1)
x_test  = np.expand_dims(x_test, -1)
x_train = np.array(x_train, dtype=np.float32)
x_test = np.array(x_test, dtype=np.float32)
x_train = x_train / 255.0
x_test  = x_test  / 255.0


print(x_train.shape)
#print(y_train)


# Architecture 1
# model = Sequential()
# model.add(Conv2D(32, (3, 3), padding='same',
#                  input_shape=(128, 128, 1)))
# model.add(Activation('relu'))
# model.add(Conv2D(32, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

# model.add(Conv2D(64, (3, 3), padding='same'))
# model.add(Activation('relu'))
# model.add(Conv2D(64, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

# model.add(Flatten())
# model.add(Dense(512))
# model.add(Activation('relu'))
# model.add(Dropout(0.5))
# model.add(Dense(num_classes))
# model.add(Activation('softmax'))

# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])



# Architecture 2
# model = Sequential()
# model.add(Lambda(lambda x: x/127.5 - 1.0,input_shape=(img_rows, img_cols, 3)))
# model.add(Conv2D( 32, (8, 8) , strides=(4, 4), padding="same", activation="relu"))
# model.add(Conv2D( 64, (8, 8) , strides=(4, 4), padding="same", activation="relu"))
# model.add(Conv2D( 128, (8, 8), strides=(2, 2), padding="same", activation="relu"))
# model.add(Conv2D( 128, (2, 2), strides=(1, 1), padding="same", activation="relu"))
# model.add(Flatten())
# model.add(Dropout(0.5))
# model.add(Dense(128))
# model.add(Activation('relu'))
# model.add(Dropout(0.5))
# model.add(Dense(num_classes))
# model.add(Activation('softmax'))
# #model.summary()
#adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
#model.compile(optimizer=adam, loss='mse', metrics=['accuracy'])




model.fit(x_train, y_train, epochs=EPOCHS)



# loss, acc = model.evaluate(x_test, y_test, verbose=1)
# print('Test loss:', loss)
# print('Test accuracy:', acc)


#Save And Load model
# model.save('my_model.h5')
# new_model = tf.keras.models.load_model('my_model.h5')
# new_model.summary()
# loss, acc = new_model.evaluate(x_test, y_test)
# print("Restored model, accuracy: {:5.2f}%".format(100*acc))

# result = new_model.predict(x_test[0], verbose=1)
# print(result)


