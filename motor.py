import RPi.GPIO as GPIO
import time

pin = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 300)
p.start(0)

try:
    while True:
        p.ChangeDutyCycle(2.5)

except KeyboardInterrupt:
    p.stop()

GPIO.cleanup()
