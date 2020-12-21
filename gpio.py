import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

pin_btn = 17
#gp.setup(18, gp.OUT)
gp.setup(pin_btn, gp.IN, pull_up_down = gp.PUD_UP)

def btn_callback(channel):
    print('Edge detected on channel %s'%channel)

gp.add_event_detect(pin_btn, gp.RISING, callback=btn_callback, bouncetime=200)
#gp.add_event_callback(channel, btn_callback, bouncetime=200)

try:
    while 1:
        print("test")
        time.sleep(5)
except KeyboardInterrupt:
    gp.cleanup()
