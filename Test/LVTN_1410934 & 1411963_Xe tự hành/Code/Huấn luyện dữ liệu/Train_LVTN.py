import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import argparse
import os
import cv2
import string
PATH = 'C:/Users/Nguyen Duc/Desktop/car-behavioral-cloning-master/data/driving_log.csv'
TEST_SIZE = 100
IMG_SIZE = 50
LR = 1e-3
threshold = 170

MODEL_NAME = 'steering-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match
def load_csv_data():
    data_df = pd.read_csv(os.path.join(PATH))

    x = data_df['center'].values
    y = data_df['steering'].values

    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size = TEST_SIZE, random_state=0)

    return train_x, test_x, train_y, test_y

def label_img(y): #180-150-120-100-60-30-0
    if str(y) == '180': return [1,0,0,0,0]
    elif str(y) == '150': return [1,0,0,0,0]
    elif str(y) == '120': return [0,1,0,0,0]
    elif str(y) == '100': return [0,0,1,0,0]# So on
    elif str(y) == '60': return [0,0,0,1,0]
    elif str(y) == '30': return [0,0,0,0,1]
    elif str(y) == '0': return [0,0,0,0,1]
    
def create_train_and_test_data():
    test_data = []
    train_data = []
    train_x, test_x, train_y, test_y = load_csv_data()
    for i in range(len(train_x)):
        path_img = (train_x[i].replace('\\','/'))
        #img = cv2.imread(path_img.replace('Nguyen Duc','Admin'),cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(path_img,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img,(128,64))
        img[img>= threshold] = 255
        img[ img < threshold] = 0
        #img[:20,:] = 0
        #img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        train_data.append([np.array(img),np.array(label_img(train_y[i]))])
    np.save('train_data.npy', train_data)
    for i in range(len(test_x)):
        path_img = (test_x[i].replace('\\','/'))
        #img = cv2.imread(path_img.replace('Nguyen Duc','Admin'),cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(path_img,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img,(128,64))
        img[img>= threshold] = 255
        img[ img < threshold] = 0
        #img[:20,:] = 0
        #img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        test_data.append([np.array(img),np.array(label_img(test_y[i]))])
    np.save('test_data.npy', test_data)
    return train_data, test_data

train_data,test_data = create_train_and_test_data()
# If you have already created the dataset:
#train_data = np.load('train_data.npy')

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected,flatten
from tflearn.layers.estimator import regression

import tensorflow as tf
tf.reset_default_graph()

convnet = input_data(shape=[None, 128, 64, 1], name='input')

convnet = conv_2d(convnet, 24, 5, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 36, 5, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 48, 5, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 3, activation='relu')
#convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 3, activation='relu')
#convnet = max_pool_2d(convnet, 5)

convnet = dropout(convnet, 0.8)
convnet = flatten(convnet, name='Flatten')

convnet = fully_connected(convnet, 100, activation='relu')


convnet = fully_connected(convnet, 50, activation='relu')


convnet = fully_connected(convnet, 5, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')



if os.path.exists('{}.meta'.format(MODEL_NAME)):
    model.load(MODEL_NAME)
    print('model loaded!')

train = train_data[:-500]
test = train_data[-500:]

X = np.array([i[0] for i in train]).reshape(-1,128,64,1)
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1,128,64,1)
test_y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=5, validation_set=({'input': test_x}, {'targets': test_y}), snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

model.save(MODEL_NAME)

