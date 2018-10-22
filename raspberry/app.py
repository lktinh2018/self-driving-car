import io, time, os, serial, socket, threading, keras,cv2
from keras.models import load_model
from picamera import PiCamera
from time import sleep
import numpy as np 
from picamera.array import PiRGBArray

class App(object):
      
    #Coming image
    coming_img = ""
    
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
    
    
    # New Coming Image Flag
    new_img_flag = False
    
    
    def __init__(self):
        self.getInfo()
        self.initSerial()
        self.initCamera()
        self.initSocketServer()
        self.handleCar()

    def handleCar(self):
        print("Set up car handling successful")
        # Load model
        new_model = load_model('my_model.h5')
        print("Load model successful !!!")
        while True:
            if self.autoMode and self.new_img_flag :
            
                self.coming_img = np.expand_dims(self.coming_img, -1)
                
                self.coming_img = np.array(self.coming_img, dtype=np.float32)
                
                self.coming_img = self.coming_img / 255.0
                
                self.coming_img = self.coming_img.reshape((1, 128, 128, 1))
                
                cv2.imshow('Coming Image', self.coming_img)
                key = cv2.waitKey(1) & 0xFF
                if  key == ord("q"):
                   break
                
                print(self.coming_img.shape)
                
                result = new_model.predict_classes(self.coming_img)
                
                print("Predict value: ", result)
#                if result == 0:
#                  self.signal = "1"
#                elif result == 1:
#                  self.signal = "3"
                
#                self.signal = "3"
#                self.serial.write((self.signal + "\r\n").encode())
                self.new_img_flag = False
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
        rawCapture = PiRGBArray(self.camera, size=(128, 128))
        while True:
          if self.autoMode :
              for frame in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                  image = frame.array
                  image = image.astype(np.uint8)
                  gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                  self.coming_img = gray_img
                  rawCapture.truncate(0)
                  if not self.autoMode:
                      break
                  self.new_img_flag = True
          else:
              for count, foo in enumerate(self.camera.capture_continuous(stream, format="jpeg")):
                  # Save stream contents to file
                  if ((self.done == False) and ((self.signal == "1" and self.c0) or (self.signal == "3" and self.c1) or (self.signal == "4" and self.c2)) ) :
                      # Rewind the stream to start
                      stream.seek(0)
                      # Get number of bytes in the stream
                      num_of_bytes = stream.tell()
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
                  if self.autoMode:
                      break
            
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
