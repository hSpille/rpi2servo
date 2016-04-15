import tkinter
import socket
import sys
import pygame
from pygame.locals import *


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10001)


def speedValue(val):
    print ("Speed:" + val)
    sent = sock.sendto(bytes('Speed:'+val,'UTF-8'), server_address)

def steerValue(val):
    print ("Steer:" +val)
    sent = sock.sendto(bytes('Steer:'+val, 'UTF-8'), server_address)


def gamepadStuff(): 
	for event in pygame.event.get(): 
		if event.type == pygame.JOYBUTTONDOWN:
			print("Joystick button pressed.")
		if event.type == pygame.JOYBUTTONUP:
			print("Joystick button released.")
		if event.type == pygame.JOYAXISMOTION:
			if(event.axis == 5):
				value = ((event.value * 100) + 100) / 2
				speedValue(str(+int(round(value))))
				scale2.set(int(round(value)))

			
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


