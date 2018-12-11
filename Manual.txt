Requirement
    + Python 3
    + pip3
    + pynput (lib)
    + serial

Port meaning:
    + RC Keyboard Server: 1111

Control signal:
    + Buzzer:           -1
    + Stop:             0
    + Forward:          1
    + Reverse:          2
    + Forward Left:     3
    + ForwardRight:     4
    + Reverse Left:     5
    + Reverse Right:    6


298 Shield Pinout:
	Function	Channel A Pin		Channel B Pin
	Direction		D12		        D13
	PWM				D10		        D11
	Buzzer			D4		        D4



- Step 1: 
	Run raspberry/app.py from raspberrypi.
- Step 2:
	Run computer/rc_keyboard_client.py from computer
- Step 3:
	Collect image by use Up, Down, Left, Right button from PC's keyboard.
- Step 4:
	Run computer/trainning.py to train model from image.
- Step 5: 
	Re-run step 1 and 2, press left-Shift from PC's keyboard to active self driving mode.