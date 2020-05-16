import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) # GPIO ids are from GPIO, not pins
BUTTON = 17 # GPIO 17, PIN 11
BUZZER = 26 # GPIO 26, PIN 37


GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.output(BUZZER, GPIO.LOW)

def buzz(noteFreq, duration):
    halveWaveTime = 1 / (noteFreq * 2 )
    waves = int(duration * noteFreq)
    for i in range(waves):
       GPIO.output(BUZZER, GPIO.HIGH)
       sleep(halveWaveTime)
       GPIO.output(BUZZER, GPIO.LOW)
       sleep(halveWaveTime)

def play():
    t=0
    notes=[262,294,330,262,262,294,330,262,330,349,392,330,349,392,392,440,392,349,330,262,392,440,392,349,330,262,262,196,262,262,196,262]
    duration=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.25,0.25,0.5,0.5,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,1,0.5,0.5,1]
    for n in notes:
        buzz(n, duration[t])
        sleep(duration[t] *0.1)
        t+=1

try:
	while True:
		if GPIO.input(BUTTON):
			print("Someone is ringing !!!")
			buzz(262,0.5)	
			sleep(2)
			#play()
			#GPIO.output(BUZZER, GPIO.HIGH)
			#sleep(0.5)
			#GPIO.output(BUZZER, GPIO.LOW)
			#sleep(1.5)
		else:
			sleep(0.01)
finally:
	GPIO.cleanup()
