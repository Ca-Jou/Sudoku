from tkinter import *


class Interface(Frame):

    def __init__(self, window):
        Frame.__init__(self, window, width=900, height=900)
        self.pack()

        # Canvas

        self.canvas = Canvas(self, bg='white', width=490, height=490)
        self.canvas.pack(expand=False, side='bottom')
        self.drawGrid()
        self.canvas.bind("<Button-1>", self.clicGrille)

        # Widgets

        self.entry = Entry(window, bg='grey')

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

    def clicGrid(self, event):
        x_clic = event.x
        y_clic = event.y

        # TODO ici on teste les coordonnees du clic et on voit dans quelle case l'user a clique -> ca nous donne les coordonnees de la case de la matrice qu'on doit modifier
        # x_case = ??
        # y_case = ??

        # TODO on donne les cooordonnees du clic au champ de saisie de texte
        # self.entry.x = x_clic
        # self.entry.y = y_clic

        self.entry.pack()

    def fillGrid(self, event):
        # TODO on enregistre dans Sudoku.guess la saisie du user
        pass
