#-*- coding: utf-8-*-
import sys
import os
import time
import RPi.GPIO as gp
import numpy as np
import cv2

# SERVO parameter
min_x = 100
max_x = 500
min_duty = 2
max_duty = 12.5
inclination = (max_duty-min_duty)/(max_x-min_x)

pin_buzz = 22
mode = 0

# GPIO init
pin_motor = 3
pin_servo = 4
pin_btn = 17
gp.setmode(gp.BCM)
gp.setup(pin_btn, gp.IN, pull_up_down = gp.PUD_UP)   # setup pull-up
gp.setup(pin_motor, gp.OUT)
gp.setup(pin_servo, gp.OUT)
gp.setup(pin_buzz, gp.OUT)

freq = [523, 587, 659, 698, 784, 880, 988, 1047]    # freq list (도, 레, 미, 파, 솔, 라, 시, 도)
list = [1, 3, 5, 1, 3, 5, 6, 6, 6, 5]               # sing

def btn_callback(channel):
    global mode
    print("test")
    gp.output(pin_buzz, gp.HIGH)
    time.sleep(0.05)
    gp.output(pin_buzz, gp.LOW)
    time.sleep(0.05)
    print(mode)
    if(mode == 0):
        motor.ChangeDutyCycle(30)
        mode+=1
    elif(mode == 1):
        motor.ChangeDutyCycle(20)
        mode+=1
    elif(mode == 2):
        motor.ChangeDutyCycle(5)
        mode+=1
    elif(mode == 3):
        motor.ChangeDutyCycle(0)
        mode+=1
        print(len(list))
        make_Tune(list)                 # 작은별 노래

    if(mode > 3):
        mode = 0


def location_equation(cur_x):
    duty = -inclination*cur_x+16
    if(duty < 4):
        duty = 4
    elif(duty >= 9.5):
        duty = 9.5
    return duty

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
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20, 20)
            )
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+x,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                mid = (x+(x+w))/2
                servo.ChangeDutyCycle(location_equation(mid))
                print(location_equation(mid))
                time.sleep(0.01)

            cv2.imshow('video',img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

    except KeyboardInterrupt:
        gp.cleanup()
        cap.release()
        cv2.destroyAllWindows()


