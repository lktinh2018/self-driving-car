import os, cv2, glob, keras
from keras.models import load_model
import numpy as np 

def get_image(path):
    #img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img_resized = cv2.resize(img, (IMG_ROWS, IMG_COLS))
    return img_resized

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


# Config
EPOCHS             = 10
IMG_ROWS, IMG_COLS = 256, 144
NUM_CLASSESS       = 3
CHANNELS           = 1
BATCH_SIZE         = 64


(x_test, y_test) = load_test()
x_test  = np.expand_dims(x_test, -1)
x_test = np.array(x_test, dtype=np.float32)
x_test  = x_test  / 255.0
y_test = keras.utils.to_categorical(y_test, NUM_CLASSESS)

# Main 
new_model = load_model('test_model.h5')


for i in range(0, 10):
    test_img = x_test[i].reshape((1, 144, 256, 1))

    #result = new_model.predict_classes(test_img)
    result = new_model.predict(test_img)
    print("Predict value: ", result)