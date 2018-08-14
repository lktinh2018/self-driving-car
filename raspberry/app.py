import socket
import threading
import serial


class App(object):

    def __init__(self):
        self.initSerial()
        self.initSocketServer()

    def initSerial(self):
        ser = serial.Serial('/dev/ttyACM0', 500000, timeout=1)
        self.serial = ser
        print("Set up serial communication successful.")

    def initSocketServer(self):
        port = 9999
        serverSocket = socket.socket()
        serverSocket.bind(('', port))
        serverSocket.listen(0)
        self.serverSocket = serverSocket
        print("Set up camera server successful.")
        
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

#Main Function
if __name__ == '__main__':
    App()