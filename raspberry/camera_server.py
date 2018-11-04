import socket
import threading
import io
import struct
import time
import picamera

class CameraServer(object):
    def __init__(self):
      try:
        self.initSocketServer()
      except:
        self.serverSocket.close()

    
    def initSocketServer(self):
        port = 2222
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
        connection = c.makefile('wb')
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (128, 128)
                camera.framerate = 10
                time.sleep(2)

                # Note the start time and construct a stream to hold image data
                # temporarily (we could write it directly to connection but in this
                # case we want to find out the size of each capture first to keep
                # our protocol simple)
                stream = io.BytesIO()
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                    # Write the length of the capture to the stream and flush to
                    # ensure it actually gets sent
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()           
                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    connection.write(stream.read())
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
        finally:
            connection.close()
            c.close()
            self.serverSocket.close()


#Main Function
if __name__ == '__main__':
    CameraServer()
