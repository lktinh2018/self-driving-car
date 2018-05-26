import socket
import threading
import serial

class RCKeyboardServer(object):
    
    def __init__(self):
        self.initSerial()
        self.initSocketServer()
    
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

    def initSerial(self):
        ser = serial.Serial('/dev/ttyACM0', 500000, timeout=1)
        self.serial = ser

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