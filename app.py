from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

@app.route('/')
def index():
	return render_template('index.html') 

@app.route('/<command>')
def process(command):
	if command == 'open':
		GPIO.output(18,0)
	elif command == 'close':
		GPIO.output(18,1)
	return command+'ed door!'
	
if __name__ == '__main__':
	app.run(debug=True, host ='0.0.0.0')
