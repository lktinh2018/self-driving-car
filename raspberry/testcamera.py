from picamera import PiCamera
from time import sleep


camera = PiCamera()
camera.resolution = (128, 128)
camera.framerate = 10
camera.start_preview()
sleep(1)


save_folder = ""
for frame in camera.capture_continuous("../train_data/1/img{counter}.jpg"):
	sleep(0.1)

