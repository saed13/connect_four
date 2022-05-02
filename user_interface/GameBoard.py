# hide_output
# hide_input
# tst_local_only

from os import system, name, path

import pygame
import sys

directoryName = path.dirname("../resources/")
pathToResources = path.abspath(directoryName)

pygame.init()

size = width, height = 722, 622
speed = [2, 2]

screen = pygame.display.set_mode(size)
board = pygame.image.load(pathToResources + "/board.png")
p1_chip = pygame.image.load(pathToResources + "/chip_1.png")
p1_chip = pygame.transform.scale(p1_chip, (80, 80))
p2_chip = pygame.image.load(pathToResources + "/chip_2.png")
p2_chip = pygame.transform.scale(p2_chip, (80, 80))
boardrect = board.get_rect()


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
        self.chipPlace = self.defineChipPlace([[], [], [], [], [], [], []])

    def __str__(self):
        return self.toStr()

    def defineBoard(self, array):
        """

        :param array:
        :return:
        """
        for e in array:
            for i in range(0, 6):
                e.append(" ")
        return array

    def defineChipPlace(self, array):
        """

        :param array:
        :return:
        """
        for i in range(0, len(array)):
            for e in range(0, 6):
                array[i].append((16 + 100 * i, 518 - 100 * e))
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
        while noWinner:
            ev = pygame.event.get()
            # proceed events
            for event in ev:

                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP and not stop:
                    pos = pygame.mouse.get_pos()

                    col = self.askInput(pos)
                    if col == -1:
                        break

                    isWinner = self.addToken(col)

                    if isWinner:
                        stop = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit()

            screen.blit(board, boardrect)
            pygame.display.flip()

    def askInput(self, pos):
        """
        :param: pos
        :return:
        """
        try:
            self.p = 1 if self.p1 else 2
            if pos == "stop":
                exit()

            column = int(pos[0] / 100 - 0.05)
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

        screen.blit(p1_chip, self.chipPlace[col][row]) if self.p1 else screen.blit(p2_chip, self.chipPlace[col][row])
        if self.p1:
            self.board[col][row] = "p1"
        else:
            self.board[col][row] = "p2"

        winner = self.checkWinner()

        self.p1 = not self.p1
        self.p2 = not self.p2
        return winner

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
             for q in range(max(p-h+1, 0), min(p+1, w))]
            for p in range(h + w - 1)]


def antidiagonals(matrix):
    """
    """
    h, w = len(matrix), len(matrix[0])
    return [[matrix[p - q][q]
             for q in range(max(p-h+1,0), min(p+1, w))]
            for p in range(h + w - 1)]


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')
