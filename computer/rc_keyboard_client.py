from pynput import keyboard
import socket
import time

class RCKeyboardClient(object):
    #Temp var
    forward = False
    reverse = False
    maxSpeed = False    
    def __init__(self):
        self.initClient()
        self.initKeyboardEvent()

    def initClient(self):          
        host = "192.168.1.101"
        port = 9999
        clientSocket = socket.socket()
        clientSocket.connect((host, port))
        self.clientSocket = clientSocket
        print("Connected to server.")
    
    def initKeyboardEvent(self):
        with keyboard.Listener(on_press = self.onPress, on_release = self.onRelease) as listener:
            listener.join()
        print("Init RC Keyboard Successful !")
        print("Press ESC To Quit Program...")   

    def onPress(self, key):
        print("\n")
        #Send control signal to car
        signal = "0"

        if key == keyboard.Key.left and RCKeyboardClient.forward:
            print("Forward Left")
            signal = "3"
        elif key == keyboard.Key.right and RCKeyboardClient.forward:
            print("Forward Right")
            signal = "4"
        elif key == keyboard.Key.left and RCKeyboardClient.reverse:
            print("Reverse Left")
            signal = "5"
        elif key == keyboard.Key.right and RCKeyboardClient.reverse:
            print("Reverse Right")
            signal = "6"
        elif key == keyboard.Key.ctrl_l:
            print("Honk")
            signal = "7"
        elif key == keyboard.Key.up:
            print("Forward")
            signal = "1"
            RCKeyboardClient.forward = True
        elif key == keyboard.Key.down:
            print("Reverse")
            signal = "2"
            RCKeyboardClient.reverse = True
        elif key == keyboard.Key.space:
            print("Active max speed")
            RCKeyboardClient.maxSpeed = True
            if  RCKeyboardClient.forward:
                self.clientSocket.sendall("10".encode())
            elif  RCKeyboardClient.reverse:
                self.clientSocket.sendall("20".encode())
            return

        if RCKeyboardClient.maxSpeed:
            signal = str(int(signal) * 10)

        print(signal)
        signal = signal.encode()
        self.clientSocket.sendall(signal)

    def onRelease(self, key):
        #Send stop signal when release key
        if key == keyboard.Key.up or  key == keyboard.Key.down:
            self.clientSocket.sendall("0".encode())

        if key == keyboard.Key.left or key == keyboard.Key.right:
            if RCKeyboardClient.forward:
                if RCKeyboardClient.maxSpeed:
                    self.clientSocket.sendall("10".encode())
                else:
                    self.clientSocket.sendall("1".encode())
            elif RCKeyboardClient.reverse:
                if RCKeyboardClient.maxSpeed:
                    self.clientSocket.sendall("20".encode())
                else:
                    self.clientSocket.sendall("2".encode())

        if key == keyboard.Key.space:
            RCKeyboardClient.maxSpeed = False

        if key == keyboard.Key.up:
            print("\nRelease Key Up")
            RCKeyboardClient.forward = False
        elif key == keyboard.Key.down:
            print("\nRelease Key Down")
            RCKeyboardClient.reverse = False

        if key == keyboard.Key.esc:
            print("\nExit program. Goodbye !!!")
            self.clientSocket.sendall("EXIT".encode())
            self.clientSocket.close()
            return False

if __name__ == '__main__':
    RCKeyboardClient()
