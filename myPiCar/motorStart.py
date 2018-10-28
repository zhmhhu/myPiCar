#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 电机转动
#
#

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def go():
    GPIO.setup(33,GPIO.OUT)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(12,GPIO.OUT)
    GPIO.output(33,True)
    GPIO.output(11,True)
    GPIO.output(12,False)

def changeSpeed():
    ENA = 33
	leftpwm = GPIO.PWM(ENA, 50)
	leftpwm.stop()
	leftpwm.start(100)
	leftpwm.ChangeDutyCycle(50)
	print('changeSpeed'+50)

go()
time.sleep(5)
changeSpeed()
#延时2秒之后执行cleanup释放GPIO接口
time.sleep(5)
GPIO.cleanup()