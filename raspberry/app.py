import socket
import threading
import serial
from picamera import PiCamera
from time import sleep
import io 

class App(object):

    signal = ""
    done = False
    autoMode = False
    
    def __init__(self):
        self.initSerial()
        self.initCamera()
        self.initSocketServer()

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
      stream = io.BytesIO()
      for count, foo in enumerate(self.camera.capture_continuous( stream, format='png', bayer=True)):
            # Get number of bytes in the stream
            num_of_bytes = stream.tell()
            # Rewind the stream to start
            stream.seek(0)
            # Save stream contents to file
            if self.signal == "1" or self.signal == "3" or self.signal == "4" and self.done == False:
              if self.signal == "1":
                save_path = "../train_data/0/img%d.png" % count
              elif self.signal == "3":
                save_path = "../train_data/1/img%d.png" % count
              elif self.signal == "4":
                save_path = "../train_data/2/img%d.png" % count
              with open(save_path, 'wb') as f:
                f.write(stream.read(num_of_bytes))
              self.done = True

            # Empty the stream
            stream.seek(0)
            stream.truncate()
            

    def initSerial(self):
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.serial = ser
        print("Set up serial communication successful.")


    def initSocketServer(self):
        port = 9999
        serverSocket = socket.socket()
        serverSocket.bind(('', port))
        serverSocket.listen(0)
        self.serverSocket = serverSocket
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
        print("\n Connection from :", a, ":", str(p))
        while True:
            data = c.recv(2).decode()
            self.signal = data[0]
            
            if self.signal == "8":
              if self.autoMode:
                print("Deactive autonomous mode")
                self.autoMode = False
              else:
                print("Active autonomous mode")
                self.autoMode = True
            #print(data)
            
            
            data += "\r\n"
            data = data.encode()
            self.serial.write(data)
            self.done = False
            if data == "EXIT":
                print("Close socket client")
                break
        c.close()
        return


#Main Function
if __name__ == '__main__':
   App()
