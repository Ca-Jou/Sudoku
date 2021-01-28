from tkinter import *
import tkinter.font as tkfont
from PIL import (Image, ImageTk)
from datetime import datetime
import tkinter.filedialog

from Sudoku import *


class Interface(Frame):

    def __init__(self, window):
        # Sudoku game
        self.sudoku = Sudoku()

        Frame.__init__(self, window, width=900, height=900)
        self.pack()

        # Canvas
        self.canvas = Canvas(self, bg='white', width=490, height=490)
        self.canvas.pack(expand=False, side='left')

        # Widgets
        self.numbers = [[] for i in range(0, 9)]
        for i in range(0, 9):
            for j in range(0, 9):
                self.numbers[i].append(Entry(self.canvas, background='white', foreground='black', font=tkfont.Font(family='Arial', size=25), highlightthickness=0, justify='center', cursor='heart'))
                self.numbers[i][j].bind('<Button-1>', self.selectNb)
                self.numbers[i][j].bind('<Return>', self.fillGrid)
        self.drawGrid()

        self.new_button = Button(self, text="New game", width=15, command=self.newGame)
        self.new_button.pack()

        self.load_button = Button(self, text="Load game", width=15, command=self.loadGame)
        self.load_button.pack()

        self.check_button = Button(self, text="Check grid", width=15, command=self.checkGrid)
        self.check_button.pack()

        self.quit_button = Button(self, text="Quit", width=15, command=self.quit)
        self.quit_button.pack(side='bottom')

        self.load_button = Button(self, text="Save game", width=15, command=self.saveGame)
        self.load_button.pack(side='bottom')

        self.text_widget = Label(window)

    def drawGrid(self):
        # wonderful background
        unicorn = Image.open("0-Files/kawaii_unicorn.jpg").resize((490, 490), Image.ANTIALIAS)
        bgImage = ImageTk.PhotoImage(unicorn)
        self.canvas.image = bgImage
        self.canvas.create_image(0, 0, image=bgImage, anchor=NW)

        # grid
        for i in range(10):
            color = "black" if i % 3 == 0 else "gray"

            x0 = 20 + i * 50
            y0 = 20
            x1 = 20 + i * 50
            y1 = 490 - 20
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = 20
            y0 = 20 + i * 50
            x1 = 490 - 20
            y1 = 20 + i * 50
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def newGame(self):
        self.text_widget.pack_forget()
        src_path = tkinter.filedialog.askopenfilename()
        self.sudoku.newGame(src_path)
        self.showGuessedNumbers()

    def loadGame(self):
        self.text_widget.pack_forget()
        src_path = tkinter.filedialog.askopenfilename()
        self.sudoku.loadGame(src_path)
        self.showGuessedNumbers()

    def saveGame(self):
        fileName = tkinter.filedialog.asksaveasfilename(defaultextension='.txt')
        self.sudoku.saveGame(fileName)
        self.text_widget["text"] = "Votre partie a ete sauvegardee dans le fichier " + fileName
        self.text_widget.pack()

    def showGuessedNumbers(self):

        # clear the canvas
        self.canvas.delete(ALL)

        # draw the numbers of the Sudoku.guessed matrix on the canvas
        # TODO trouver un moyen de degager la bordure!!!
        i, j = 0, 0
        for line in self.sudoku.getGuess():
            for number in line:
                x_nb = 20 + j * 50
                y_nb = 20 + i * 50
                self.numbers[i][j].delete(0, 'end')
                if self.sudoku.getInitNb()[i][j]:
                    self.numbers[i][j].configure(fg='deep sky blue')
                else:
                    self.numbers[i][j].configure(fg='black')
                self.numbers[i][j].insert('end', number)
                self.numbers[i][j].place(x=x_nb, y=y_nb, width=50, height=50)
                j += 1
            j = 0
            i += 1

        #  redraw the grid
        self.drawGrid()

    def selectNb(self, event):
        event.widget.delete(0, 'end')

    def fillGrid(self, event):
        # retrieve the user entry
        newNb = event.widget.get()
        maxNb = self.sudoku.getSize()

        j = int((event.widget.winfo_x() - 20) / 50)
        i = int((event.widget.winfo_y() - 20) / 50)

        oldNb = self.sudoku.getGuess()[i][j]

        try:
            newNb = int(newNb)
            if (newNb > maxNb):
                raise ValueError()
            self.sudoku.fill(newNb, i, j)
            self.numbers[i][j].configure(fg='black')
            self.canvas.focus_set()
        except ValueError:
            event.widget.delete(0, 'end')
            event.widget.insert(0, oldNb)
            self.canvas.focus_set()

    def checkGrid(self):
        ok = self.sudoku.check()
        for i in range(0, len(ok)):
            for j in range(0, len(ok[i])):
                if self.sudoku.getInitNb()[i][j]:
                    continue
                elif ok[i][j]:
                    self.numbers[i][j].configure(fg="seagreen3")
                else:
                    self.numbers[i][j].configure(fg="brown1")
        if self.sudoku.win():
            self.text_widget["text"] = "Good job B*tch !"
            self.text_widget.pack()
