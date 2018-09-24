
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCamPanTilt.py
#  	Streaming video with Flask based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with PanTilt position Control
#
#   MJRoBot.org 30Jan18

import os
from time import sleep
from flask import Flask, render_template, request, Response

import RPi.GPIO as GPIO
import time
# Raspberry Pi camera module (requires picamera package from Miguel Grinberg)
from camera_pi import Camera
import stateCtrl as SC

app = Flask(__name__)

# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90

global speed
speed = 50

panPin = 29
tiltPin = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#######PWM车速控制###########
ENA = 33  # //L298使能A
ENB = 35  # //L298使能B

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
leftpwm = GPIO.PWM(ENA, 1000)
rightpwm = GPIO.PWM(ENB, 1000)
leftpwm.start(100)
rightpwm.start(100)
print('pwm start')
#######PWM车速控制###########


@app.route('/')
def index():
	"""Video streaming home page."""

	templateData = {
	  'panServoAngle'	: panServoAngle,
	  'tiltServoAngle'	: tiltServoAngle
	}
	return render_template('index.html', **templateData)


def gen(camera):
	"""Video streaming generator function."""
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

## 这个是摄像头画面，没装摄像头就把这个函数注释掉
@app.route('/video_feed')
def video_feed():
	"""Video streaming route. Put this in the src attribute of an img tag."""
	return Response(gen(Camera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/camera/<servo>/<angle>")
def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		if angle == '+':
			panServoAngle = panServoAngle + 10
		else:
			panServoAngle = panServoAngle - 10
		os.system("python3 angleServoCtrl.py " +
				  str(panPin) + " " + str(panServoAngle))
	if servo == 'tilt':
		if angle == '+':
			tiltServoAngle = tiltServoAngle + 10
		else:
			tiltServoAngle = tiltServoAngle - 10
		os.system("python3 angleServoCtrl.py " +
				  str(tiltPin) + " " + str(tiltServoAngle))

	templateData = {
	  'panServoAngle'	: panServoAngle,
	  'tiltServoAngle'	: tiltServoAngle
	}
	return render_template('index.html', **templateData)


@app.route("/ctrl/<state>")
def ctrl(state):
		car = SC.stateCtrl()
		if state == "t_up":
			car.t_up()
		elif state == "t_down":
			car.t_down()
		elif state == "t_left":
			car.t_left()
		elif state == "t_right":
			car.t_right()
		elif state == 't_stop':
			car.t_stop()
		return render_template('index.html')


@app.route("/speed/<state>")
def speedChange(state):
		global speed
		car = SC.stateCtrl()
		if state == 'acc':
			speed = speed + 10
			if int(speed) >= 100:
				speed = 100
			# car.changeSpeed(int(speed))
			leftpwm.ChangeDutyCycle(int(speed))
			rightpwm.ChangeDutyCycle(int(speed))
		elif state == 'dec':
			speed = speed - 10
			if int(speed) <= 0:
				speed = 0
			leftpwm.ChangeDutyCycle(int(speed))
			rightpwm.ChangeDutyCycle(int(speed))
		else:
			speed == 60   #复位到60
			leftpwm.ChangeDutyCycle(int(speed))
			rightpwm.ChangeDutyCycle(int(speed))

		return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port =8000)

