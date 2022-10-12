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
        
    def setup_game(self, col, row):
        self.canvas.delete('all')

        self.col = col
        self.row = row
        self.width = self.col * self.square
        self.height = self.row * self.square

        self.canvas.config(width = self.width, height = self.height)
        self.canvas.pack()
        self.pack()

        for i in range(self.col+1):
            self.canvas.create_line(i*self.square,0,i*self.square,self.height,fill='black')
        for i in range(self.row+1):
            self.canvas.create_line(0,i*self.square,self.width,i*self.square,fill='black')

        self.pattern = np.zeros(self.col * self.row * 2, dtype = 'int32').reshape(self.col, self.row, 2)


        # Create mine
        for _ in range(self.mine):
            i = random.randint(0, self.col-1)
            j = random.randint(0, self.row-1)
            while self.pattern[i][j][Minesweeper.element["MINE"]] == -1:       
                i = random.randint(0, self.col-1)
                j = random.randint(0, self.row-1)
            self.pattern[i][j][Minesweeper.element["MINE"]] = -1  
            # Cheat code
            # self.canvas.create_text((i+0.5)*self.square, (j+0.5)*self.square, text = 'O', fill = 'green', font = ('Helvetica', 40), tags = 'bomb')
        
        for i in range(self.col):
            for j in range(self.row):
                if self.pattern[i][j][Minesweeper.element["MINE"]] == -1: continue
                count = 0
                for xx in range(-1, 2):
                    if i+xx < 0 or i+xx >= self.col: continue    
                    for yy in range(-1, 2):
                        if j+yy < 0 or j+yy >= self.row: continue
                        if self.pattern[i+xx][j+yy][Minesweeper.element["MINE"]] == -1:
                            count += 1
                self.pattern[i][j][Minesweeper.element["MINE"]] = count

    def setup_9x9(self):
        self.mine = 10
        self.canvas.bind('<Button-1>', self.left_click)
        self.canvas.bind('<Button-2>', self.right_click)  
        self.setup_game(9, 9)

    def setup_16x16(self):
        self.mine = 40
        self.canvas.bind('<Button-1>', self.left_click)
        self.canvas.bind('<Button-2>', self.right_click)  
        self.setup_game(16, 16)

    def setup_30x16(self):
        self.mine = 99
        self.canvas.bind('<Button-1>', self.left_click)
        self.canvas.bind('<Button-2>', self.right_click)  
        self.setup_game(30, 16)
     
    def check_win(self):
        bIsWin = True
        for i in range(self.col):
            if bIsWin == True:
                for j in range(self.row):
                    if self.pattern[i][j][Minesweeper.element["CLICK"]] == Minesweeper.click["NON"]:
                        bIsWin = False
                        break
                    if self.pattern[i][j][Minesweeper.element["MINE"]] == -1:
                        if self.pattern[i][j][Minesweeper.element["CLICK"]] != Minesweeper.click["RIGHT"]:
                            bIsWin = False
                            break
                    else:
                        if self.pattern[i][j][Minesweeper.element["CLICK"]] == Minesweeper.click["RIGHT"]:
                            bIsWin = False
                            break
            else:
                break
        if bIsWin is True:
            self.canvas.unbind('<Button-1>')
            self.canvas.unbind('<Button-2>')  
            messagebox.showinfo('WIN', ' YOU WIN!')

    def left_click(self, event):
        x = event.x//self.square
        y = event.y//self.square
        if self.pattern[x][y][Minesweeper.element["MINE"]] == -1:
            messagebox.showinfo('BOMB', 'BOMB!')
            self.setup_game(self.col, self.row)
        else:
            self.detect_region(x, y)
        self.check_win()
        

    def right_click(self, event):  
        x = event.x//self.square
        y = event.y//self.square
        if self.pattern[x][y][Minesweeper.element["CLICK"]] == Minesweeper.click["NON"]:
            self.canvas.create_text((x+0.5)*self.square, (y+0.5)*self.square, text = 'X', fill = 'red', font = ('Helvetica', 40), tags = '[{},{}]'.format(x,y))
            self.pattern[x][y][Minesweeper.element["CLICK"]] = Minesweeper.click["RIGHT"]
        elif self.pattern[x][y][Minesweeper.element["CLICK"]] == Minesweeper.click["RIGHT"]:
            self.canvas.delete('[{},{}]'.format(x,y))
            self.pattern[x][y][Minesweeper.element["CLICK"]] = Minesweeper.click["NON"]
        self.check_win()
        
    def detect_region(self, x, y):
        self.canvas.create_text((x+0.5)*self.square, (y+0.5)*self.square, text = str(self.pattern[x][y][Minesweeper.element["MINE"]]), fill = 'black', font = ('Helvetica', 40))
        if self.pattern[x][y][Minesweeper.element["CLICK"]] == Minesweeper.click["RIGHT"]:
            self.canvas.delete('[{},{}]'.format(x,y))
        self.pattern[x][y][Minesweeper.element["CLICK"]] = Minesweeper.click["LEFT"]
        if self.pattern[x][y][Minesweeper.element["MINE"]] == 0:
                for xx in range(-1, 2):
                    if x+xx < 0 or x+xx >= self.col: continue
                    for yy in range(-1, 2):
                        if y+yy < 0 or y+yy >= self.row: continue
                        if self.pattern[x+xx][y+yy][Minesweeper.element["CLICK"]] == Minesweeper.click["LEFT"]: continue
                        self.detect_region(x+xx, y+yy)
                


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
