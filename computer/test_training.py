import os, cv2, glob, keras
import numpy as np 
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Lambda
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import Adam, RMSprop
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import confusion_matrix


def get_image(path):
    #img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img_resized = cv2.resize(img, (IMG_ROWS, IMG_COLS))
    return img_resized

def load_train():
    print("Read train images...")
    x_train = []
    y_train = []
    for i in range(3):
        path = os.path.join('..', 'train_data', str(i), '*.jpg')
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
    # path = os.path.join("..", "test_data", "*.jpg")
    # files = glob.glob(path)
    # for fl in files:
    #     img = get_image(fl)
    #     x_test.append(img)
    #     y_test.append(1)
    for i in range(3):
        path = os.path.join('..', 'test_data', str(i), '*.jpg')
        files = glob.glob(path)
        for fl in files:
            img = get_image(fl)
            x_test.append(img)
            y_test.append(i)
    return (x_test, y_test)


def build_model():

    model = Sequential()
    #model.add(Lambda(lambda x: x/127.5-1.0, input_shape=(IMG_COLS, IMG_ROWS, 1)))
    model.add(Conv2D(24, (5, 5), activation='elu', strides=(2, 2), input_shape=(IMG_COLS, IMG_ROWS, 1)))

    model.add(Conv2D(36, (5, 5), activation='elu', strides=(2, 2)))
    model.add(Dropout(0.5)) #########################################################################################

    #model.add(Conv2D(48, (5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    #model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Dropout(0.5))
    model.add(Flatten())
    #model.add(Dense(100, activation='elu'))
    #model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))

    #model.add(Dense(1))
    
    model.add(Dense(NUM_CLASSESS, activation='softmax'))

    model.summary()
    return model


# Config
print("Preparing for train model...")
EPOCHS             = 10
IMG_ROWS, IMG_COLS = 256, 144
NUM_CLASSESS       = 3
CHANNELS           = 1
BATCH_SIZE         = 64

(x_train, y_train) = load_train()
(x_test,  y_test)  = load_test()    
x_train = np.expand_dims(x_train, -1)
x_test  = np.expand_dims(x_test, -1)
x_train = np.array(x_train, dtype=np.float32)
x_test = np.array(x_test, dtype=np.float32)
x_train = x_train / 255.0
x_test  = x_test  / 255.0
y_train = keras.utils.to_categorical(y_train, NUM_CLASSESS)
y_test = keras.utils.to_categorical(y_test, NUM_CLASSESS)


model = build_model()

model.compile(loss='mean_squared_error', optimizer=Adam(lr=1.0e-4))

model.fit(x_train, y_train, epochs=EPOCHS, shuffle=True)

#Save model
model.save('test_model.h5')

# Evaluate model
loss = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', loss)


#confusion_matrix(y_true, y_pred)



# Predict
# img = x_test[2]
# img = img.reshape((1, 128, 128, 1))
# result = model.predict_classes(img)
# print(result)








