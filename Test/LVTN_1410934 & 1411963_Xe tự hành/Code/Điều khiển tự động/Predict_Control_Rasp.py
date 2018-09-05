import pandas as pd
import cv2
import numpy as np
import time
from sklearn.model_selection import train_test_split
TEST_SIZE = 20
IMG_SIZE = 50
LR = 1e-3
threshold = 120
high_threshold = 190
MODEL_NAME = 'steering-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected, flatten
from tflearn.layers.estimator import regression
from picamera.array import PiRGBArray
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (320, 160)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(320, 160))
camera.awb_mode = 'off'
camera.awb_gains = (1.8,1.5)
time.sleep(0.1)
import serial
import struct
ser = serial.Serial()
ser.baudrate = 9600
try:
    ser.port = '/dev/ttyUSB1'
    ser.open()
except serial.serialutil.SerialException :
    try:
        ser.port = '/dev/ttyUSB0'
        ser.open()
    except serial.serialutil.SerialException :
        ser.port = '/dev/ttyUSB2'
        ser.open() 
ser.flushInput()
ser.flushOutput()
time.sleep(2)
##camera.shutter_speed = 30000
##camera.still_stats
##camera.exposure_mode = 'off'
##camera.still_stats = 'true'
##camera.capture(stream,format='jpeg')
##allow the camera to warmup

#firstcascade = cv2.CascadeClassifier('/home/pi/Desktop/Traffic_Sign/Cascade_Classifier/stopsign_classifier.xml')
P_cascade = cv2.CascadeClassifier('./Cascade_Classifier/Psign2.xml')
Stop_cascade = cv2.CascadeClassifier('./Cascade_Classifier/stopsign_classifier.xml')
Danger_cascade = cv2.CascadeClassifier('./Cascade_Classifier/danger_class.xml')
Limit_cascade = cv2.CascadeClassifier('./Cascade_Classifier/Limit.xml')

import tensorflow as tf
#tf.reset_default_graph()
import tensorflow as tf
#from utils import INPUT_SHAPE, batch_generator
import argparse
import os
import cv2
import string
#PATH = 'C:/Users/Admin/Desktop/car-behavioral-cloning-master/data/driving_log1.csv'

def nothing(x):
    pass
def control(model_out):
    if(np.argmax(model_out) == 0):
        print('goc queo = 150 ','acc = ',model_out[0][0])
        ser.write(struct.pack('>B', 120))
        if (ser.inWaiting() > 0 ):
            reachedPos = str(ser.readline())            
            print(reachedPos)
            ser.flushOutput()
    elif (np.argmax(model_out) == 1):
        print('goc queo = 120 ','acc = ',model_out[0][1])
        ser.write(struct.pack('>B', 120))
        if (ser.inWaiting() > 0 ):
            reachedPos = str(ser.readline())            
            print(reachedPos)
            ser.flushOutput()
    elif (np.argmax(model_out) == 2):
        print('goc queo = 90 ','acc = ',model_out[0][2])
        ser.write(struct.pack('>B', 97))
        if (ser.inWaiting() > 0 ):
            reachedPos = str(ser.readline())            
            print(reachedPos)
            ser.flushOutput()
    elif (np.argmax(model_out) == 3):
        print('goc queo = 60 ','acc = ',model_out[0][3])
        ser.write(struct.pack('>B', 60))
        if (ser.inWaiting() > 0 ):
            reachedPos = str(ser.readline())            
            print(reachedPos)
            ser.flushOutput()
    elif (np.argmax(model_out) == 4):
        print('goc queo = 30 ' ,'acc = ',model_out[0][4])
        ser.write(struct.pack('>B', 35))
        if (ser.inWaiting() > 0 ):
            reachedPos = str(ser.readline())            
            print(reachedPos)
            ser.flushOutput()

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

cv2.namedWindow('abc')
cv2.createTrackbar('Threshold','abc',160,255,nothing)
cv2.createTrackbar('high_Threshold','abc',170,255,nothing)

font = cv2.FONT_HERSHEY_SIMPLEX

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    frame1 = image.astype(np.uint8)
    img_flip = cv2.flip( frame1, -1 )
    gray = cv2.cvtColor(img_flip, cv2.COLOR_BGR2GRAY)
    stop_flag=0

    

    stop = Stop_cascade.detectMultiScale(gray, 1.3, 5)


    for (x,y,w,h) in stop:
        cv2.rectangle(img_flip,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(img_flip,'STOP',(x,y-5), font, 0.5,(255,255,0),1,cv2.LINE_AA)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img_flip[y:y+h, x:x+w]
        stop_flag = 1
        
    threshold = cv2.getTrackbarPos('Threshold','abc')
    high_threshold = cv2.getTrackbarPos('high_Threshold','abc')
    gray[gray < threshold ]  = 0
    #img[img > high_threshold ] = 0
    gray[gray >= threshold ] = 255
    img1 = cv2.resize(gray, (128,64))
    #img1 = img
    #img1[:20,:] = 0
    cv2.imshow('org',img1)
    model_out = model.predict(img1.reshape(-1,128,64,1))
    #print(model_out)
    if(stop_flag == 0):
        control(model_out)
    else:
        ser.write(struct.pack('>B', 103))
        if (ser.inWaiting() > 0 ):
            reachedPos = str(ser.readline())            
            print(reachedPos)
            #print('STOP SIGN IN FRONT')
            ser.flushOutput()

    park = P_cascade.detectMultiScale(gray, 1.3, 5)
    danger = Danger_cascade.detectMultiScale(gray, 1.1, 3)
    Limit = Limit_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in park:
        cv2.rectangle(img_flip,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(img_flip,'PARK CAR',(x,y-5), font, 0.5,(0,255,0),1,cv2.LINE_AA)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img_flip[y:y+h, x:x+w]
        
    for (x,y,w,h) in danger:
        cv2.rectangle(img_flip,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(img_flip,'DANGER',(x,y-5), font, 0.5,(255,0,0),1,cv2.LINE_AA)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img_flip[y:y+h, x:x+w]
        #print('DANGER')
        
    for (x,y,w,h) in Limit:
        cv2.rectangle(img_flip,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.putText(img_flip,'SPEED LIMIT',(x,y-5), font, 0.5,(0,0,255),1,cv2.LINE_AA)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img_flip[y:y+h, x:x+w]
    #cv2.imshow('img_flip',img_flip)



    
    cv2.imshow('anh final',img_flip)
    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF
    if  key == ord("q"):
        break

cv2.destroyAllWindows()

