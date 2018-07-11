import socket
import threading
import serial
import BlynkLib

class RCKeyboardServer(object):
    BLYNK_AUTH = '2cd11bf758264c46a57c09d9f9dc29f9'
    
    def __init__(self):
        self.initSerial()
        self.initSocketServer()
        self.initBlynk()
    
    def initSerial(self):
        ser = serial.Serial('/dev/ttyACM0', 500000, timeout=1)
        self.serial = ser

    def initSocketServer(self):
        port = 1111
        serverSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        serverSocket.bind(('', port))
        serverSocket.listen(0)
        print("Set up rc keyboard server successful.")

        while True:
            c, (a, p) = serverSocket.accept()
            t = threading.Thread(target = self.handleClient, args=(c, a, p))
            t.start()

    def initBlynk(self):
        blynk = BlynkLib.Blynk(BLYNK_AUTH)
        self.initBlynkHandlers()

    #def initBlynkHandlers(self):
    @blynk.VIRTUAL_WRITE(0)
    def autoModeHandler(value):
        print('Current V0 value: {}'.format(value))

    @blynk.VIRTUAL_WRITE(1)
    def buzzerHandler(value):
        print('Current V1 value: {}'.format(value))

    @blynk.VIRTUAL_WRITE(2)
    def my_write_handler(value):
        print('Current V2 value: {}'.format(value))

    @blynk.VIRTUAL_WRITE(3)
    def my_write_handler(value):
        print('Current V3 value: {}'.format(value))

    @blynk.VIRTUAL_WRITE(4)
    def my_write_handler(value):
        print('Current V4 value: {}'.format(value))

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

#Main Function
if __name__ == '__main__':
    RCKeyboardServer()
    blynk.run()
