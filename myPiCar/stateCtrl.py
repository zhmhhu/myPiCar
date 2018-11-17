#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 电机控制
#
#

import RPi.GPIO as GPIO
import time


class stateCtrl(object):
	'''电机控制模块'''

	def __init__(self):

		########电机驱动接口定义#################
		self.ENA = 29  # //L298使能A
		self.ENB = 31  # //L298使能B
		self.IN1 = 7  # //电机接口1
		self.IN2 = 16  # //电机接口2
		self.IN3 = 13  # //电机接口3
		self.IN4 = 15  # //电机接口4

		########红外传感器接口定义#################
		self.IR_LF = 16  # 左上
		self.IR_LB = 18  # 左下
		self.IR_RF = 32  # 右上
		self.IR_RB = 22  # 右下

		########超声波传感器接口定义#################
		self.Trig = 33
		self.Echo = 32

		self.checkdiststate = False
		self.diststart = False

		#self.setup()

	def setup(self):
		'''引脚初始化'''
		#GPIO.setmode(GPIO.BOARD)
		#GPIO.setwarnings(False)

		GPIO.setup(self.IN1, GPIO.OUT)
		GPIO.setup(self.IN2, GPIO.OUT)
		GPIO.setup(self.IN3, GPIO.OUT)
		GPIO.setup(self.IN4, GPIO.OUT)

		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.LOW)
		print('car start')

		#GPIO.output(self.ENA, GPIO.HIGH)
		#GPIO.output(self.ENB, GPIO.HIGH)
		
	def t_up(self, secondvalue=0):
		self.setup()
		GPIO.output(self.IN1, True)
		GPIO.output(self.IN2, False)
		GPIO.output(self.IN3, True)
		GPIO.output(self.IN4, False)
		
	def t_down(self, secondvalue=0):
		self.setup()
		GPIO.output(self.IN1, False)
		GPIO.output(self.IN2, True)
		GPIO.output(self.IN3, False)
		GPIO.output(self.IN4, True)

	def t_left(self, secondvalue=0):
		self.setup()
		GPIO.output(self.IN1, True)
		GPIO.output(self.IN2, False)
		GPIO.output(self.IN3, False)
		GPIO.output(self.IN4, True)

	def t_right(self, secondvalue=0):
		self.setup()
		GPIO.output(self.IN1, False)
		GPIO.output(self.IN2, True)
		GPIO.output(self.IN3, True)
		GPIO.output(self.IN4, False)

	def t_stop(self):
		self.setup()
		GPIO.output(self.IN1, False)
		GPIO.output(self.IN2, False)
		GPIO.output(self.IN3, False)
		GPIO.output(self.IN4, False)

