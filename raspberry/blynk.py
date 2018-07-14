import BlynkLib

class Blynk(object):
    BLYNK_AUTH = '2cd11bf758264c46a57c09d9f9dc29f9'
    blynkObj = 0

    def __init__(self):
        self.initBlynk()

    def initBlynk(self):
        Blynk.blynkObj = BlynkLib.Blynk(Blynk.BLYNK_AUTH)
        print("Set up Bylnk successful.")

        @Blynk.blynkObj.VIRTUAL_WRITE(0)
        def autoModeHandler(value):
            print('Current V0 value: {}'.format(value))

        @Blynk.blynkObj.VIRTUAL_WRITE(1)
        def buzzerHandler(value):
            print('Current V1 value: {}'.format(value))

        @Blynk.blynkObj.VIRTUAL_WRITE(2)
        def speedHandler(value):
            print('Current V2 value: {}'.format(value))

        @Blynk.blynkObj.VIRTUAL_WRITE(3)
        def xAxisHandler(value):
            print('Current V3 value: {}'.format(value))

        @Blynk.blynkObj.VIRTUAL_WRITE(4)
        def yAxisHandler(value):
            print('Current V4 value: {}'.format(value))

        Blynk.blynkObj.run()

#Main Function
if __name__ == '__main__':
    Blynk()
    print("Hello")
    sleep(3)
