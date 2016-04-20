import tkinter
import socket
import sys
import pygame
from pygame.locals import *


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.178.58', 10001)

pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
jStick =""
for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print("Found:" +joystick.get_name())
        if(i == 0):
        	jStick = joystick





def speedValue(val):
	if(int(val) < 150):
		return
	print ("Speed:" + val)
	sent = sock.sendto(bytes('speed:'+val,'UTF-8'), server_address)

def brakeValue(val):
	if(int(val) < 150):
		return
	print ("Brake:" + val)
	sent = sock.sendto(bytes('brake:'+val,'UTF-8'), server_address)



def steerValue(val):
	if(int(val) < 150):
		return
	print ("Steerx:" +val)
	sent = sock.sendto(bytes('steer:'+val, 'UTF-8'), server_address)


def gamepadStuff(): 
	for event in pygame.event.get(): 
		print("Brake: ", jStick.get_axis(12))
		print("Speed: ", jStick.get_axis(13))
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
		value =  (value)*2.25 + 375
		speedValue(str(+int(round(value))))
		#Steer:
		value = ((jStick.get_axis(0) * 100)) / 2
		scale.set(int(round(value)))
		value =  (value+50)*4.5 + 150
		steerValue(str(+int(round(value))))
	root.after(50, gamepadStuff)


pygame.init()
root = tkinter.Tk()
root.title("control the blind")
root.geometry("350x200+100+50")
scale = tkinter.Scale(orient='horizontal', from_=-50, to=50, command=steerValue)
scale2 = tkinter.Scale(orient='vertical', from_=100, to=0, command=speedValue)
scale3 = tkinter.Scale(orient='vertical', from_=100, to=0, command=brakeValue)

scale.pack()
scale2.pack()
scale3.pack()


root.after(25, gamepadStuff)
root.mainloop()


