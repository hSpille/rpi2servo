
import socket
import os, os.path
import time
import signal
import sys

jsonDataString = '{"ax": 0.029296875, "ay": 0.1015625, "az": 1.01708984375, "gx": -1, "gy": 1, "gz": -1} \n'
guiSocketAdr = "/tmp/python_socket.sock"
gyroSocketAdr = "/tmp/gyro_socket.sock"

def listenGui():
	datagram = guiServer.recv( 1024 )
	if not datagram:
		return "StopString"
	return datagram.decode("utf-8")


if os.path.exists( guiSocketAdr):
	os.remove( guiSocketAdr )
guiServer = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
guiServer.bind(guiSocketAdr)

#SocketGyro
if os.path.exists( gyroSocketAdr):
	os.remove( gyroSocketAdr )
gyroSocket = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
gyroSocket.bind(gyroSocketAdr)
 
gyroSocket.listen(1)
while 1:
	try:
		conn, addr = gyroSocket.accept()
		data = conn.recv(1024)
		doListen = True;
		print("GYRO: incoming connection: " )
		while doListen:
			instructionGui = listenGui()
			conn.send( str(jsonDataString).encode())
			print("SocketMock receives: " + instructionGui)
		#Ending
	except IOError as e:
		print("connection lost or TIFU")


