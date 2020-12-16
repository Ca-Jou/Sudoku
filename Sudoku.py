from random import randrange

class Sudoku:

    def __init__(self):
        self.__guess = []
        self.__solution = []
        self.__level = 1

    def newGame(self):
        # generate a sudoku grid
        # at first we load it from a file
        self.__solution.clear()
        self.__guess.clear()

        with open("solucegrille.txt", "r") as file:
            currentLine = file.readline()
            while currentLine != "":
                self.__solution.append(currentLine.split(";")[:-1])
                currentLine = file.readline()

        # generate the corresponding player's grid
        self.__guess = [['X' for i in self.__solution] for j in self.__solution]

        # show randomized numbers in the player's grid -> the bigger the level of difficulty, the less values we show
        n = 0
        if self.__level == 1:
            n = 25
        elif self.__level == 2:
            n = 20
        elif self.__level == 3:
            n = 17  # minimal number of values that have to be shown for the problem to be minimal, according to Gordon Royle (source Wikipedia - Mathematiques du sudoku)

        for count in range(0, n):
            i = randrange(0, len(self.__guess) - 1)
            j = randrange(0, len(self.__guess) - 1)
            self.__guess[i][j] = self.__solution[i][j]

    def __show(self, grid):
        print()
        for line in grid:
            print(' | ', end='')
            for value in line:
                print(str(value), end=' ')
            print('|')

    def guess(self, n, line, column):
        if line in range(1, len(self.__guess) + 1) and column in range(1, len(self.__guess) + 1):
            self.__guess[line - 1][column - 1] = n

    def win(self):
        return self.__guess == self.__solution
