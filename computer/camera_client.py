import socket
import time
import numpy as np
import cv2

class CameraClient(object):

    streamSocket = ""

    def __init__(self):
        self.initSocketClient()

    def initSocketClient(self):
        host = "raspberrypi"
        port = 2222
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        streamSocket = clientSocket.makefile('rb')
        print("Connected to camera server")
        try:
            print("Streaming...")
            stream_bytes = " "
            
            while True:
                stream_bytes += self.streamSocket.recv(1024).decode('utf-8')
                first = stream_bytes.find('\xff\xd8')
                last  = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)


                    #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
                    #cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                    cv2.imshow('Camera', image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        finally:
            clientSocket.close()
            streamSocket.close()

#Main Function
if __name__ == '__main__':
    CameraClient()