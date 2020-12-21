import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)
pin_buzzer = 22

scale = [261, 294, 329, 349, 392, 440, 493, 523]

gp.setup(pin_buzzer, gp.OUT)

try:
    p = gp.PWM(pin_buzzer, 100)
    p.start(100)
    p.ChangeDutyCycle(90)

    for i in range(8):
        print(i+1)
        p.ChangeFrequency(scale[i])
        time.sleep(1)

    p.stop()

finally:
    gp.cleanup()


