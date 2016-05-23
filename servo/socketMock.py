
import socket
import os, os.path
import time
import signal
import sys


SocketAdr = "/tmp/python_socket.sock"

def listen():
    datagram = server.recv( 1024 )
    if not datagram:
        print("strange things happen... better stop")
        return "StopString"
    return datagram.decode("utf-8")



if os.path.exists( SocketAdr):
	os.remove( SocketAdr )
server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
server.bind(SocketAdr)
 
doListen = True;
while doListen:
    instruction = listen()
    print(instruction)
#Ending
server.close()
os.remove(SocketAdr)
print ("bye")
