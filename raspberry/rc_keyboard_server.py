import socket
import threading
import serial

def handleClient(c, a, p):
    print("Connection from :", a, ":", str(p))
    while True:
        data = c.recv(1024).decode()
        ser.write(data)
        if data == "1":
            print("Forward")
        elif data == "2":
            print("Reverse")
        elif data == "3":
            print("Forward Left")
        elif data == "4":
            print("Forward Right")
        elif data == "5":
            print("Reverse Left")
        elif data == "6":
            print("Reverse Right")
        elif data == "0":
            print("Stop")
        
        if data == "EXIT":
            print("Close socket client")
            break
    c.close()
    return

#Set Up Serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

#Set Up Socket Server
port = 1111
connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
connection.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connection.bind(('', port))
connection.listen(0)
print("Set up rc keyboard server successful.")
while True:
    c, (a, p) = connection.accept()
    t = threading.Thread( target=handleClient, args=(c, a, p))
    t.start()
