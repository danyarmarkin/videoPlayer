import time
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Separator
import tkinter
import Main


class Task:
    h_start = 0
    m_start = 0
    h_stop = 0
    m_stop = 0

    def __init__(self, h_start, m_start, h_stop, m_stop, path, days):
        self.h_start = h_start
        self.m_start = m_start
        self.h_stop = h_stop
        self.m_stop = m_stop
        self.path = path
        self.days = days

    def __str__(self):
        return f"{self.h_start} {self.m_start} {self.h_stop} {self.m_stop} {self.path}"


class TaskFrame(tkinter.Frame):
    task = None
    start_entry_h = None
    start_entry_m = None
    stop_entry_h = None
    stop_entry_m = None
    days_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    def __init__(self, task: Task, **kw):
        super().__init__(**kw)
        self.task = task

        for j in range(18):
            Separator(self, orient="horizontal").grid(row=0, column=j, sticky="we")

        def dest():
            self.task = None
            self.destroy()

        del_button = tkinter.Button(self, text=" X ", command=dest)
        del_button.grid(row=1, column=0)

        self.start_entry_h = tkinter.Entry(self, width=4)
        self.start_entry_h.insert(tkinter.END, str(self.task.h_start))
        self.start_entry_h.grid(row=1, column=1)

        tkinter.Label(self, text=":").grid(row=1, column=2)

        self.start_entry_m = tkinter.Entry(self, width=4)
        self.start_entry_m.insert(tkinter.END, str(self.task.m_start))
        self.start_entry_m.grid(row=1, column=3)

        tkinter.Label(self, text="to").grid(row=1, column=4, padx=10)

        self.stop_entry_h = tkinter.Entry(self, width=4)
        self.stop_entry_h.insert(tkinter.END, str(self.task.h_stop))
        self.stop_entry_h.grid(row=1, column=5)

        tkinter.Label(self, text=":").grid(row=1, column=6)

        self.stop_entry_m = tkinter.Entry(self, width=4)
        self.stop_entry_m.insert(tkinter.END, str(self.task.m_stop))
        self.stop_entry_m.grid(row=1, column=7)

        file = tkinter.Entry(self, width=50)
        file.insert(tkinter.END, str(self.task.path))
        file.grid(row=1, column=8)

        def change_path():
            path = askopenfilename()
            print(path)
            file.insert(tkinter.END, path)
            self.task.path = path

        browse_button = tkinter.Button(self, text="Browse", command=change_path)
        browse_button.grid(row=1, column=9)

        self.days_checkboxes_var = []
        for i in range(7):
            cb_frame = tkinter.Frame(master=self)
            var = tkinter.IntVar()
            var.set(self.task.days[i])
            cb = tkinter.Checkbutton(cb_frame, text="", variable=var, onvalue=1, offvalue=0)
            cb.grid(row=0, column=0)
            label = tkinter.Label(cb_frame, text=self.days_names[i])
            label.grid(row=1, column=0)
            self.days_checkboxes_var.append(var)
            cb_frame.grid(row=1, column=i + 10)

    def __str__(self):
        return f"{self.start_entry_h.get()} {self.start_entry_m.get()} " + \
               f"{self.stop_entry_h.get()} {self.stop_entry_m.get()} {self.task.path} " \
               + str(list(map(tkinter.IntVar.get, self.days_checkboxes_var))).replace(" ", "")


def interface():
    tasks = []
    frames = []
    root = tkinter.Tk()
    root.geometry("1400x800")
    root.title("Settings")
    f = open("settings.txt", "r")
    for line in f.readlines():
        t = line.split()
        if len(t) != 6:
            continue
        task = Task(int(t[0]), int(t[1]), int(t[2]), int(t[3]), t[4], list(map(int, t[5].replace("[", "").replace("]", "").split(","))))
        tasks.append(task)
    f.close()

    def add_task():
        path = askopenfilename()
        new_task = Task(0, 0, 0, 0, path, [1] * 7)
        tasks.append(new_task)
        new_frame = TaskFrame(new_task, master=root)
        new_frame.grid(row=len(frames) + 1, column=0)
        frames.append(new_frame)

    def save():
        file = open('settings.txt', 'w')
        for current_frame in frames:
            if current_frame.task is None:
                continue
            file.write(str(current_frame))
            file.write('\n')
        file.close()
        save_button["text"] = "Saved!"
        save_button.update()
        time.sleep(3)
        save_button["text"] = "Save"
        save_button.update()

    plus_button = tkinter.Button(root, text="+", width=10, height=3, command=add_task)
    plus_button.grid(row=0, column=0)

    save_button = tkinter.Button(root, text="Save", width=10, height=4, command=save)
    save_button.grid(row=0, column=1)

    def start():
        root.destroy()
        Main.start()

    start_button = tkinter.Button(root, text="Start Video", width=10, height=4, fg='green', command=start)
    start_button.grid(row=0, column=2)

    for i, task in enumerate(tasks):
        frame = TaskFrame(task, master=root)
        frame.grid(row=i + 1, column=0)
        frames.append(frame)

    root.mainloop()
