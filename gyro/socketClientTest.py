import socket
import os
import time
# import os, os.path

print("Connecting...")
if os.path.exists("/tmp/gyro_socket.sock"):
	client = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
	client.connect("/tmp/gyro_socket.sock")
	try:
		print("waiting for data")
		while True:
			data = client.recv(1024)
			print(data)
			time.sleep(2)
	finally:
		print("closing test socket")
		client.close()
