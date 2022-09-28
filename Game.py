import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

class Minesweeper(tk.Frame):
    element = {"MINE":0, "CLICK":1}
    click = {"LEFT":-1, "NON":0, "RIGHT":1}

    def __init__(self, master):
        super(Minesweeper, self).__init__(master)
        self.width = 360
        self.height = 360
        self.square = 40
        self.canvas = tk.Canvas(self, bg='#a6b1fd',
                                width = self.width,
                                height = self.height)
        self.canvas.pack()
        self.pack()

        self.setup_9x9()
        self.canvas.focus_set()
        self.canvas.bind('<Button-1>', self.left_click)
        self.canvas.bind('<Button-2>', self.right_click)  

    def setup_game(self, row, col):
        # Cheat code
        self.canvas.delete('bomb')

        self.row = row
        self.col = col
        self.width = self.col * self.square
        self.height = self.row * self.square

        self.canvas.config(width = self.width, height = self.height)
        self.canvas.pack()
        self.pack()

        for i in range(self.col+1):
            self.canvas.create_line(i*self.square,0,i*self.square,self.height,fill='black')
        for i in range(self.row+1):
            self.canvas.create_line(0,i*self.square,self.width,i*self.square,fill='black')

        self.pattern = np.zeros(self.col * self.row * 3, dtype = 'int32').reshape(self.col, self.row, 3)

        # Create mine
        for _ in range(self.mine):
            i = random.randint(0, self.col-1)
            j = random.randint(0, self.row-1)
            while self.pattern[i][j][Minesweeper.element["MINE"]] == -1:       
                i = random.randint(0, self.col-1)
                j = random.randint(0, self.row-1)
            
            self.pattern[i][j][Minesweeper.element["MINE"]] = -1  
            # Cheat code
            self.canvas.create_text((i+0.5)*self.square, (j+0.5)*self.square, text = 'O', fill = 'black', font = ('Helvetica', 40), tags = 'bomb')
    
    def setup_9x9(self):
        self.mine = 10
        self.setup_game(9, 9)

    def setup_16x16(self):
        self.mine = 40
        self.setup_game(16, 16)

    def setup_30x16(self):
        self.mine = 99
        self.setup_game(16, 30)

    def left_click(self, event):
        x = event.x//self.square
        y = event.y//self.square
        if self.pattern[x][y][Minesweeper.element["MINE"]] == -1:
            messagebox.showinfo('BOMB', 'BOMB!')
            self.setup_game(self.row, self.col)
        else:
            self.detect_region(x, y)                

    def right_click(self, event):  
        x = event.x//self.square
        y = event.y//self.square
        if self.pattern[x][y][Minesweeper.element["CLICK"]] == Minesweeper.click["NON"]:
            self.canvas.create_text((x+0.5)*self.square, (y+0.5)*self.square, text = 'X', fill = 'red', font = ('Helvetica', 40), tags = '[{},{}]'.format(x,y))
            self.pattern[x][y][Minesweeper.element["CLICK"]] = Minesweeper.click["RIGHT"]
        elif self.pattern[x][y][Minesweeper.element["CLICK"]] == Minesweeper.click["RIGHT"]:
            self.canvas.delete('[{},{}]'.format(x,y))
            self.pattern[x][y][Minesweeper.element["CLICK"]] = Minesweeper.click["NON"]
        
    def detect_region(self, x, y):
        pass
        
            


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