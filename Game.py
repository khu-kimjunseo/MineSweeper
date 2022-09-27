import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper(tk.Frame):
    def __init__(self, master):
        super(Minesweeper, self).__init__(master)
        self.width = 360
        self.height = 360
        self.canvas = tk.Canvas(self, bg='#a6b1fd',
                                width = self.width,
                                height = self.height)
        self.canvas.pack()
        self.pack()

        self.setup_9x9()
        self.canvas.focus_set()
        self.canvas.bind('<Button-1>', self.left_click)
        self.canvas.bind('<Button-2>', self.right_click)  

    def setup_9x9(self):
        self.width = 360
        self.height = 360
        self.canvas.config(width = self.width,
                            height = self.height)
        self.canvas.pack()
        self.pack()
        
        for i in range(10):
            self.canvas.create_line(i*40,0,i*40,360,fill='black')
            self.canvas.create_line(0,i*40,360,i*40,fill='black')
          

    def setup_16x16(self):
        self.width = 640
        self.height = 640
        self.canvas.config(width = self.width,
                            height = self.height)
        self.canvas.pack()
        self.pack()
        
        for i in range(17):
            self.canvas.create_line(i*40,0,i*40,640,fill='black')
            self.canvas.create_line(0,i*40,640,i*40,fill='black')
        
    def setup_30x16(self):
        self.canvas.delete("all")
        self.width = 1200
        self.height = 640
        self.canvas.config(width = self.width,
                            height = self.height)
        self.canvas.pack()
        self.pack()
        
        for i in range(31):
            self.canvas.create_line(i*40,0,i*40,640,fill='black')
        for i in range(17):
            self.canvas.create_line(0,i*40,1200,i*40,fill='black')


    def left_click(self, event):
        x = event.x
        y = event.y
    def right_click(self, event):  
        x = event.x
        y = event.y


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Hello, Mine!')

    game = Minesweeper(root)

    menubar = tk.Menu(root)
    filemenu=tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="9*9", command = game.setup_9x9)
    filemenu.add_command(label="16*16", command = game.setup_16x16)
    filemenu.add_command(label="30*16", command = game.setup_30x16)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command = root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    game.mainloop()