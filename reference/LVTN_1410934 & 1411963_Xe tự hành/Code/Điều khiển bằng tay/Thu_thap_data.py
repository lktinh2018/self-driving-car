import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#import dlib
import serial
import pandas as pd
#Khai bao pandas
basename = "steering_%s.jpg"
label = []
steering_csv = []
t = 1       # dem so luong hinh anh
global steering     # gia tri goc quay
i = 1  # dem hinh csv
csv_path = "./driving_log.csv"

#Khai bao camera pi
camera = PiCamera()
camera.resolution = (50, 50)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(50, 50))
camera.awb_mode = 'off'
camera.awb_gains = (1.8,1.5)
time.sleep(0.1)

#Khai bao serial
ser = serial.Serial()
ser.baudrate = 115200
try:
    ser.port = '/dev/ttyUSB1'
    ser.open()
except serial.serialutil.SerialException :
    try:
        
        ser.port = '/dev/ttyUSB0'
        ser.open()
    except serial.serialutil.SerialException :
        ser.port = 'COM4'
        ser.open()
ser.flushInput()
# cot 1 la vi tri x, cot 2 la vi tri y
pts1 = np.float32([[116,13],[390,13],[0,157],[450,140]])
pts2 = np.float32([[0,0],[479,0],[10,367],[445,367]])
##pts1 = np.float32([[75,120],[420,120],[0,157],[455,160]])
##pts2 = np.float32([[0,0],[479,0],[10,367],[445,367]])

#Khai bao pandas


def insert_csv(basename,steering):
    global i,t
    global label, steering_csv
    
    text='C:/Users/Nguyen Duc/Desktop/car-behavioral-cloning-master/data/IMG/%s' %(basename %(t) )
    label.insert(i,text)
    steering_csv.insert(i,steering)
    i+=1
    t+=1
def flip_image(image,steering):
    flip_img=cv2.flip(image,1)
    if (steering != 100 ):
        steering = 180 - steering

    return flip_img, steering
def export_csv():
    global label, steering_csv
    d = {'center':label,'steering':steering_csv}
    df = pd.DataFrame.from_records(data=d)
    df.to_csv(csv_path, sep=',',index=False)
def nothing(x):
    pass

cv2.namedWindow('abc')
cv2.createTrackbar('Threshold','abc',160,255,nothing)
    
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #Doc camera
    img = frame.array
    image = img.astype(np.uint8)
    image = cv2.flip( image, -1 )
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imshape = image.shape
    cv2.imshow('image',image)
    threshold = cv2.getTrackbarPos('Threshold','abc')
    img[:10,:]=0
    img[img < threshold ]  = 0
    img[img >= threshold ] = 255
    cv2.imshow('anh',img)
    '''
        #Threholding
    high_threshold = np.array([255, 255, 255]) #Bright white
    #high_threshold = np.array([255, 255, 255]) #Bright white
    #low_threshold = np.array([100, 120, 130]) #Soft White
    low_threshold = np.array([90, 115, 130]) #Soft White
    #low_threshold = np.array([200, 190, 190])
    mask = cv2.inRange(image, low_threshold, high_threshold)   
    #cv2.imshow('white mask',mask)
    
        #Perspective Transform
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(mask,M,(480,368))
    dst[(dst > 0)] = 255
    #white_img = cv2.bitwise_and(image, image, mask=mask)

    #cv2.imshow('dst',dst)
    '''
    

        #Nhan serial
    try:
    #ser.flushinput()
        #if (ser.inWaiting() > 0 and ser.inWaiting() <10):
        
        if (ser.inWaiting() > 0 ):
        
            print('bye wait = ',ser.inWaiting())
            #mess=ser.readline(size = 10)
            
            mess=ser.readline()
            
            try:
                steering = int(mess)
                if ( steering == 97):
                    steering = 100
                print('steering angle = ',steering)
##                cv2.putText(image,"Steering angle = /n" + str(mess) , org=(50,150), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
##                fontScale=1, color=(255,255,255), lineType = cv2.LINE_AA, thickness=1)
                cv2.imwrite("./IMG/steering_%d.jpg" % (t), img)     # save frame as JPEG file
                cv2.imwrite("./IMG1/steering_%d.jpg" % (t), image)
                insert_csv(basename,steering)
                
                flip_img,flip_steering = flip_image(img,steering)
                flip_img1,_ = flip_image(image,steering)
                cv2.imwrite("./IMG/steering_%d.jpg" % (t), flip_img)
                cv2.imwrite("./IMG1/steering_%d.jpg" % (t), flip_img1)
                insert_csv(basename,flip_steering)
                
                print('anh thu i,t = ',i,' ',t)
                
            except ValueError :
                print('mess = ',mess)
            ser.flushInput()
        
    except OSError :
        print('rekt')
        print('port hien tai = ',ser.port)
        ser.close()
        time.sleep(3)
        ser.open()
        #ser.flushInput()
        print(' co port connect chua : ',ser.isOpen())
        print(' so byte dang doi : ',ser.inWaiting())
        if ( ser.inWaiting() > 20):
            mess1=ser.readline()
            print('mess1 = ',mess1)
            ser.flushInput()
            #print('vua xoa, so byte dang doi',ser.inWaiting())
        
        pass  

    rawCapture.truncate(0)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
export_csv()            
cv2.destroyAllWindows() 


