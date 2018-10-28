#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 使用红外传感器探测障碍
#
#

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
########红外传感器接口定义#################
GPIO_OUT = 16
led = 37 
#设置引脚为输入和输出
#设置16针脚为输入，接到红外避障传感器模块的out引脚
GPIO.setup(GPIO_OUT,GPIO.IN) 
GPIO.setup(led,GPIO.OUT)     
 
def warn():   
	GPIO.output(led,GPIO.HIGH) #亮灯来作为有障碍物时发出的警告
	time.sleep(0.5)
	GPIO.output(led,GPIO.LOW)
	time.sleep(0.5)
		
while True:
	if GPIO.input(GPIO_OUT)==0: #当有障碍物时，传感器输出低电平，所以检测低电平
		warn()

GPIO.cleanup()