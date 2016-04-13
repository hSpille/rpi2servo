import tkinter
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10001)

def speedValue(val):
    print ("Speed:" + val)
    sent = sock.sendto(bytes('Speed:'+val,'UTF-8'), server_address)

def steerValue(val):
    print ("Steer:" +val)
    sent = sock.sendto(bytes('Steer:'+val, 'UTF-8'), server_address)

root = tkinter.Tk()
root.title("control the blind")
root.geometry("350x200+100+50")
scale = tkinter.Scale(orient='horizontal', from_=-50, to=50, command=steerValue)
scale2 = tkinter.Scale(orient='vertical', from_=100, to=0, command=speedValue)

scale.pack()
scale.set(0)
scale2.pack()

root.mainloop()
