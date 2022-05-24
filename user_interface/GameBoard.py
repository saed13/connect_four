from os import system, name, environ
from Players import Human, AI
from dotenv import load_dotenv
import redis as redis

load_dotenv()
REDIS_KEY = environ.get('REDIS_KEY')

r = redis.Redis(host='connect-four.redis.cache.windows.net', port=6380, db=0, password=REDIS_KEY, ssl=True)
# r = redis.Redis(host='http://172.17.0.3')
r.set("second", "test")


# print(r.get("test"))

class GameBoard:
    """
    mode 1: player vs player
    mode 2: player vs AI
    mode 3: AI vs AI
    """
    board = []
    p1 = True
    p2 = False

    def __init__(self, mode=1):
        self.winner = None
        self.p = None
        self.board = self.define_board([[], [], [], [], [], [], []])
        self._mode = mode
        self.player1 = Human("John_Doe", 1)
        self.player2 = Human("John_Doe1", 2)

    def __str__(self):
        return self.to_str()

    @property
    def mode(self):
        return self._mode

    @staticmethod
    def define_board(array):
        """

        :param array:
        :return:
        """
        for e in array:
            for i in range(0, 6):
                e.append(" ")
        return array

    def to_str(self):
        """

        :return:
        """
        transposed = transpose(self.board)

        current_board = ""
        for e in transposed:
            for i in e:
                current_board += i + " | "
            current_board += "\n"

        return current_board

    def start_game(self):
        """

        :return:
        """
        noWinner = True
        stop = False

    def get_input(self, pos):
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

    def AI_move(self):
        current_player = self.player1 if self.p1 else self.player2

        column = current_player.next_move(self.board)
        if column == -1:
            return "full"

        return self.add_token(column)

    def add_player(self, human, name):
        current_player = 1 if self.player1 is not None else 2

        player = Human(name, current_player) if human else AI(current_player)

        if current_player == 1:
            self.player1 = player
        else:
            self.player2 = player

        return player

    def add_token(self, col):
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

        winner_exists, winner = check_winner(self.board)
        if winner_exists:
            self.winner = winner

        self.p1 = not self.p1
        self.p2 = not self.p2

        return winner_exists, place, not self.p1, self.winner


def check_winner(board):
    """

    :return:
    """
    horizontal = check_shape(transpose(board))
    if horizontal is not None:
        return True, horizontal
    vertical = check_shape(board)
    if vertical is not True:
        return True, vertical
    diagonal = check_shape(diagonals(board))
    if diagonal is not True:
        return True, diagonal
    anti_diagonal = check_shape(anti_diagonals(board))
    if anti_diagonal is not True:
        return True, anti_diagonal

    return False, None


def check_shape(array):
    """

    :param array
    :return:
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


def anti_diagonals(matrix):
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
