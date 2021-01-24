from tkinter import *

# TODO:
# - bouton nouvelle partie
# - bouton enregistrer
# - bouton verifier la grille
# - boutton quitter


class Interface(Frame):

    def __init__(self, window, sudoku):
        Frame.__init__(self, window, width=900, height=900)
        self.pack()

        # Canvas

        self.canvas = Canvas(self, bg='white', width=490, height=490)
        self.canvas.pack(expand=False, side='bottom')
        self.drawGrid()
        self.canvas.bind("<Button-1>", self.clicGrid)

        # Widgets

        self.entry = Entry(window, bg='grey')
        self.entry.bind("<Return>", self.fillGrid)

        self.text_widget = Text(window)

        # Sudoku game
        self.sudoku = sudoku

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

        # TODO on donne les cooordonnees du clic au champ de saisie de texte
        # self.entry.x = x_clic
        # self.entry.y = y_clic

        self.entry.pack()

    def fillGrid(self, event):
        #retrieve the user entry
        userNb = self.entry.get()
        maxNb = self.sudoku.getSize()

        try:
            userNb = int(userNb)
            if (userNb > maxNb):
                raise ValueError()
        except ValueError:
            self.text_widget.delete(0)
            self.text_widget.insert(END, "Please enter an integer between 1 and {}.".format(maxNb), foreground="red")
            self.text_widget.pack()
            userNb = self.entry.get()

        # retrieve the coordinates of the entry field (upper left corner), and deduce the line and column modified in the Sudoku guess matrix
        x_entry = self.entry.winfo_x()
        y_entry = self.entry.winfo_y()
        line = (x_entry - 20) / 50
        column = (y_entry - 20) / 50

        # save the user entry in their Sudoku matrix
        self.sudoku.fill(userNb, line, column)
