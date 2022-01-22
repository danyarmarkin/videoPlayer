import cv2
import datetime
from UI import *


def start():
    while True:
        moscow_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
        current_time = int(str(moscow_time).split()[1].split(":")[0])

        win = tkinter.Tk()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        cap = cv2.VideoCapture('video1.mp4')

        if 9 <= current_time < 14:
            cap = cv2.VideoCapture("video2.mp4")
        if 14 <= current_time < 17:
            cap = cv2.VideoCapture("video3.mp4")
        if 17 <= current_time < 23:
            cap = cv2.VideoCapture("video4.mp4")

        if not cap.isOpened():
            print("Error opening video  file")

        stop = False
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                sized_frame = cv2.resize(frame, (screen_width, screen_height))
                cv2.imshow('window', sized_frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    stop = True
                    break
            else:
                break
        cap.release()
        if stop:
            break

    print("interface")
    cv2.destroyWindow("window")
    cv2.destroyAllWindows()
    interface()


if __name__ == "__main__":
    start()
