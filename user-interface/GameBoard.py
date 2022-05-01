from os import system, name
from time import sleep


class GameBoard:
    board = []
    p1 = True
    p2 = False
    p1symbol = "X"
    p2symbol = "O"

    def __init__(self):
        self.p = None
        self.board = [[], [], [], [], [], [], []]

        for e in self.board:
            for i in range(0, 7):
                e.append(" ")

    def __str__(self):
        return self.toStr()

    def toStr(self):
        transposed = transpose(self.board)

        currentBoard = ""
        for e in transposed:
            for i in e:
                currentBoard += i + " | "
            currentBoard += "\n"

        return currentBoard

    def startGame(self):
        """

        :return:
        """
        while True:
            x = self.askInput()
            sleep(0.3)
            clear()
            print(x)

    def askInput(self):
        """

        :return:
        """
        try:
            self.p = 1 if self.p1 else 2
            column = input(f"Player {self.p}, enter your move[1-7]:")
            if column == "stop":
                exit()
            column = int(self.check(column))

            result = self.addToken(column)
            return result
        except EOFError as e:
            exit()

    def check(self, column):
        try:
            while True:
                if column in ["1", "2", "3", "4", "5", "6", "7"]:
                    if " " not in self.board[int(column) - 1]:
                        column = input(f"Column is full! Player {self.p}, enter your move[1-7]:")
                        column = self.check(column)
                    break

                column = input(f"Wrong input! Player {self.p}, enter your move[1-7]:")

            return column
        except EOFError as e:
            exit()

    def addToken(self, column):
        """

        :param column:
        :return:
        """
        currentBoard = self.board
        column = column - 1

        for i in range(6, -1, -1):
            if currentBoard[column][i] == " ":
                currentBoard[column][i] = self.p1symbol if self.p1 else self.p2symbol

                self.p1 = not self.p1
                self.p2 = not self.p2
                break

        self.board = currentBoard
        return self.toStr()


def transpose(matrix):
    """

    :param matrix:
    :return:
    """
    rows = len(matrix)
    columns = len(matrix[0])

    matrix_t = []
    for j in range(columns):
        row = []
        for i in range(rows):
            row.append(matrix[i][j])
        matrix_t.append(row)

    return matrix_t


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')
