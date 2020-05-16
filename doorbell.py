import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) # GPIO ids are from GPIO, not pins
BUTTON = 17 # GPIO 17, PIN 11
BUZZER = 26 # GPIO 26, PIN 37

GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.output(BUZZER, GPIO.LOW)
buzzer = GPIO.PWM(BUZZER, 100)
buzzer.start(50)

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
c = [32, 65, 131, 262, 523]
db= [34, 69, 139, 277, 554]
d = [36, 73, 147, 294, 587]
eb= [37, 78, 156, 311, 622]
e = [41, 82, 165, 330, 659]
f = [43, 87, 175, 349, 698]
gb= [46, 92, 185, 370, 740]
g = [49, 98, 196, 392, 784]
ab= [52, 104, 208, 415, 831]
a = [55, 110, 220, 440, 880]
bb= [58, 117, 223, 466, 932]
b = [61, 123, 246, 492, 984]

#notes of two scales, feel free to add more
cmajor = [c, d, e, f, g, a, b]
aminor = [a, b, c, d, e, f, g]

#Star Wars Theme -- Key of C
starwars_notes = [c[1], g[1], f[1], e[1], d[1], c[2], g[1], f[1], e[1], d[1], c[2], g[1], 
              f[1], e[1], f[1], d[1]]
starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]

#London Bridges --Key of C
londonbridges_notes = [g[1], a[1], g[1], f[1], e[1], f[1], g[1], d[1], e[1], f[1],
                   e[1], f[1], g[1], g[1], a[1], g[1], f[1], e[1], f[1], g[1],
                   d[1], g[1], e[1], c[1]]
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
            time.sleep(pause)
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
    buzzer.ChangeDutyCycle(50)
    for i in range(0, len(songnotes)):
        buzzer.ChangeFrequency(songnotes[i])
        time.sleep(songbeats[i]*tempo)
    buzzer.ChangeDutyCycle(0)

try:
	while True:
		if GPIO.input(BUTTON):
			print("Someone is ringing !!!")
			playSong(starwars_notes, starwars_beats, 0.2)
			playSong(londonbridges_notes, londonbridges_beats, 0.3)	
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
