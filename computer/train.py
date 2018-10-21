import os, cv2, glob, keras
import numpy as np 
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Lambda
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import Adam, RMSprop
from keras.callbacks import EarlyStopping, ModelCheckpoint


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
    path = os.path.join("..", "test_data", "*.jpg")
    files = glob.glob(path)
    for fl in files:
        img = get_image(fl)
        x_test.append(img)
        y_test.append(1)
    return (x_test, y_test)

def build_model():

    model = Sequential()
    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=(IMG_ROWS, IMG_COLS, 1)))
    model.add(Conv2D(24, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(36, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(48, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(64, 3, 3, activation='elu'))
    model.add(Conv2D(64, 3, 3, activation='elu'))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    #model.add(Dense(1))
    
    model.add(Dense(NUM_CLASSESS, activation='softmax'))

    model.summary()

    return model


# Config 
EPOCHS             = 10
IMG_ROWS, IMG_COLS = 128, 128
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

print(x_train.shape)
model = build_model()

model.compile(loss='mean_squared_error', optimizer=Adam(lr=1.0e-4))

model.fit(x_train, y_train, epochs=EPOCHS)

# Evaluate model
# loss, acc = model.evaluate(x_test, y_test, verbose=1)
# print('Test loss:', loss)
# print('Test accuracy:', acc)

# Predict

img = x_test[2]
img = img.reshape((1, 128, 128, 1))
result = model.predict_classes(img)
print(result)






# def read_image(path):
#     """Read image and reverse channels"""
#     img = cv2.imread(path, cv2.IMREAD_COLOR)
#     return img[:,:,::-1]

# #### Use to load ALL data into memory (See next section for python generator) 
# X_all = np.ndarray((n_samples, ROWS, COLS, CHANNELS), dtype=np.uint8)

# for i, path in enumerate(image_paths):
#     DIR+path
#     img = read_image(DIR+path)
#     X_all[i] = img

### Create steering angle labels

# data = pd.read_csv('data/driving_log.csv', header=None, 
#                    names=['center', 'left', 'right', 'angle', 'throttle', 'break', 'speed'])

# y_all = data.angle.values

### Creating Validation Data
# X_train, X_test, y_train, y_test = train_test_split(
#     X_all, y_all, test_size=0.20, random_state=23)

# Callbacks
# early_stopping = EarlyStopping(monitor='val_loss', patience=8, verbose=1, mode='auto')   
# save_weights = ModelCheckpoint('model.h5', monitor='val_loss', save_best_only=True)

# model.fit_generator(fit_gen(data, batch_size),
#         samples_per_epoch=data.shape[0], nb_epoch=EPOCHS, 
#         validation_data=(x_test, y_test), callbacks=[save_weights, early_stopping])
    

# model.fit_generator(fit_gen(data, batch_size),
#         steps_per_epoch=None, epochs=EPOCHS, 
#         validation_data=(x_test, y_test), callbacks=[save_weights, early_stopping])
    

# preds = model.predict(X_test, verbose=1)

# print( "Test MSE: {}".format(mean_squared_error(y_test, preds)))
# print( "Test RMSE: {}".format(np.sqrt(mean_squared_error(y_test, preds))))


# Evaluate model
# loss, acc = model.evaluate(x_test, y_test, verbose=1)
# print('Test loss:', loss)
# print('Test accuracy:', acc)

#Save model
# model.save('my_model.h5')

# Load model
# new_model = tf.keras.models.load_model('my_model.h5') 
# new_model.summary()
# loss, acc = new_model.evaluate(x_test, y_test)
# print("Restored model, accuracy: {:5.2f}%".format(100*acc))

# Predict 
# result = new_model.predict(x_test[0], verbose=1)
# print(result)



# Architecture 1
# model = Sequential()
# model.add(Conv2D(32, (3, 3), padding='same', input_shape=(128, 128, 1)))
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
# model.add(Lambda(lambda x: x/127.5 - 1.0,input_shape=(img_rows, img_cols, 1)))
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
# adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
# model.compile(optimizer=adam, loss='mse', metrics=['accuracy'])

