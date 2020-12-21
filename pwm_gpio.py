import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

pin_btn = 17
pin_motor = 3
#gp.setup(18, gp.OUT)
gp.setup(pin_btn, gp.IN, pull_up_down = gp.PUD_UP)
gp.setup(pin_motor, gp.OUT)

motor = gp.PWM(pin_motor, 300)
motor.start(0)

mode = 0

def btn_callback(channel):
    print('Edge detected on channel %s'%channel)
    global mode
    if(mode == 0):
        motor.ChangeDutyCycle(5)
        mode+=1
    elif(mode == 1):
        motor.ChangeDutyCycle(20)
        mode+=1
    elif(mode == 2):
        motor.ChangeDutyCycle(30)
        mode+=1
    elif(mode == 3):
        motor.ChangeDutyCycle(0)
        mode+=1
    if(mode > 3):
        mode = 0

gp.add_event_detect(pin_btn, gp.RISING, callback=btn_callback, bouncetime=200)
#gp.add_event_callback(channel, btn_callback, bouncetime=200)

try:
    while 1:
        print("test")
        time.sleep(5)
except KeyboardInterrupt:
    gp.cleanup()
