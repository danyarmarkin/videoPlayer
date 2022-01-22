import cv2
import datetime
import tkinter
from UI import interface


def start():
    while True:
        moscow_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
        current_h = int(str(moscow_time).split()[1].split(":")[0])
        current_m = int(str(moscow_time).split()[1].split(":")[1])

        win = tkinter.Tk()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        win.destroy()

        tasks = []
        file = open("settings.txt", "r")
        for line in file.readlines():
            t = line.split()
            if len(t) != 5:
                continue
            from UI import Task
            task = Task(int(t[0]), int(t[1]), int(t[2]), int(t[3]), t[4])
            tasks.append(task)
        file.close()

        cap = cv2.VideoCapture('video1.mp4')

        for task in tasks:
            if task.h_start * 60 + task.m_start <= current_h * 60 + current_m < task.h_stop * 60 + task.m_stop:
                cap = cv2.VideoCapture(task.path)
                break

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
