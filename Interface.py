from tkinter import *
import tkinter.font as tkfont
from PIL import (Image, ImageTk)
from datetime import datetime
import tkinter.filedialog

from Sudoku import *


class Interface(Frame):

    def __init__(self, window):
        self.__inGame = False

        # Sudoku game
        self.sudoku = Sudoku()

        Frame.__init__(self, window, width=1600, height=1600)
        self.pack()

        # Canvas
        self.canvas = Canvas(self, bg='white', width=500, height=500, highlightthickness=0, bd=0, relief='ridge')
        self.canvas.pack(expand=False, side='left')

        # Wonderful welcoming background
        unicorn = Image.open("0-Files/kawaii_unicorn.jpg").resize((500, 500), Image.ANTIALIAS)
        bgImage = ImageTk.PhotoImage(unicorn)
        self.canvas.image = bgImage
        self.canvas.create_image(0, 0, image=bgImage, anchor=NW)

        # Widgets
        self.numbers = []
        self.hints = []

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

    def hydrate(self):
        # this method is used to hydrate GUI attributes that depend on the sudoku size
        # - and thus on the choice of grid size made by the user AFTER initiating the GUI
        # Canvas
        self.canvas.configure(width=40+50*self.sudoku.getSize(), height=40+50*self.sudoku.getSize())

        # Number entries
        self.numbers = [[] for i in range(0, self.sudoku.getSize())]
        for i in range(0, self.sudoku.getSize()):
            for j in range(0, self.sudoku.getSize()):
                self.numbers[i].append(Entry(self.canvas, background='white', foreground='black',
                                             font=tkfont.Font(family='Arial', size=25), highlightthickness=0,
                                             borderwidth=0, justify='center', cursor='heart'))
                self.numbers[i][j].bind('<Button-1>', self.selectNb)
                self.numbers[i][j].bind('<Return>', self.fillGrid)
                self.numbers[i][j].bind('<FocusOut>', self.fillGrid)

        # Hints entries
        self.hints = [[] for i in range(0, self.sudoku.getSize())]
        for i in range(0, self.sudoku.getSize()):
            for j in range(0, self.sudoku.getSize()):
                self.hints[i].append(Entry(self.canvas, background='white', foreground='snow4',
                                           font=tkfont.Font(family='Arial', size=10), highlightthickness=0,
                                           borderwidth=0, justify='left', cursor='pencil'))

    def drawGrid(self):
        color = ""
        width = 1
        for i in range(0, self.sudoku.getSize()+1):
            if self.sudoku.getSize() == 9:
                color = "black" if i % 3 == 0 else "gray"
                width = 2 if i % 3 == 0 else 1
            elif self.sudoku.getSize() == 16:
                color = "black" if i % 4 == 0 else "gray"
                width = 2 if i % 4 == 0 else 1

            x0 = 20 + i * 50
            y0 = 20
            x1 = 20 + i * 50
            y1 = 20 + 50 * self.sudoku.getSize()
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

            x0 = 20
            y0 = 20 + i * 50
            x1 = 20 + 50 * self.sudoku.getSize()
            y1 = 20 + i * 50
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    def newGame(self):
        self.text_widget.pack_forget()
        src_path = tkinter.filedialog.askopenfilename()
        self.sudoku.newGame(src_path)
        self.__inGame = True
        self.hydrate()
        self.showGuessedNumbers()

    def loadGame(self):
        self.text_widget.pack_forget()
        src_path = tkinter.filedialog.askopenfilename()
        self.sudoku.loadGame(src_path)
        self.__inGame = True
        self.hydrate()
        self.showGuessedNumbers()

    def saveGame(self):
        fileName = tkinter.filedialog.asksaveasfilename(defaultextension='.txt')
        self.sudoku.saveGame(fileName)
        self.text_widget["text"] = "Votre partie a ete sauvegardee dans le fichier " + fileName
        self.text_widget.pack()

    def showGuessedNumbers(self):
        # clear the canvas
        self.canvas.delete(ALL)

        #  redraw the grid
        self.drawGrid()

        # draw the numbers of the Sudoku.guessed matrix on the canvas
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
                self.numbers[i][j].place(x=x_nb+5, y=y_nb+5, width=40, height=40)
                j += 1
            j = 0
            i += 1

        # hints
        for i in range(0, self.sudoku.getSize()):
            for j in range(0, self.sudoku.getSize()):
                self.hints[i][j].place(x=25+i*50, y=21+j*50, width=40, height=10)

    def selectNb(self, event):
        event.widget.delete(0, 'end')
        event.widget.configure(fg='black')

    def fillGrid(self, event):
        # retrieve the user entry
        j = int((event.widget.winfo_x() - 25) / 50)
        i = int((event.widget.winfo_y() - 25) / 50)
        newNb = str(event.widget.get())
        oldNb = self.sudoku.getGuess()[i][j]

        try:
            if not self.sudoku.isValid(newNb):
                raise ValueError()
            self.sudoku.fill(newNb, i, j)
            self.numbers[i][j].configure(fg='black')
            self.canvas.focus_set()
        except ValueError:
            event.widget.delete(0, 'end')
            event.widget.insert(0, oldNb)
            self.canvas.focus_set()

    def checkGrid(self):
        if self.__inGame:
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
