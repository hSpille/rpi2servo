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
steerChannel = 4
speedChannel = 0



def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)



#Begin main
#Stopping first
pwm = PWM(0x40)
pwm.setPWMFreq(60)  
 


print("Here we go")
while True:
    pwm.setPWM(steerChannel, 0, servoMin)
    time.sleep(2)
    pwm.setPWM(steerChannel, 0, servoMax)
    time.sleep(2)
    

#Ending
server.close()
os.remove(SocketAdr)
print ("bye")
