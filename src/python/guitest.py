import tkinter as tk
from tkinter import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.input_parameters(['Name','Start date'])
        # self.input_parameter()

        self.optional_textblock('Welcome')
        self.optional_textblock('Sign here')

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def input_parameters(self, names, addTo=None):
        if not addTo:
            addTo = self
        frame = tk.Frame(addTo)
        r = 0
        for name in names:
            label = tk.Label(frame, text=name)
            label.grid(row=r,column=0)
            input = tk.Text(frame,height=1)
            input.insert(END, name)
            input.grid(row=r, column=1)
            r +=1
        frame.pack(side="top")

        return frame

    def optional_textblock(self, txt, addTo=None):
        if not addTo:
            addTo = self
        frame = tk.Frame(addTo)
        incl = tk.Checkbutton(frame)
        incl["text"] = "include"
        incl.grid(row=0,column=0)

        incl = tk.Label(frame)
        incl["text"] = txt
        incl.grid(row=0,column=1)
        frame.pack(side="top")

        return frame

root = tk.Tk()
app = Application(master=root)
app.mainloop()