from flask import Flask, render_template
import time
from math import *
import os
app = Flask(__name__)
@app.route("/")
def getPage():
	templateData = {
		'title' : 'Robot Control'
	}
	return render_template('index.html', **templateData)
	
@app.route("/forward", methods=['GET', 'POST'])
def forward():
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
	return ('', 204)

@app.route("/confirm", methods=['GET', 'POST'])
def confirm():
	return ('', 204)

try:
	if __name__ == "__main__":
		# setup_GPIO()
		app.run(host='0.0.0.0', port=5002, debug=True)
finally:
	# GPIO.cleanup()
	print("finish")