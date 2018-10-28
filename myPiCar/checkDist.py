#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 使用超声波传感器探测目标距离
#
#

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

########超声波传感器接口定义#################
Trig = 38
Echo = 40


# 超声波距离探测
def checkdist():
	GPIO.setup(Trig, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(Echo, GPIO.IN)
	GPIO.output(Trig, GPIO.HIGH)
	time.sleep(0.00015)
	GPIO.output(Trig, GPIO.LOW)
	while not GPIO.input(Echo):
		pass
	t1 = time.time()
	while GPIO.input(Echo):
		pass
	t2 = time.time()
	return (t2-t1)*340*100/2

def distStart():
	try:
    while True:
        print '目标距离:%0.2f cm' % checkdist()
        time.sleep(0.5)
	except KeyboardInterrupt:
    	GPIO.cleanup()

distStart()
