import RPi.GPIO as GPIO
import time
from threading import Thread
from pygame import mixer

GPIO.setmode(GPIO.BCM)

#Initilize the mixer
mixer.init()

BBL = 26
RBL = 19
GBL = 13
YBL = 6
WBL = 12
l1 = 16
l2 = 20
r8 = 21

#I need to set these values
BB = 
RB = 
GB = 
YB = 
#White Button is mode changer
WB = 

#Light Mode 1 through 5
RMode = 4

#Audio on or off
YMode = 1

#Toggle Buttons on and off
GMode = 1

#No use rn
BMode = 1

#GPIO Pin setup
GPIO.setup(BBL, GPIO.OUT)
GPIO.setup(RBL, GPIO.OUT)
GPIO.setup(GBL, GPIO.OUT)
GPIO.setup(YBL, GPIO.OUT)
GPIO.setup(WBL, GPIO.OUT)
GPIO.setup(l1, GPIO.OUT)
GPIO.setup(l2, GPIO.OUT)
GPIO.setup(r8, GPIO.OUT)
GPIO.setup(BB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(YB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(WB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Initilize the outputs so the relays are off
GPIO.output(BBL, 1)
GPIO.output(RBL, 1)
GPIO.output(GBL, 1)
GPIO.output(YBL, 1)
GPIO.output(WBL, 1)
GPIO.output(l1, 1)
GPIO.output(l2, 1)
GPIO.output(r8, 1)

def light_thread():
	global RMode
	
	while True:
		#Check which light mode and blink lights accordingly
		if RMode == 1:
			GPIO.output(l1, 1)
			GPIO.output(l2, 1)
		elif RMode == 2:
			GPIO.output(l1, 0)
			GPIO.output(l2, 0)
		elif RMode == 3:
			GPIO.output(l1, 1)
			GPIO.output(l2, 0)
			#Might have to adjust timing
			time.sleep(1.5)
			GPIO.output(l1, 0)
			GPIO.output(l2, 1)
		elif RMode == 4:
			GPIO.output(l1, 0)
			GPIO.output(l2, 0)
			time.sleep(1)
			GPIO.output(l1, 1)
			GPIO.output(l2, 1)
		elif RMode == 5:
			GPIO.output(l1, 0)
			GPIO.output(l2, 1)
			time.sleep(1)
			GPIO.output(l1, 0)
			GPIO.output(l2, 0)
			time.sleep(1)
			GPIO.output(l1, 1)
			GPIO.output(l2, 1)
			
def button_light_thread():
	#Check if buttons are enabled
	global GMode
	
	while True:
		if(GMode or GPIO.input(WB)):
			if GPIO.input(RB):
				GPIO.output(RBL, 1)
				GPIO.output(BBL, 1)
				GPIO.output(GBL, 1)
				GPIO.output(YBL, 1)
				time.sleep(1)
				GPIO.output(BBL, 0)
				GPIO.output(GBL, 0)
				GPIO.output(YBL, 0)
			elif GPIO.input(YB):
				GPIO.output(YBL, 1)
				GPIO.output(BBL, 1)
				GPIO.output(RBL, 1)
				GPIO.output(GBL, 1)
				time.sleep(1)
				GPIO.output(BBL, 0)
				GPIO.output(RBL, 0)
				GPIO.output(GBL, 0)
			elif GPIO.input(BB):
				GPIO.output(BBL, 1)
				GPIO.output(RBL, 1)
				GPIO.output(GBL, 1)
				GPIO.output(YBL, 1)
				time.sleep(1)
				GPIO.output(RBL, 0)
				GPIO.output(GBL, 0)
				GPIO.output(YBL, 0)
			elif GPIO.input(GB):
				GPIO.output(GBL, 1)
				GPIO.output(BBL, 1)
				GPIO.output(RBL, 1)
				GPIO.output(YBL, 1)
				time.sleep(1)
				GPIO.output(BBL, 0)
				GPIO.output(RBL, 0)
				GPIO.output(YBL, 0)
			elif GPIO.input(WB):
				GPIO.output(WBL, 1)
				GPIO.output(BBL, 1)
				GPIO.output(RBL, 1)
				GPIO.output(GBL, 1)
				GPIO.output(YBL, 1)
				time.sleep(1)
				GPIO.output(BBL, 0)
				GPIO.output(RBL, 0)
				GPIO.output(GBL, 0)
				GPIO.output(YBL, 0)
			else:
				GPIO.output(BBL, 1)
				GPIO.output(RBL, 1)
				GPIO.output(GBL, 1)
				GPIO.output(YBL, 1)
				time.sleep(1)
				GPIO.output(BBL, 0)
				GPIO.output(RBL, 0)
				GPIO.output(GBL, 0)
				GPIO.output(YBL, 0)
			time.sleep(1)
		else:
			#Turn button lights off
			GPIO.output(BBL, 1)
			GPIO.output(RBL, 1)
			GPIO.output(GBL, 1)
			GPIO.output(YBL, 1)

def input_thread():
	global RMode
	global GMode

while True:
	if GPIO.input(WB):
		if GPIO.input(RB):
			if RMode == 1:
				RMode = 2
			elif RMode == 2:
				RMode = 3
			elif RMode == 3:
				RMode = 4
			elif RMode == 4:
				RMode = 5
			elif RMode == 5:
				RMode = 1
				time.sleep(1)
		elif GPIO.input(YB):
			#1 = music on
			#0 = music off
			if YMode == 1:
				YMode = 0
			elif YMode == 0:
				YMode = 1
		elif GPIO.input(GB):
			if GMode == 1:
				GMode = 0
			elif GMode == 0:
				GMode = 1
		elif GPIO.input(BB):
			if BMode == 1:
				BMode = 0
			elif BMode == 0:
				BMode = 1		
	else:
		#Check if buttons are active
		if not GMode:
			#Do nothing until active again
		else:
			#Red Button Siren and Fire Engine Sound
			if GPIO.input(RB):
				#Turn siren lights on
				GPIO.output(r8, 0)
				#Check if sound should play
				if YMode:
					mixer.music.load("fire_engine.mp3")
					mixer.music.play()
				#Change value based on length of audio clip?
				time.sleep(5)
				#Might have to pause music, it might automatically loop
				#Turn off siren lights
				GPIO.output(r8, 1)
			elif GPIO.input(YB):
				GPIO.output(YBL, 0)
				if YMode:
					mixer.music.load("911_operator.mp3")
					mixer.music.play()
				#Change value based on length of audio clip
				time.sleep(5)
				#Might have to pause music, it might not loop
				GPIO.output(YBL, 1)
			elif GPIO.input(GB):
				GPIO.output(GBL, 0)
				GPIO.output(r8, 0)
				if YMode:
					mixer.music.load("move_stations.mp3")
					mixer.music.play()
				#Change value based on length of audio clip
				time.sleep(5)
				#Might have to pause music, it might not loop
				GPIO.output(GBL, 1)
				GPIO.output(r8, 1)
			elif GPIO.input(BB):
				GPIO.output(BBL, 0)
				if YMode:
					mixer.music.load("police_radio.mp3")
					mixer.music.play()
				#Change value based on length of audio clip
				time.sleep(5)
				#Might have to pause music, it might not loop
				GPIO.output(BBL, 1)

#Launch Threads
thread1 = Thread(target = light_thread)
thread2 = Thread(target = button_light_thread)
thread3 = Thread(target = input_thread)
					
			
			
