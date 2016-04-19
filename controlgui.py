import tkinter
import socket
import sys
import pygame
from pygame.locals import *


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.178.58', 10001)


def speedValue(val):
	if(val > 150):
		return
    print ("Speedx:" + val)
    sent = sock.sendto(bytes('speed:'+val,'UTF-8'), server_address)

def steerValue(val):
	if(val > 150):
		return
    print ("Steerx:" +val)
    sent = sock.sendto(bytes('steer:'+val, 'UTF-8'), server_address)


def gamepadStuff(): 
	for event in pygame.event.get(): 
		if event.type == pygame.JOYBUTTONDOWN:
			print("Joystick button pressed.")
		if event.type == pygame.JOYBUTTONUP:
			print("Joystick button released.")
		if event.type == pygame.JOYAXISMOTION:
			if(event.axis == 5):
				value = ((event.value * 100) + 100) / 2
				scale2.set(int(round(value)))
				value =  value*4.5 + 150
				speedValue(str(+int(round(value))))
			if(event.axis == 0):
				value = ((event.value * 100)) / 2
				scale.set(int(round(value)))
				value =  (value+50)*4.5 + 150
				steerValue(str(+int(round(value))))
	root.after(50, gamepadStuff)

pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print("Found:" +joystick.get_name())
pygame.init()
root = tkinter.Tk()
root.title("control the blind")
root.geometry("350x200+100+50")
scale = tkinter.Scale(orient='horizontal', from_=-50, to=50, command=steerValue)
scale2 = tkinter.Scale(orient='vertical', from_=100, to=0, command=speedValue)

scale.pack()
scale.set(0)
scale2.pack()

root.after(25, gamepadStuff)
root.mainloop()


