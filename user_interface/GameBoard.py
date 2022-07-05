from os import system, name
from user_interface.Players import Human, AI


class GameBoard:
    """
    mode 1: player vs player
    mode 2: player vs AI
    mode 3: AI vs AI
    """
    board = []
    p1 = True
    p2 = False

    def __init__(self, mode):
        self.winner = None
        self.p = None
        self.board = self.define_board([[], [], [], [], [], [], []])
        self._mode = mode
        self.player1 = AI(1)
        self.player2 = AI(2)

    def __str__(self):
        return self.to_str()

    @property
    def mode(self):
        return self._mode

    @staticmethod
    def define_board(array):
        """
        define a board with empty strings, 7 columns and 6 rows
        :param array: matrix containing 7 empty arrays
        :return: board matrix
        """
        for e in array:
            for i in range(0, 6):
                e.append(" ")
        return array

    def to_str(self):
        """
        :return: current board as string
        """
        transposed = transpose(self.board)

        current_board = ""
        for e in transposed:
            for i in e:
                current_board += i + " | "
            current_board += "\n"

        return current_board

    def add_token(self, col):
        """
        gets column number, check if there is a winner using winning algorithm and in which row the token should be placed
        :param col: column number
        :return: if winner exists, (col, row), next player, winner, updated class object
        """
        row = self.board[col].index(' ')

        place = (col, row)

        if self.p1:
            self.board[col][row] = "p1"
        else:
            self.board[col][row] = "p2"

        winner_exists, winner = check_winner(self.board)
        if winner_exists:
            self.winner = winner

        self.p1 = not self.p1
        self.p2 = not self.p2

        return winner_exists, place, not self.p1, self.winner, self


# help methods
def check_winner(board):
    """
    check if there is a winner in the 4 possible lines
    :param board: current board
    :return: if there is a winner, True and which player(1 or 2). otherwise False.
    """
    horizontal = check_shape(transpose(board))
    if horizontal is not None:
        return True, horizontal

    vertical = check_shape(board)
    if vertical is not None:
        return True, vertical

    diagonal = check_shape(diagonals(board))
    if diagonal is not None:
        return True, diagonal

    anti_diagonal = check_shape(anti_diagonals(board))
    if anti_diagonal is not None:
        return True, anti_diagonal

    return False, None


def check_shape(array):
    """
    check for 4 connected tokens in one array in the matrix
    :param array: transposed matrix.
    :return: the winner if exists
    """
    current_winner = ""
    four_connected = 1

    for i in array:
        for e in range(len(i)):
            if i[e] != " ":
                if i[e] == current_winner:
                    four_connected += 1
                else:
                    four_connected = 1

                current_winner = i[e]
                if four_connected == 4:
                    break
            else:
                current_winner = " "
                four_connected = 1

        if four_connected == 4:
            break

        four_connected = 1
        current_winner = " "

    if four_connected == 4:
        return current_winner

    return None


def transpose(matrix):
    """
    transpose matrix to check horizontal lines
    :param matrix:
    :return: transposed matrix
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
    :param matrix:
    :return: diagonal lines in single arrays
    """
    h, w = len(matrix), len(matrix[0])
    return [[matrix[h - p + q - 1][q]
             for q in range(max(p - h + 1, 0), min(p + 1, w))]
            for p in range(h + w - 1)]


def anti_diagonals(matrix):
    """
    :param matrix:
    :return: anti-diagonal lines in single arrays
    """
    h, w = len(matrix), len(matrix[0])
    return [[matrix[p - q][q]
             for q in range(max(p - h + 1, 0), min(p + 1, w))]
            for p in range(h + w - 1)]

