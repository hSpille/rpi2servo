import tkinter

def speedValue(val):
    print ("Speed:" + val)

def steerValue(val):
    print ("Steer:" +val)

root = tkinter.Tk()
root.title("control the blind")
root.geometry("350x200+100+50")
scale = tkinter.Scale(orient='horizontal', from_=-50, to=50, command=steerValue)
scale2 = tkinter.Scale(orient='vertical', from_=100, to=0, command=speedValue)

scale.pack()
scale.set(0)
scale2.pack()

root.mainloop()