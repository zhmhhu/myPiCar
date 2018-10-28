#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# LED 灯亮度及频率控制
#
#

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

p1 = GPIO.PWM(23, 50)
p2 = GPIO.PWM(24, 38)

p1.start(0)
p2.start(0)

try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            p11.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            p11.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass

p1.stop()
p2.stop()
GPIO.cleanup()