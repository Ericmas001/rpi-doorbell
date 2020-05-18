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

buzzer = GPIO.PWM(BUZZER, 8000)
buzzer.start(0)

'''
How melodies are transposed into code that is played on buzzer:

Every song needs two lists, one to store the variables for the notes and octaves,
and one to store the corresponding lengths of the beats for each note.
The length of both lists MUST be the same. Numbers are used to indicate the note length.
In the case of most melodies:

0.5 = eighth 
1 = quarter note
2 = half note
3 = dotted half note
4 = whole note

This is a relative system, even if a piece is composed mainly in eighth notes or smaller
you should convert the time so that you're using mainly values of 1, 2, 3, and 4 for your notes list.
Actual numbers can be adjusted up or down slightly to account for any fermata or accents,
for example a quarter note with a fermata could be a value of 1.05 or 1.1.

The actual tempo is adjusted when the song is played. The note number system decribed above
is to classify the notes RELATIVE to each other in the song, not when the song is played.
Tempo can be experimentally tested when the function to play the song is called.

All songs should be composed in the key of C whenever possible as the lowest note available
is a C and doing so would simplify the octave referencing.

The easiest way to encode a song's info so it can be played is to do it by ear.
This method and the playSong function currently only support one buzzer, though in the 
future two buzzer support might be added. 
'''
#Note frequencies, starting with a C
#speaker works good from 32hz to about 500hz, so the first four octaves here, fifth octave just for fun
#in case you're not familiar with musical notation, the 'b' after some of these indicates a flat so 'db' is 'd-flat'
c = [0, 32, 65, 131, 262, 523, 0]
db= [0, 34, 69, 139, 277, 554, 0]
d = [0, 36, 73, 147, 294, 587, 0]
eb= [0, 37, 78, 156, 311, 622, 0]
e = [0, 41, 82, 165, 330, 659, 0]
f = [0, 43, 87, 175, 349, 698, 0]
gb= [0, 46, 92, 185, 370, 740, 0]
g = [0, 49, 98, 196, 392, 784, 0]
ab= [0, 52, 104, 208, 415, 831, 0]
a = [0, 55, 110, 220, 440, 880, 0]
bb= [0, 58, 117, 223, 466, 932, 0]
b = [0, 61, 123, 246, 492, 984, 0]
s = 0

#notes of two scales, feel free to add more
cmajor = [c, d, e, f, g, a, b]
aminor = [a, b, c, d, e, f, g]

z = 4

#Doorbell
doorbell_notes = [a[z], a[z+1], a[z], s, e[z], e[z+1], e[z], s, c[z], c[z+1], c[z], s]
doorbell_beats = [0.1, 0.25, 0.1, 0.25, 0.1, 0.25, 0.1, 0.25, 0.1, 0.25, 0.1, 1]

doorbell2_notes = [a[1+z], s, e[1+z], s, g[1+z], s, c[1+z], s, c[1+z], s, g[1+z], s, a[1+z], s, e[1+z], s]
doorbell2_beats = [0.5, 0.25, 0.5, 0.25, 0.5, 0.25, 1, 0.5, 0.5, 0.25, 0.5, 0.25, 0.5, 0.25, 1, 0.5]

doorbell3_beats = [0.25, 0.25, 0.5, 0.25]
doorbell3_notes = [a[4], s, a[3], s]

#Star Wars Theme -- Key of C
starwars_notes = [c[1+z], g[1+z], f[1+z], e[1+z], d[1+z], c[2+z], g[1+z], f[1+z], e[1+z], d[1+z], c[2+z], g[1+z], 
              f[1+z], e[1+z], f[1+z], d[1+z]]
starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]

#London Bridges --Key of C
londonbridges_notes = [g[1+z], a[1+z], g[1+z], f[1+z], e[1+z], f[1+z], g[1+z], d[1+z], e[1+z], f[1+z],
                   e[1+z], f[1+z], g[1+z], g[1+z], a[1+z], g[1+z], f[1+z], e[1+z], f[1+z], g[1+z],
                   d[1+z], g[1+z], e[1+z], c[1+z]]
londonbridges_beats = [2, 0.5, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0.5, 1, 1, 1, 1,
                   2, 2, 2, 1,1]

def playScale(scale, pause):
    '''
    scale: scale name to be played
	    pause: pause between each notes played
    
    This function plays the given scale in every available octave
    I used this to test what was audible on the buzzer
    '''
    for i in range(0, 5):
        for note in scale:
            buzzer.ChangeFrequency(note[i])
            sleep(pause)
    buzzer.stop()

#call the playScale function   
#playScale(aminor, 0.5)

def playSong(songnotes, songbeats, tempo):
    '''
    songnotes: list of the melodies notes
    songbeats: list of melodies beat times
    tempo: speed of song, this is not traditional tempo in bpm like on a metronome, 
        but more like a multiplier for whatever the notes are so a tempo value of 2 
        make it play twice as fast. Adjust this by ear.
        
    This function plays the melody, simply by iterating through the list. 
    '''
    #buzzer.ChangeDutyCycle(50)
    for i in range(0, len(songnotes)):
	if songnotes[i] > 0:
		buzzer.ChangeDutyCycle(50)
        	buzzer.ChangeFrequency(songnotes[i])
	else:
		buzzer.ChangeDutyCycle(0)
        sleep(songbeats[i]*tempo)
    buzzer.ChangeDutyCycle(0)

try:
	while True:
		if GPIO.input(BUTTON):
			print("Someone is ringing !!!")
#			playSong(doorbell_notes,doorbell_beats,0.2)
#			sleep(0.5)
#			playSong(doorbell2_notes,doorbell2_beats,0.5)
#			sleep(0.5)
			playSong(doorbell3_notes,doorbell3_beats,0.2)
			sleep(0.5)
			#playSong(starwars_notes, starwars_beats, 0.2)
			#sleep(0.5)
			#playSong(londonbridges_notes, londonbridges_beats, 0.3)
			#sleep(0.5)
			#play()
			#buzz(50000,1)
			#GPIO.output(BUZZER, 0.1)
			#sleep(0.5)
			#GPIO.output(BUZZER, 0)
			#sleep(1.5)
		else:
			sleep(0.01)
finally:
	GPIO.cleanup()
