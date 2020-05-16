import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) # GPIO ids are from GPIO, not pins
BUTTON = 17 # GPIO 17, PIN 11
BUZZER = 26 # GPIO 26, PIN 37


GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.output(BUZZER, GPIO.LOW)

try:
	while True:
		if GPIO.input(BUTTON):
			print("Someone is ringing !!!")
			GPIO.output(BUZZER, GPIO.HIGH)
			sleep(0.5)
			GPIO.output(BUZZER, GPIO.LOW)
			sleep(1.5)
		else:
			sleep(0.01)
finally:
	GPIO.cleanup()
