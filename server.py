from flask import Flask, render_template
import time
from math import *
import os
import rcpy
import rcpy.motor as motor
from rcpy.motor import motor1,motor2,motor3
import rcpy.encoder as encoder
import rcpy.clock as clock





#Duty Time
DT = 0.02
DTus = DT*1000000


#max of Pulse Width Modulation
PWM_max=0.99

#1500 pulses/ rotation
#pi = pi   
COD = 1500/2.0/pi



#Function to avoid over value of pwm
def sature(v):
	if(v>PWM_max):
		return PWM_max
	if(v<-PWM_max):
		return -PWM_max
	return v

#Function to control with speed of the 4 wheels the duty cycle voltage of the motors		
class regulation(clock.Action):
	def __init__(self):
		#global speed in rad/s of the 4 wheels(for a robot with 4 wheels)

		#To gather the positions of the motors
		self.cod1=0
		self.cod2=0
		self.cod3=0
		#self.cod4=0
		
		#command in voltage duty cycle
		self.cmd1=0
		self.cmd2=0
		self.cmd3=0
		#self.cmd4=0

		self.err1=0
		self.err2=0
		self.err3=0
		#self.err4=0

		self.c_cod1=0
		self.c_cod2=0
		self.c_cod3=0
		#self.c_cod4=0

	
	
	def run(self):
		global w1,w2,w3
		t0 = time.clock_gettime(time.CLOCK_REALTIME)#get the real time
		#to enslave position
		self.c_cod1=self.c_cod1+w1*DT*COD
		self.c_cod2=self.c_cod2+w2*DT*COD
		self.c_cod3=self.c_cod3+w3*DT*COD
		#self.c_cod4=self.c_cod4+w4*DT*COD

		#Read Encodeur
		self.cod1=encoder.get(1)
		self.cod2=encoder.get(2)
		self.cod3=encoder.get(3)
		#self.cod4=encoder.get(4)
		#print("cod 1 2 and 3: ",self.cod1,self.cod2,self.cod3)#,self.cod4)

		self.err1=self.c_cod1-self.cod1
		self.err2=self.c_cod2-self.cod2
		self.err3=self.c_cod3-self.cod3
		#self.err4=self.c_cod4-self.cod4

		KP = 0.01#corrector proportionnal
		self.cmd1=KP*self.err1
		self.cmd2=KP*self.err2
		self.cmd3=KP*self.err3
		#self.cmd4=KP*self.err4

		#limit pwm command -1< cmd <1
		self.cmd1=sature(self.cmd1)
		self.cmd2=sature(self.cmd2)
		self.cmd3=sature(self.cmd3)
		#self.cmd4=sature(self.cmd4)
		#print("cmd1 :", self.cmd1, "cmd2 :",self.cmd2, "cmd3 :", self.cmd3)

		motor1.set(self.cmd1)
		motor2.set(self.cmd2)
		motor3.set(self.cmd3)
		#motor4.set(self.cmd4) #No need because we have just 3 wheels

		t1 = time.clock_gettime(time.CLOCK_REALTIME)#get the real time
		wait = DT -(t1-t0) 
		print("wait time in s is : ",wait)
		time.sleep(wait)#wait for the execution of the thread_regul


#Function to control the speed  of the 3 wheels with the speed of forward/backward(u)(m/s);Go_left/Go_right(v)(m/s);turn_no_clockwise(w)(rad/s)
def command(u,v,w):
	global w1,w2,w3,thread_regul
	w1=0
	w2=0
	w3=0
	#thread_regul.toggle()#unpause the thread_regul
	
	thread_regul.cod1=0
	thread_regul.cod2=0
	thread_regul.cod3=0

	thread_regul.cmd1=0
	thread_regul.cmd2=0
	thread_regul.cmd3=0

	thread_regul.err1=0
	thread_regul.err2=0
	thread_regul.err3=0

	thread_regul.c_cod1=0
	thread_regul.c_cod2=0
	thread_regul.c_cod3=0
	
	w1=(-(u)*sin(0)+v*cos(0)+1*w)/3
	w2=(-(u)*sin((2**pi)/3)+v*cos((2*3*pi)/3)+1*w)/3
	w3=(-(u)*sin((-2**pi)/3)+v*cos((-2*pi)/3)+1*w)/3

def stop_motors():
	
	global w1,w2,w3,thread_regul
	"""
	thread_regul.toggle()#unpause the thread_regul
	"""
	w1=0
	w2=0
	w3=0
	motor1.brake()
	motor2.brake()
	motor3.brake()

speed = 1
app = Flask(__name__)
@app.route("/")
def getPage():
	templateData = {
		'title' : 'Robot Control'
	}
	return render_template('index.html', **templateData)
	
@app.route("/forward", methods=['GET', 'POST'])
def forward():
	command(100*speed,0,0)
	print("Avance")
	return ('', 204)

@app.route("/backward", methods=['GET', 'POST'])
def backward():
	# robot_travel(False)
	return ('', 204)

@app.route("/turnRight", methods=['GET', 'POST'])
def turn_right():
	# robot_turn(True)
	return ('', 204)

@app.route("/turnLeft", methods=['GET', 'POST'])
def turn_left():
	# robot_turn(False)
	return ('', 204)

@app.route("/stop", methods=['GET', 'POST'])
def stop():
	stop_motors()
	return ('', 204)

try:
	if __name__ == "__main__":
		# setup_GPIO()
		app.run(host='0.0.0.0', port=5002, debug=True)
finally:
	# GPIO.cleanup()
	print("finish")