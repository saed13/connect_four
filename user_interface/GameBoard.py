from os import system, name, environ

from dotenv import load_dotenv
import redis as redis
load_dotenv()
REDIS_KEY = environ.get('REDIS_KEY')

r = redis.Redis(host='connect-four.redis.cache.windows.net', port=6380, db=0, password=REDIS_KEY, ssl=True)
#r = redis.Redis(host='http://172.17.0.3')
r.set("second", "test")
#print(r.get("test"))


class GameBoard:
    board = []
    p1 = True
    p2 = False
    p1symbol = "X"
    p2symbol = "O"

    def __init__(self):
        self.winner = None
        self.p = None
        self.board = self.defineBoard([[], [], [], [], [], [], []])

    def __str__(self):
        return self.toStr()

    @staticmethod
    def defineBoard(array):
        """

        :param array:
        :return:
        """
        for e in array:
            for i in range(0, 6):
                e.append(" ")
        return array

    def toStr(self):
        """

        :return:
        """
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
        noWinner = True
        stop = False

    def getInput(self, pos):
        """
        :param: pos
        :return:
        """
        try:
            self.p = 1 if self.p1 else 2
            if pos == "stop":
                exit()

            column = int(pos / 100 - 0.05)
            column = int(self.check(column))
            if column == -1:
                return -1

            return column
        except EOFError as e:
            exit()

    def check(self, column):
        """

        :param column:
        :return:
        """
        try:
            while True:
                if column in range(0, 7):
                    if " " not in self.board[int(column)]:
                        return -1
                    return column
                else:
                    return -1

        except EOFError as e:
            exit()

    def addToken(self, col):
        """

        :param col:
        :return:
        """
        row = self.board[col].index(' ')

        place = (col, row)

        if self.p1:
            self.board[col][row] = "p1"
        else:
            self.board[col][row] = "p2"

        winner = self.checkWinner()

        self.p1 = not self.p1
        self.p2 = not self.p2

        return winner, place, not self.p1, self.winner

    def checkWinner(self):
        """

        :return:
        """
        horizontal = self.checkShape(transpose(self.board))
        vertical = self.checkShape(self.board)
        diagonal = self.checkShape(diagonals(self.board))
        antidiagonal = self.checkShape(antidiagonals(self.board))

        if (antidiagonal or diagonal or vertical or horizontal) is not None:
            return True

        return False

    def checkShape(self, array):
        """

        :param array
        :return:
        """
        currentWinner = ""
        fourConnected = 1

        for i in array:
            for e in range(len(i)):
                if i[e] != " ":
                    if i[e] == currentWinner:
                        fourConnected += 1
                    else:
                        fourConnected = 1

                    currentWinner = i[e]
                    if fourConnected == 4:
                        break
                else:
                    currentWinner = " "
                    fourConnected = 1

            if fourConnected == 4:
                break

            fourConnected = 1
            currentWinner = " "

        if fourConnected == 4:
            self.winner = currentWinner
            return currentWinner

        return None


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


def diagonals(matrix):
    """
    """
    h, w = len(matrix), len(matrix[0])
    return [[matrix[h - p + q - 1][q]
             for q in range(max(p - h + 1, 0), min(p + 1, w))]
            for p in range(h + w - 1)]


def antidiagonals(matrix):
    """
    """
    h, w = len(matrix), len(matrix[0])
    return [[matrix[p - q][q]
             for q in range(max(p - h + 1, 0), min(p + 1, w))]
            for p in range(h + w - 1)]


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')
