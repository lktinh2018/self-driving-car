import socket
import threading
import serial
import threading
import BlynkLib
from time import sleep

class App():

    BLYNK_AUTH = '2cd11bf758264c46a57c09d9f9dc29f9'
    blynkObj = 0
    serverSocket = 0
    serial = 0
    xAxis = 0 
    yAxis = 0

    def __init__(self):
        self.initSerial()
        #self.initSocketServer()
        self.initBlynk()

    def initSerial(self):
        ser = serial.Serial('/dev/ttyACM0', 500000, timeout=1)
        App.serial = ser
        print("Set up serial communication successful.")

    def initSocketServer(self):
        port = 1111
        serverSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        serverSocket.bind(('', port))
        serverSocket.listen(0)
        App.serverSocket = serverSocket
        
        serverThread = threading.Thread(target = self.serverHandler, args=())
        serverThread.start()
        print("Set up rc keyboard server successful.")
        
    def serverHandler(self):
        serverSocket = App.serverSocket
        while True:
            c, (a, p) = serverSocket.accept()
            t = threading.Thread(target = self.handleClient, args=(c, a, p))
            t.start()
        
    def handleClient(self, c, a, p):
        print("Connection from :", a, ":", str(p))
        while True:
            data = c.recv(2).decode()
            print(data)
            data += "\r\n"
            data = data.encode()
            self.serial.write(data)
            
            if data == "EXIT":
                print("Close socket client")
                break
        c.close()
        return

    def initBlynk(self):
        App.blynkObj = BlynkLib.Blynk(App.BLYNK_AUTH)

        @App.blynkObj.VIRTUAL_WRITE(0)
        def autoModeHandler(value):
            print('Current V0 value: {}'.format(value))

        @App.blynkObj.VIRTUAL_WRITE(1)
        def buzzerHandler(value):
            print("Buzz !!!")
            if value=="1":
                signal = "7"
            signal += "\r\n"
            signal = signal.encode()
            self.serial.write(signal)

        @App.blynkObj.VIRTUAL_WRITE(2)
        def speedHandler(value):
            print('Current V2 value: {}'.format(value))

        @App.blynkObj.VIRTUAL_WRITE(3)
        def xAxisHandler(value):
            App.xAxis = value

        @App.blynkObj.VIRTUAL_WRITE(4)
        def yAxisHandler(value):
            App.yAxis = value

        t = threading.Thread(target = self.blynkHandler, args=())
        t.start()

        t2 = threading.Thread(target = self.sendSignalHandler, args=())
        t2.start()
        
    def blynkHandler(self):
        App.blynkObj.run()

    def sendSignalHandler(self):
        while True:
            x = int(App.xAxis)
            y = int(App.yAxis)
            signal = 0
            print("X= {}  Y= {}".format(x, y))
            if x==100 and y==100:
                print("STOP")
                signal = 0
            
            if y > 100:
                if 50<=x and x<=150:
                    print("Forward")
                    signal = 1
                elif 0<=x and x<50:
                    print("Forward Left")
                    signal = 3
                elif 150<x and x<=200:
                    print("Forward Right")
                    signal = 4
            elif y < 100:
                if 50<=x and x<=150:
                    print("Reverse")
                    signal = 2
                elif 0<=x and x<50:
                    print("Reverse Left")
                    signal = 5
                elif 150 < x and x<=200:
                    print("Reverse Right")
                    signal =6

            signal += "\r\n"
            signal = signal.encode()
            self.serial.write(signal)
            sleep(0.01)




#Main Function
if __name__ == '__main__':
    App()




