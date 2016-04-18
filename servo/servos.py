from __future__ import with_statement # Required in 2.5
import socket
import os, os.path
import time
import signal
import sys
from contextlib import contextmanager
from Adafruit_PWM_Servo_Driver import PWM


pwm = PWM(0x40)
#pwm = PWM(0x40, debug=True)
servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

SocketAdr = "/tmp/python_socket.sock"
StopString = "HALT"
TimeOutSeconds = 4

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException()
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

def listen():
    datagram = server.recv( 1024 )
    if not datagram:
        print("strange things happen... better stop")
        return StopString
    return datagram.decode("utf-8")

def actuate(instruction):
    sys.stdout.write("\rInstruction: " + instruction )
    if "speed" in instruction:
        sys.stdout.write("\rSetting speed: "  +instruction[6:] )
        pwm.setPWM(0, 0, int(instruction[6:]))
    sys.stdout.flush()



#Begin main
#Stopping first
pwm = PWM(0x40)
pwm.setPWMFreq(60)  
if os.path.exists( SocketAdr):
	os.remove( SocketAdr )
server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
server.bind(SocketAdr)
 
print("\nListening for first connection")
datagram = server.recv( 1024 )
print("Here we go")
doListen = True;
while doListen:
    instruction = StopString
    try:
        with time_limit(TimeOutSeconds):
            instruction = listen()
    except TimeoutException:
        print ("Close after TimeoutException")
        doListen = False
    actuate(instruction)
#Ending
server.close()
os.remove(SocketAdr)
print ("bye")
