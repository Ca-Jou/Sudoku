from tkinter import *


class Interface(Frame):

    def __init__(self, window):
        Frame.__init__(self, window, width=900, height=900)
        self.pack()

        # Canvas

        self.canvas = Canvas(self, bg='white', width=490, height=490)
        self.canvas.pack(expand=False, side='bottom')
        self.drawGrid()

    def drawGrid(self):
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
