from pynput import keyboard
import socket

def on_press(key):
        print("\n")
        #Send control signal to car
        signal = ""
        global forward
        global reverse
        if key == keyboard.Key.left and forward == True:
            print("Forward Left")
            signal = "3"
        elif key == keyboard.Key.right and forward:
            print("Forward Right")
            signal = "4"
        elif key == keyboard.Key.left and reverse:
            print("Reverse Left")
            signal = "5"
        elif key == keyboard.Key.right and reverse:
            print("Reverse Right")
            signal = "6"
        elif key == keyboard.Key.up:
            print("Forward")
            signal = "1"
            forward = True
        elif key == keyboard.Key.down:
            print("Reverse")
            signal = "2"
            reverse = True

        signal = signal.encode()
        connection.send(signal)



def on_release(key):
    #Send stop signal when release key
    signal = "0"
    signal = signal.encode()
    connection.send(signal)
    
    global forward
    global reverse
    if key == keyboard.Key.up:
        print("\nRelease Key Up")
        forward = False
    elif key == keyboard.Key.down:
        print("\nRelease Key Down")
        reverse = False

    if key == keyboard.Key.esc:
        print("\nExit program. Goodbye !!!")
        connection.send("EXIT".encode())
        connection.close()
        return False

#Main
# host = socket.gethostname()
host = "192.168.1.14"
port = 1111
connection = socket.socket()
connection.connect((host, port))

#Temp var
forward = False
reverse = False

print("Welcome To RC Keyboard Program !")
print("Press ESC To Quit Program...")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

