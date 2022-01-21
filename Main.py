import cv2
import numpy as np
import tkinter

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video.mp4')

win = tkinter.Tk()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

if not cap.isOpened():
    print("Error opening video  file")

while cap.isOpened():

    ret, frame = cap.read()
    if ret:

        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        sized_frame = cv2.resize(frame, (screen_width, screen_height))
        cv2.imshow('window', sized_frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()