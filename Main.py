import cv2
import datetime
import tkinter


def isVideo(task, d, h, m):
    sh = task.h_start
    sm = task.m_start
    fh = task.h_stop
    fm = task.m_stop
    wd = task.days

    # print(sh, sm, fh, fm, h, m, d, wd)

    if sh * 60 + sm <= h * 60 + m < fh * 60 + fm and wd[d] == 1:
        return True

    if sh * 60 + sm <= h * 60 + m and fh * 60 + fm == 0 and wd[d] == 1:
        return True

    if ((sh * 60 + sm <= h * 60 + m) or (h * 60 + m < fh * 60 + fm)) and (wd[d] == 1 or wd[(d - 1) % 7] == 1) and (
            sh * 60 + sm >= fh * 60 + fm):
        return True

    return False


def start():
    while True:
        moscow_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
        weekday = moscow_time.weekday()
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
            if len(t) != 6:
                continue
            from UI import Task
            task = Task(int(t[0]), int(t[1]), int(t[2]), int(t[3]), t[4], list(map(int, t[5].replace("[", "").replace("]", "").split(","))))
            tasks.append(task)
        file.close()

        cap = cv2.VideoCapture('black.mp4')
        for task in tasks:
            if isVideo(task, weekday, current_h, current_m):
                cap = cv2.VideoCapture(task.path)
                break

        if not cap.isOpened():
            print("Error opening video  file")

        stop = False
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
                # cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.namedWindow("window")
                cv2.resizeWindow("window", screen_width, screen_height)
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
    from UI import interface
    interface()


if __name__ == "__main__":
    start()
