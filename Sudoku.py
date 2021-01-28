from random import randrange
import pickle

# TODO:
# - generer les grilles de facon aleatoire

class Sudoku:

    def __init__(self):
        self.__guess = []
        self.__solution = []
        self.__level = 1
        self.__size = 9
        self.__initNb = []

    # setters
    def setGuess(self, grid):
        self.__guess = grid

    def setSolution(self, grid):
        self.__solution = grid

    def setLevel(self, level):
        self.__level = level

    def setSize(self, n):
        self.__size = n

    def setInitNb(self, grid):
        self.__initNb = grid

    # getters
    def getGuess(self):
        return self.__guess

    def getSolution(self):
        return self.__solution

    def getLevel(self):
        return self.__level

    def getSize(self):
        return self.__size

    def getInitNb(self):
        return self.__initNb

    # methodes metier

    def clearGame(self):
        self.__solution.clear()
        self.__guess.clear()
        self.__initNb.clear()

    def newGame(self, name):
        # generate a sudoku grid
        # at first we load it from a file
        self.clearGame()

        with open(name, "r") as file:
            currentLine = file.readline()
            while currentLine != "":
                self.__solution.append(currentLine.split(";")[:-1])
                currentLine = file.readline()

        for i in range(0, len(self.__solution)):
            for j in range(0, len(self.__solution)):
                self.__solution[i][j] = int(self.__solution[i][j])

        # set the corresponding size
        self.__size = len(self.__solution)

        # generate the corresponding player's grid
        self.setGuess([['' for i in self.__solution] for j in self.__solution])
        self.setInitNb([[False for i in self.__solution] for j in self.__solution])

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
            self.__initNb[i][j] = True

    def fill(self, n, i, j):
        if i in range(0, len(self.__guess)) and j in range(0, len(self.__guess[i])):
            self.__guess[i][j] = n

    def win(self):
        return self.getGuess() == self.getSolution()

    def saveGame(self, name):
        gameData = {
            "solution": self.getSolution(),
            "initnb": self.getInitNb(),
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
        self.setInitNb(gameData["initnb"])
        self.setGuess(gameData["guess"])
        self.setLevel(gameData["level"])

    def check(self):
        ok = [[False for i in self.__solution] for j in self.__solution]
        for i in range(0, len(ok)):
            for j in range(0, len(ok[i])):
                if self.__guess[i][j] == '':
                    continue
                else:
                    ok[i][j] = (self.__guess[i][j] == self.__solution[i][j])
        return ok
