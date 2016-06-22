import tkinter
import socket
import sys
import time
import pygame
import fcntl, os
import errno
from pygame.locals import *
from tkinter import *
from random import randint
import json
import gpxpy 
import gpxpy.gpx 

#ConfigStuff
lastBrakeValue = 0
lastSteerValue = 0
lastSpeedValue = 0
chokeMinValue= 10
elevationValue = 0
#sendSocket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.10.1 ', 10001)
#receive
listenInterface = "0.0.0.0"
listenPort = 12000
#gps
longitude = None
latitude = None
altitude = None
speed = None
receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
receiverSocket.bind((listenInterface, listenPort))
fcntl.fcntl(receiverSocket, fcntl.F_SETFL, os.O_NONBLOCK)
chokeButtonText = 'Choke'
gamepadName = "none connected"
chokeIsOn = False

#TkInterStuff
root = tkinter.Tk()
root.title("RC-Control")
root.geometry("450x250+100+50")

#gpx logging
gpx = None
gpx_track = None
gpx_segment = None



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


def createGpxTrack():
	global gpx 
	gpx = gpxpy.gpx.GPX() 
	global gpx_track 
	gpx_track = gpxpy.gpx.GPXTrack() 
	gpx.tracks.append(gpx_track) 
	global gpx_segment 
	gpx_segment = gpxpy.gpx.GPXTrackSegment() 
	gpx_track.segments.append(gpx_segment) 

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


def readFromNav():
	msg = None
	data = None
	try:
		msg = receiverSocket.recv(4096)
		jsonString = msg.decode("UTF-8")
		with open("gpslog.txt", "a") as text_file:
			print(jsonString, file=text_file)
		data = json.loads(jsonString.replace("=",":"))
		global elevationValue
		elevationValue = elevationValue + 1
		point =  gpxpy.gpx.GPXTrackPoint(data["latitude"], data["longitude"], elevation=elevationValue)
		point.speed = data["speed"]
		gpx_segment.points.append(point)

		#print("Longitude:" + data["longitude"])
		#print("Latitude: " +data["latitude"])
		#print("Altitude: " +data["altitude"])
		#print("Speed: " + data["speed"])
		return data
	except socket.error as e:
		err = e.args[0]
		if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
			return msg
		else:
			# a "real" error occurred
			print (e)
			sys.exit(1)
	return data
			


def gamepadStuff():
	gpsData = readFromNav()
	if gpsData:
		print("gpsData", gpsData)
		global gpsSpeed
		gpsSpeed['text'] = "{:.9f}".format(3.6 * gpsData["speed"])
		print(gpsSpeed['text'])
	global chokeIsOn
	if(not chokeIsOn):
		for event in pygame.event.get(): 
			if event.type == pygame.JOYBUTTONDOWN:
				print("Joystick button pressed." , event.dict['button'])
				if(event.dict['button'] == 15):
					print("Starting new GPX file")
					print('Created GPX:', gpx.to_xml())
					timestr = time.strftime("%Y%m%d-%H%M%S")
					with open("gpslog"+ timestr + ".xml", "a") as text_file:
						print(gpx.to_xml(), file=text_file)
						elevationValue = 0
						createGpxTrack()

			if event.type == pygame.JOYBUTTONUP:
				print("Joystick button released.")
			#Brake
			value = ((jStick.get_axis(12) * 100)+ 100) / 2
			scale3.set(int(round(value)))
			value =  375 - (value)*2.25 
			brakeValue(str(+int(round(value))))
			#Speed
			#441 max
			# 150 min
			value = ((jStick.get_axis(13) * 100) +150) / 2
			scale2.set(int(round(value)))
			value =  (value) + 350
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
		toSet = chokeMinValue + randint(15,35)
		scale2.set(toSet)
		sock.sendto(bytes('speed:'+ str((chokeMinValue + toSet) +350),'UTF-8'), server_address)
	root.after(200, gamepadStuff)
	

createGpxTrack()
pygame.init()

padLabel = Label(root, text="Gamepad: " ,fg="black", height=1)
padLabel.grid(row=0,column=1)
caripLabel = Label(root, text="RC-Car-IP: ", fg="black", height=1)
caripLabel.grid(row=1,column=1)
speedLabel = Label(root, text="CurrentSpeed: ", fg="black", height=1)
speedLabel.grid(row=2,column=1)

pad = Label(root, text=gamepadName  ,fg="black", height=1)
pad.grid(row=0,column=2)
carip = Label(root, text=server_address, fg="black", height=1)
carip.grid(row=1,column=2)
gpsSpeed = Label(root, text="not moving", fg="black", height=1)
gpsSpeed.grid(row=2,column=2)


steer = Label(root, text="Steer",  fg="black", height=2)
steer.grid(row=3,column=2)
scale = tkinter.Scale(orient='horizontal', from_=-50, to=50, command=steerValue)
scale.grid(row=4, column=2 )

greenSpeedRectangle = Label(root, text="Speed", bg="green", fg="white", height=2)
greenSpeedRectangle.grid(row=3,column=3)
scale2 = tkinter.Scale(orient='vertical', from_=100, to=0, command=speedValue)
scale2.grid(row=4, column=3)

brake = Label(root, text="Brake", bg="red", fg="white", height=2)
brake.grid(row=3,column=4)
scale3 = tkinter.Scale(orient='vertical', from_=100, to=0, command=brakeValue)
scale3.grid(row=4, column=4)

chokeLabel = Label(root, text="off", fg="black", height=2)
chokeLabel.grid(row=5,column=2)
b = Button(root, text=chokeButtonText ,command=chokeFunc)
b.grid(row=5,column=1)



e1 = Entry(scale)
e2 = Entry(scale2)
e3 = Entry(scale3)


root.after(25, gamepadStuff)
root.mainloop()


