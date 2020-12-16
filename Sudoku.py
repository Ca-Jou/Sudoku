from random import randrange
import pickle

class Sudoku:

    def __init__(self):
        self.__guess = []
        self.__solution = []
        self.__level = 1

    # setters
    def setGuess(self, grid):
        self.__guess = grid

    def setSolution(self, grid):
        self.__solution = grid

    def setLevel(self, level):
        self.__level = level

    # getters
    def getGuess(self):
        return self.__guess

    def getSolution(self):
        return self.__solution

    def getLevel(self):
        return self.__level

    # methodes metier

    def clearGame(self):
        self.__solution.clear()
        self.__guess.clear()

    def newGame(self):
        # generate a sudoku grid
        # at first we load it from a file
        self.clearGame()

        with open("solucegrille.txt", "r") as file:
            currentLine = file.readline()
            while currentLine != "":
                self.__solution.append(currentLine.split(";")[:-1])
                currentLine = file.readline()

        # generate the corresponding player's grid
        self.setGuess([['X' for i in self.__solution] for j in self.__solution])

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

    def fill(self, n, line, column):
        if line in range(1, len(self.__guess) + 1) and column in range(1, len(self.__guess) + 1):
            self.__guess[line - 1][column - 1] = n

    def win(self):
        return self.getGuess() == self.getSolution()

    def saveGame(self, name):
        gameData = {
            "solution": self.getSolution(),
            "guess": self.getGuess(),
            "level": self.getLevel()
        }
        with open(name, "wb") as file:
            pickler = pickle.Pickler(file)
            pickler.dump(gameData)

    def loadGame(self, name):
        self.clearGame()

        with open(name, "rb") as file:
            unpickler = pickle.Unpickler(file)
            gameData = unpickler.load()

        self.setSolution(gameData["solution"])
        self.setGuess(gameData["guess"])
        self.setLevel(gameData["level"])