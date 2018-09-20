import socket
import threading
import serial
from picamera import PiCamera
from time import sleep
import io 
import os

class App(object):

    # Train data path
    CLASS_0_PATH = "../train_data/0/"
    CLASS_1_PATH = "../train_data/1/"
    CLASS_2_PATH = "../train_data/2/"

    # Flag variables for capture images
    c0 = c1 = c2 = ""

    # Current control signal
    signal = ""

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
        print("Set up car handling Successful")
        while True:
            if self.autoMode:
                self.signal = "3"
                self.signal += "\r\n"
                self.signal = self.signal.encode()
                self.serial.write(self.signal)
                sleep(1)

    def getInfo(self):
      c0 = c1 = c2 = ""
      while True:
        print("Number images class 0 (forward):", len([f for f in os.listdir(self.CLASS_0_PATH) if f.endswith(".jpg")]) )
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
      sleep(1)
      print("Set up camera successful.")
      t = threading.Thread(target = self.handleCamera)
      t.start()

    def handleCamera(self):
        while True:
            if not self.autoMode:
                print("Hello Camera")
                stream = io.BytesIO()
                for count, foo in enumerate(self.camera.capture_continuous(stream, format="jpeg", bayer=True)):
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
                print("Deactive autonomous mode")
                self.autoMode = False
              else:
                print("Active autonomous mode")
                self.autoMode = True
            
            if not self.autoMode:
                self.signal += "\r\n"
                self.signal = self.signal.encode()
                self.serial.write(self.signal)
                self.done = False

        c.close()
        self.serverSocket.close()
        return

# Main Function
if __name__ == "__main__":
   App()
