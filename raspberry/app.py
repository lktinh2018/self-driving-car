import socket
import threading
import serial
import threading
import BlynkLib

class App():

    BLYNK_AUTH = '2cd11bf758264c46a57c09d9f9dc29f9'
    blynkObj = 0
    serverSocket = 0
    
    def __init__(self):
        self.initSerial()
        self.initSocketServer()
    
    def initSerial(self):
        ser = serial.Serial('/dev/ttyACM0', 500000, timeout=1)
        self.serial = ser
        print("Set up serial communication successful.")

    def initSocketServer(self):
        port = 1111
        serverSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        serverSocket.bind(('', port))
        serverSocket.listen(5)
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
            print('Current V1 value: {}'.format(value))

        @App.blynkObj.VIRTUAL_WRITE(2)
        def speedHandler(value):
            print('Current V2 value: {}'.format(value))

        @App.blynkObj.VIRTUAL_WRITE(3)
        def xAxisHandler(value):
            print('Current V3 value: {}'.format(value))

        @App.blynkObj.VIRTUAL_WRITE(4)
        def yAxisHandler(value):
            print('Current V4 value: {}'.format(value))

        t = threading.Thread(target = self.blynkHandler, args=())
        t.start()
        
    
    def blynkHandler(self):
        App.blynkObj.run()




#Main Function
if __name__ == '__main__':
    App()



