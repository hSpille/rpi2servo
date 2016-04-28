import tkinter
import socket
import sys
import pygame
from pygame.locals import *
from tkinter import *
from random import randint

#ConfigStuff
lastBrakeValue = 0
lastSteerValue = 0
lastSpeedValue = 0
chokeMinValue= 10
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.1', 10001)
chokeButtonText = 'Choke'
gamepadName = "none connected"
chokeIsOn = False

#TkInterStuff
root = tkinter.Tk()
root.title("RC-Control")
root.geometry("450x250+100+50")




pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
jStick =""
for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print("Found:" +joystick.get_name())
        gamepadName = joystick.get_name()
        if(i == 0):
        	jStick = joystick

def chokeFunc():
	global chokeLabel
	global chokeIsOn
	if(chokeIsOn):
		chokeLabel.config(text='OFF')
		chokeLabel.config(bg=root.cget('bg'))
		chokeIsOn = False
		speedValue("0")
		scale2.set(0)
	else:
		chokeLabel.config(text='ON')
		chokeLabel.config(bg="blue")
		chokeIsOn = True



def speedValue(val):
	if(int(val) < 150):
		return
	global lastSpeedValue
	if(val == lastSpeedValue):
		return
	lastSpeedValue = val
	print ("Speed:" + val)
	sent = sock.sendto(bytes('speed:'+val,'UTF-8'), server_address)

def brakeValue(val):
	if(int(val) < 150):
		return
	global lastBrakeValue
	if(lastBrakeValue == val):
		return
	lastBrakeValue = val
	print ("Brake:" + val)
	sent = sock.sendto(bytes('brake:'+val,'UTF-8'), server_address)


def steerValue(val):
	if(int(val) < 150):
		return
	global lastSteerValue
	if(lastSteerValue == val):
		return
	lastSteerValue  = val
	print ("Steerx:" +val)
	sent = sock.sendto(bytes('steer:'+val, 'UTF-8'), server_address)


def gamepadStuff():
	global chokeIsOn
	if(not chokeIsOn):
		for event in pygame.event.get(): 
			if event.type == pygame.JOYBUTTONDOWN:
				print("Joystick button pressed.")
			if event.type == pygame.JOYBUTTONUP:
				print("Joystick button released.")
			#Brake
			value = ((jStick.get_axis(12) * 100)+ 100) / 2
			scale3.set(int(round(value)))
			value =  375 - (value)*2.25 
			brakeValue(str(+int(round(value))))
			#Speed
			value = ((jStick.get_axis(13) * 100) +100) / 2
			scale2.set(int(round(value)))
			value =  (value)*2 + 375
			speedValue(str(+int(round(value))))
			#Steer:
			#300 Min 
			#445 Max
			value = ((jStick.get_axis(0) * 100)) / 2
			scale.set(int(round(value)))
			value =  (value+50)*1.45 + 300
			steerValue(str(+int(round(value))))
		root.after(50, gamepadStuff)
		return
	else:
		toSet = chokeMinValue + randint(0,20)
		scale2.set(toSet)
		sock.sendto(bytes('speed:'+ str((chokeMinValue + randint(0,20)) *2+375),'UTF-8'), server_address)
	root.after(200, gamepadStuff)
	


pygame.init()

padLabel = Label(root, text="Gamepad: " ,fg="black", height=1)
padLabel.grid(row=0,column=1)
caripLabel = Label(root, text="RC-Car-IP: ", fg="black", height=1)
caripLabel.grid(row=1,column=1)

pad = Label(root, text=gamepadName  ,fg="black", height=1)
pad.grid(row=0,column=2)
carip = Label(root, text=server_address, fg="black", height=1)
carip.grid(row=1,column=2)

steer = Label(root, text="Steer",  fg="black", height=2)
steer.grid(row=2,column=2)
scale = tkinter.Scale(orient='horizontal', from_=-50, to=50, command=steerValue)
scale.grid(row=3, column=2 )

speed = Label(root, text="Speed", bg="green", fg="white", height=2)
speed.grid(row=2,column=3)
scale2 = tkinter.Scale(orient='vertical', from_=100, to=0, command=speedValue)
scale2.grid(row=3, column=3)

brake = Label(root, text="Brake", bg="red", fg="white", height=2)
brake.grid(row=2,column=4)
scale3 = tkinter.Scale(orient='vertical', from_=100, to=0, command=brakeValue)
scale3.grid(row=3, column=4)

chokeLabel = Label(root, text="off", fg="black", height=2)
chokeLabel.grid(row=4,column=2)
b = Button(root, text=chokeButtonText ,command=chokeFunc)
b.grid(row=4,column=1)



e1 = Entry(scale)
e2 = Entry(scale2)
e3 = Entry(scale3)


root.after(25, gamepadStuff)
root.mainloop()


