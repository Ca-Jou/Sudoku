from Interface import *
from Sudoku import *
from tkinter import *

window = Tk()
window.title("Sudoku des personnes agées.")
sudoku = Sudoku()
interface = Interface(window, sudoku)

window.mainloop()

# TODO tester la win

window.destroy()
