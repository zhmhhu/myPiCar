#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 电机控制
# 超声波测距
# 红外避障
#

import RPi.GPIO as GPIO
import time


class stateCtrl(object):
	'''电机控制模块'''

	def __init__(self):

		########电机驱动接口定义#################
		self.ENA = 33  # //L298使能A
		self.ENB = 35  # //L298使能B
		self.IN1 = 11  # //电机接口1
		self.IN2 = 12  # //电机接口2
		self.IN3 = 13  # //电机接口3
		self.IN4 = 15  # //电机接口4

		########红外传感器接口定义#################
		self.IR_LF = 16  # 左上
		self.IR_LB = 18  # 左下
		self.IR_RF = 32  # 右上
		self.IR_RB = 22  # 右下

		########超声波传感器接口定义#################
		self.Trig = 38
		self.Echo = 40

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
		GPIO.output(self.IN3, False)
		GPIO.output(self.IN4, True)
		self.checkdiststate = True
		if self.diststart == False:
			self.distStart()
		else:
			pass

		if secondvalue != 0:
		   time.sleep(secondvalue)
		   self.stop()


	def t_left(self, secondvalue=0):
		self.setup()
		GPIO.output(self.IN1, False)
		GPIO.output(self.IN2, True)
		GPIO.output(self.IN3, False)
		GPIO.output(self.IN4, True)
		self.checkdiststate = True
		if self.diststart == False:
			self.distStart()
		else:
			pass

		if secondvalue != 0:
		   time.sleep(secondvalue)
		   self.stop()

	def t_right(self, secondvalue=0):
		self.setup()
		GPIO.output(self.IN1, True)
		GPIO.output(self.IN2, False)
		GPIO.output(self.IN3, True)
		GPIO.output(self.IN4, False)
		self.checkdiststate = True
		if self.diststart == False:
			self.distStart()
		else:
			pass

		if secondvalue != 0:
		   time.sleep(secondvalue)
		   self.stop()

	def t_down(self, secondvalue=0):
		self.setup()
		GPIO.output(self.IN1, False)
		GPIO.output(self.IN2, True)
		GPIO.output(self.IN3, True)
		GPIO.output(self.IN4, False)
		self.checkdiststate = True
		if self.diststart == False:
			self.distStart()
		else:
			pass

		if secondvalue != 0:
		   time.sleep(secondvalue)
		   self.stop()

	def t_stop(self):
		self.setup()
		GPIO.output(self.IN1, False)
		GPIO.output(self.IN2, False)
		GPIO.output(self.IN3, False)
		GPIO.output(self.IN4, False)
		self.checkdiststate = False

	def distStart(self):
		self.diststart = True
		try:
			while self.checkdiststate:
				self.warn()
				if  self.checkdist() <= 50 and self.checkdist()>=15 :
					# self.speedChange('dec')
					print('attention!!')
				elif  self.checkdist() < 15 :
					self.t_stop()
					time.sleep(0.3)
					self.t_down()
					time.sleep(0.2)
					self.t_stop()
					print('stop!!')
				time.sleep(0.5)
		except KeyboardInterrupt:
				GPIO.cleanup()

	# 红外避障
	def warn(self):
		GPIO.setup(self.IR_LF, GPIO.IN)
		GPIO.setup(self.IR_LB, GPIO.IN)
		GPIO.setup(self.IR_RF, GPIO.IN)
		GPIO.setup(self.IR_RB, GPIO.IN)
		time.sleep(0.00015)
		if GPIO.input(self.IR_LF) == 0:
			self.t_stop()
			time.sleep(0.2)
			self.t_down()
			time.sleep(0.3)
			self.t_right()
			time.sleep(0.1)
			self.t_stop()
		elif GPIO.input(self.IR_RF) == 0:
			self.t_stop()
			time.sleep(0.2)
			self.t_down()
			time.sleep(0.3)
			self.t_left()
			time.sleep(0.1)
			self.t_stop()
		elif GPIO.input(self.IR_LB) == 0:
			self.t_stop()
			time.sleep(0.2)
			self.t_up()
			time.sleep(0.3)
			self.t_right()
			time.sleep(0.1)
			self.t_stop()
		elif GPIO.input(self.IR_RB) == 0:
			self.t_stop()
			time.sleep(0.2)
			self.t_up()
			time.sleep(0.3)
			self.t_left()
			time.sleep(0.1)
			self.t_stop()
	
	
	# 超声波距离探测
	def checkdist(self):
		GPIO.setup(self.Trig, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.Echo, GPIO.IN)
		GPIO.output(self.Trig, GPIO.HIGH)
		time.sleep(0.00015)
		GPIO.output(self.Trig, GPIO.LOW)
		while not GPIO.input(self.Echo):
			pass
		t1 = time.time()
		while GPIO.input(self.Echo):
			pass
		t2 = time.time()
		return (t2-t1)*340*100/2

