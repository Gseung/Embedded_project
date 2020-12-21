#-*- coding: utf-8-*-
import sys
import os
import time
import threading
import RPi.GPIO as gp
import numpy as np
import cv2
import Adafruit_DHT

# Sensor should be set to Adafruit_DHT.DHT11, Adafruit_DHT.DHT22 or Adafruit_DHT.AM2302
sensor = Adafruit_DHT.DHT11     # DHT11

# SERVO parameter
min_x = 100
max_x = 500
min_duty = 2
max_duty = 12.5
inclination = (max_duty-min_duty)/(max_x-min_x)

# GLOBAL variable
pin_buzz = 22
pin_sensor = 27
mode = 0
count = 0
check_human = 0

freq = [523, 587, 659, 698, 784, 880, 988, 1047]    # freq list (도, 레, 미, 파, 솔, 라, 시, 도)
list = [1, 3, 5, 1, 3, 5, 6, 6, 6, 5]               # sing

def btn_callback(channel):
    global mode
    print("fan mode : %d" %mode)
    gp.output(pin_buzz, gp.HIGH)
    time.sleep(0.05)
    gp.output(pin_buzz, gp.LOW)
    time.sleep(0.05)
    if(mode == 0):
        motor.ChangeDutyCycle(10)
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
        make_Tune(list)                 # 작은별 노래

    if(mode > 3):
        mode = 0


def sensor_thread():
    print("sensor thread")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_sensor)
    check_temperature = 0
    if humidity is not None and temperature is not None:
        print("temperature : {0:0.1f}*C%".format(temperature))
        if(temperature > 30):
            motor.ChangeDutyCycle(30)
            mode = 2
            check_temperature = 1
        elif(check_temperature == 1):
            motor.ChangeDutyCycle(0)
            mode = 3
            check = 0
    else:
        print('Failed to get reading. Try again!')

    timer1=threading.Timer(600,sensor_thread)            # check temperature per 10 minutes
    timer1.start()

def timer_count():
    global count
    print("timer cnt %d" %count)
    #print(count)
    if(check_human == 0):
        count+=1
    if(count > 30):
        motor.ChangeDutyCycle(0)
        mode = 3
        count = 0
    timer2=threading.Timer(1,timer_count)               # check human per 1 second
    timer2.start()


# Invert face location to servo duty
def location_equation(cur_x):
    duty = -inclination*cur_x+16
    if(duty < 4):
        duty = 4
    elif(duty >= 9.5):
        duty = 9.5
    return duty

# Sing of Twinkle Twinkle little Star
def make_Tune(list):
    p = gp.PWM(pin_buzz, 100)
    p.start(100)
    p.ChangeDutyCycle(10)
    for i in list:
        p.ChangeFrequency(freq[i])
        time.sleep(0.6)
    p.stop()


if __name__ == '__main__':

    # GPIO init
    pin_motor = 3
    pin_servo = 4
    pin_btn = 17
    gp.setmode(gp.BCM)
    gp.setup(pin_btn, gp.IN, pull_up_down = gp.PUD_UP)   # setup pull-up
    gp.setup(pin_motor, gp.OUT)
    gp.setup(pin_servo, gp.OUT)
    gp.setup(pin_buzz, gp.OUT)

    # add interrupt
    gp.add_event_detect(pin_btn, gp.RISING, callback=btn_callback, bouncetime=200)

    # PWM init
    motor = gp.PWM(pin_motor, 300)
    servo = gp.PWM(pin_servo, 50)
    motor.start(0)
    servo.start(0)

    # Face Detection
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    try:
        sensor_thread()
        timer_count()
        while True:
            check_human = 0
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20, 20)
            )
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+x,y+h),(255,0,0),2)       # boxing by OpenCV
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                mid = (x+(x+w))/2
                servo.ChangeDutyCycle(location_equation(mid))
                print(location_equation(mid))
                check_humman = 1                                     # Human Detect Flag
                count = 0
                time.sleep(0.01)

            cv2.imshow('video',img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

    except KeyboardInterrupt:
        gp.cleanup()
        cap.release()
        cv2.destroyAllWindows()


