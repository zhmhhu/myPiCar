#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  舵机测试模块
#
#
 
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
servo = 18
angle = 50
GPIO.setup(servo, GPIO.OUT)
pwm = GPIO.PWM(servo, 50)
pwm.start(8)
dutyCycle = angle / 18. + 3.
pwm.ChangeDutyCycle(dutyCycle)
sleep(0.3)
pwm.stop()
GPIO.cleanup()
print('cleanup!!')

