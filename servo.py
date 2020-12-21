import numpy as np
import RPi.GPIO as gp
import time

pin_servo = 4 
gp.setmode(gp.BCM)
gp.setup(pin_servo, gp.OUT)
p = gp.PWM(pin_servo, 50)
p.start(0)

duty = np.arange(2,13,0.5)

try:
    while True:
        p.ChangeDutyCycle(2)
        '''
        for dc in duty:
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.03)
        for dc in np.flip(duty):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.03)
            '''

except KeyboardInterrupt:
    gp.cleanup()

