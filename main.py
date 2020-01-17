import tkinter
import cv2 #pip install opencv-python
import PIL.Image, PIL.ImageTk #pip install pillow
from functools import partial
import threading
import imutils
from PIL import Image
from PIL import ImageTk
import time

stream = cv2.VideoCapture("video.mp4")
def play(speed):
    print(f"You clicked on play. Speed is {speed}")
    #for frame + speed
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    
    grabbed, frame = stream.read()
    frame =imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image= Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW) 
    canvas.create_text(135,27, fill="red", font="times 25 bold", text="Decision Pending")
         

def pending(decision):
    # 1.Display decision pending image
    frame = cv2.cvtColor(cv2.imread("decision_pending.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # 2. wait for 1 second
    time.sleep(1)
    # 3. Display sponsor image
    frame = cv2.cvtColor(cv2.imread("advertise.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    # 4. wait for 1.5 second
    time.sleep(11.5)
    # 5. Display out/not out image
    if decision == 'out':
        decisionImg = 'out.jpg'
    else:
        decisionImg = 'not_out.jpg'  

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

# Width and height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 368

# Tkinter gui starts here
window = tkinter.Tk()
window.title("Third Umpire Decision Review Kit")
cv_img= cv2.cvtColor(cv2.imread("welcome.jpg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()



# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()
window.mainloop()