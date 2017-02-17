# Nitro Racer driven by Raspberry pi

Yes. It is code for a Raspberry Pi driving a nitro engine powered RC car using GPS and a 9DOF to navigate. Kind of. 

Actually this is my try to build an autonomous car based on an RC car. But everybody does this using electric toy cars. So i tried it using a nitro engine. Which doesn't make it much easier.
But, it's kind of more fun when your pi reaches 70km/h without seeing anything in front of it. Well, grab your gamepad and make it stop - uhm... too late, crashed.  :)

# Software
## golang navgo.go 
This is the all connecting heart. It reads GPS, GYRO and inputs from the Gamepad (controlgui) and sends commands to the python servo.py which does talk to the servos. It runs direkt on the pi, opens a udp-socket
for the control gui. If the gui disconnects - this whole thing is based on WLAN connection between your laptop and the pi - it 
notices after a short time and stops the car. Usually you lose wireless connection cause the car went to far. It also has a command
priority - human controlled gamepad first to be safe. Always remember, this thing does 70km/h so it really can hurt someone. 

## python /servo/servos.py
Opens a socket and wait's for commands to forward to the servos. Code is based on adafruid servo-hat: https://www.adafruit.com/product/2327
Only logic here is - if there's no command for a time it stops the car. Maybe the other processes crashed. 

## Mocks
All files named something with Mock usually open a port or do some other stuff to make developing easier. You don't always want 
to start the car or power up servos, get GPS signal and so on.

## GPS 
based on linux gpsd: https://wiki.ubuntuusers.de/gpsd/

#Hardware

###### RC Car
is a LRP S8BX http://www.lrp.cc/de/produkt/lrp-s8-bx-rtr-18-nitro-buggy-rtr-1/ 
![Alt text](/IMG_20160422_221632.jpg?raw=true "TheCar")
###### Raspberry 
PI B. Default. What do i say? 
###### Servos
Adafruid Servo hat: https://www.adafruit.com/product/2327
###### GPS
Ublox NEO 6M GPS Modul Aircraft Flight Controller https://www.amazon.de/dp/B00S4RLICU/ref=cm_sw_r_tw_dp_x_dk2Pyb7SNS70C
![Alt text](/frame-024.jpg?raw=true "TheCar")


###### Gyro
MPU 9250 code based on  https://github.com/micropython-IMU/micropython-mpu9x50 and http://blog.bitify.co.uk/2013/11/using-complementary-filter-to-combine.html
