import socket
import threading
import serial
from picamera import PiCamera
from time import sleep
import io 
import os

# Libs for CNN
import keras
from keras.datasets import mnist
from keras import backend as K
from keras.models import load_model
import time

# Var for CNN
batch_size = 128
num_classes = 10
epochs = 12

# Input image dimensions
img_rows, img_cols = 28, 28
IMG_ROWS, IMG_COLS = 28, 28

class App(object):

    # Train data path
    CLASS_0_PATH = "../train_data/0/"
    CLASS_1_PATH = "../train_data/1/"
    CLASS_2_PATH = "../train_data/2/"

    # Flag variables for capture images
    c0 = c1 = c2 = ""

    # Current control signal
    signal = ""

    # Camera object
    camera = ""

    # Capture flag
    done = False

    # Auto mode flag
    autoMode = False

    # Server socket var
    serverSocket = ""

    def __init__(self):
        self.getInfo()
        self.initSerial()
        self.initCamera()
        self.initSocketServer()
        self.handleCar()

    def handleCar(self):
        print("Set up car handling successful")
        # Load train and test sets
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
        print('x_train shape:', x_train.shape)
        # Convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)
        # Load model
        new_model = load_model('MNIST.h5')
        print("Load model successful !!!")
        while True:
            if self.autoMode:
                start = time.time()
                new_img = x_test[0]
                new_img = new_img.reshape((1, 28, 28, 1))
                result = new_model.predict_classes(new_img)
                end = time.time()
                print("Time elapse: ", end - start)
                print("Predict value: ", result)
                self.signal = "3"
                self.serial.write((self.signal + "\r\n").encode())
                sleep(1)

    def getInfo(self):
        c0 = c1 = c2 = ""
        while True:
            print("\nNumber images class 0 (forward):", len([f for f in os.listdir(self.CLASS_0_PATH) if f.endswith(".jpg")]) )
            print("Do you want to continue capture image class 0 (y/n) ?")
            c0 = input()
            if c0 == "y" or c0 == "Y":
                print("You select continue capture class 0.\n\n")
                self.c0 = True
                break;
            elif c0 == "n" or c0 == "N": 
                print("You select NOT continue capture class 0.\n\n")
                self.c0 = False
                break;
            else:
                print("Wrong input, Plese enter 'y' or 'n' character.\n\n")

        while True:    
            print("Number images class 1 (turn left):", len([f for f in os.listdir(self.CLASS_1_PATH) if f.endswith("jpg")]) )
            print("Do you want to continue capture image class 1 (y/n) ?")
            c1 = input()
            if c1 == "y" or c1 == "Y":
                print("You select continue capture class 1.\n\n")
                self.c1 = True
                break;
            elif c1 == "n" or c1 == "N": 
                print("You select NOT continue capture class 1.\n\n")
                self.c1 = False
                break;
            else:
                print("Wrong input, Plese enter 'y' or 'n' character.\n\n")

        while True:    
            print("Number images class 2 (turn right):", len([f for f in os.listdir(self.CLASS_2_PATH) if f.endswith("jpg")]) )
            print("Do you want to continue capture image class 2 (y/n) ?")
            c2 = input()
            if c2 == "y" or c2 == "Y":
                print("You select continue capture class 2.\n\n")
                self.c2 = True
                break;
            elif c2 == "n" or c2 == "N": 
                print("You select NOT continue capture class 2.\n\n")
                self.c2 = False
                break;
            else:
                print("Wrong input, Plese enter 'y' or 'n' character.\n\n")

    def initCamera(self):
        camera = PiCamera()
        camera.resolution = (128, 128)
        camera.framerate = 10
        camera.start_preview()
        self.camera = camera
        sleep(2)
        print("Set up camera successful.")
        t = threading.Thread(target = self.handleCamera)
        t.start()

    def handleCamera(self):
        stream = io.BytesIO()
        for count, foo in enumerate(self.camera.capture_continuous(stream, format="jpeg")):
            if not self.autoMode :
                # Save stream contents to file
                if ( (self.done == False) and ((self.signal == "1" and self.c0) or (self.signal == "3" and self.c1) or (self.signal == "4" and self.c2)) ) :
                    # Get number of bytes in the stream
                    num_of_bytes = stream.tell()
                    # Rewind the stream to start
                    stream.seek(0)
                    if self.signal == "1":
                        save_path = "../train_data/0/img%d.jpg" % count
                    elif self.signal == "3":
                        save_path = "../train_data/1/img%d.jpg" % count
                    elif self.signal == "4":
                        save_path = "../train_data/2/img%d.jpg" % count
                    with open(save_path, "wb") as f:
                        f.write(stream.read(num_of_bytes))
                    self.done = True
                    # Empty the stream
                    stream.seek(0)
                    stream.truncate()

            
    def initSerial(self):
        ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
        self.serial = ser
        print("Set up serial communication successful.")

    def initSocketServer(self):
        port = 9999
        serverSocket = socket.socket()
        serverSocket.bind(("", port))
        serverSocket.listen(0)
        self.serverSocket = serverSocket
        print("Set up socket server successful.")
        serverThread = threading.Thread(target = self.handleSocketServer)
        serverThread.start()
        
    def handleSocketServer(self):
      while True:
        c, (a, p) = self.serverSocket.accept()
        handleClientThread = threading.Thread(target = self.handleClient, args=(c, a, p))
        handleClientThread.start()
    
    def handleClient(self, c, a, p):
        print("\nConnection from :", a, ":", str(p))
        while True:
            data = c.recv(2).decode()
            if data == "EX":
                print("Close socket server")
                break

            self.signal = data[0]
            if self.signal == "8":
              if self.autoMode:
                self.serial.write(("0\r\n").encode())
                print("Deactive autonomous mode")
                self.autoMode = False
              else:
                print("Active autonomous mode")
                self.autoMode = True
            
            if not self.autoMode:
                self.serial.write( (self.signal + "\r\n").encode())
                self.done = False

        c.close()
        self.serverSocket.close()
        return

# Main Function
if __name__ == "__main__":
   App()
