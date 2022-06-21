import math
import user_interface.GameBoard as GameBoard
import copy

class Player:
    def __init__(self, name, turn, type):
        self._name = name
        self._turn = turn
        self._type = type

    @property
    def name(self):
        return self._name

    @property
    def turn(self):
        return self._turn

    @property
    def type(self):
        return self._type

    def next_move(self, board):
        pass


class Human(Player):
    def __init__(self, name, turn):
        super(Human, self).__init__(name, turn, "human")


class AI(Player):
    def __init__(self, turn):
        super(AI, self).__init__('AI', turn, "AI")
        self.tree = None
        self.depth = 5

    def next_move(self, board):
        pass

    def change_player(self, current_player):
        next_player = 2 if current_player == 1 else 1
        return next_player

    def add_token(self, board, col, player):
        if board[col].index(' ') != 0:
            row = board[col].index(' ')
            board[col][row] = "p" + str(player)
        return board
    ''''|6| | | | | | | |
        |5| | | | | | | |
        |4| | | | | | | |
        |3| | | | | | | |
        |2| | | | | | | |
        |1| | | | | | | |
        |0| | | | | | | |'''
    def get_valid_locations(self, board):
        valid_locations = []
        for i in range(0, len(board)):
            if ' ' in board[i][len(board[i]) - 1]:
                valid_locations.append(i)

        return valid_locations

    def get_AIMove(self, board):
        board_copy = copy.deepcopy(board)
        valid_locations = self.get_valid_locations(board_copy)
        best_score = -math.inf
        best_col = None

        for location in valid_locations:
            #current_board = self.add_token(board, location, self._turn)
            board_copy[location][board_copy[location].index(' ')] = 'p' + str(self._turn)
            vert_points = self.evaluate_points(board_copy, self._turn)
            if vert_points > best_score:
                best_score = vert_points
                best_col = location

            horizontal = GameBoard.transpose(board_copy)
            horiz_points = self.evaluate_points(horizontal, self._turn)
            if horiz_points > best_score:
                best_score = horiz_points
                best_col = location

            diag = GameBoard.diagonals(board_copy)
            diag_points = self.evaluate_points(diag, self._turn)
            if diag_points > best_score:
                best_score = diag_points
                best_col = location

            anti_diag = GameBoard.anti_diagonals(board_copy)
            anti_diag_points = self.evaluate_points(anti_diag, self._turn)
            if anti_diag_points > best_score:
                best_score = anti_diag_points
                best_col = location

        return best_col

    def alphabeta(self, board, depth, a, b, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        best_move = None

        if depth == 0 or self.is_winning(board, 1) or self.is_winning(board, 2):
            return self.evaluate_points(board, self._turn)

        if maximizingPlayer:
            v = -math.inf
            for col in valid_locations:
                current_board = self.add_token(board, col, self._turn)
                score = max(v, self.alphabeta(current_board, depth - 1, a, b, False))
                if score > v:
                    v = score
                    best_move = col
                if score >= b:
                    break
                a = max(a, score)
                return best_move
        else:
            v = math.inf
            for col in valid_locations:
                current_player = self.change_player(self._turn)
                current_board = self.add_token(board, col, current_player)
                score = min(v, self.alphabeta(current_board, depth - 1, a, b, True))
                if score < v:
                    v = score
                    best_move = col
                if b <= a:
                    break
                b = min(b, score)
                return best_move

    def evaluate_points(self, board, current_player):
        score = 0
        other_player = self.change_player(current_player)
        # vertical
        score += self.count_points(board, current_player, other_player)
        # horizontal
        horizontal = GameBoard.transpose(board)
        score += self.count_points(horizontal, current_player, other_player)
        # diag
        diag = GameBoard.diagonals(board)
        score += self.count_points(diag, current_player, other_player)
        # anti_diag
        anti_diag = GameBoard.anti_diagonals(board)
        score += self.count_points(anti_diag, current_player, other_player)

        return score

    def count_points(self, board, current_player, other_player):
        score = 0
        piece_count = 0
        streak = other_player
        if self.is_winning(board):
            score = 1000
        if self.is_winning(board):
            score = -1000
        for row in range(0, len(board)):
            for col in range(0, len(board[row])):
                if board[row][col] == ' ':
                    break
                if board[row][col] == 'p' + str(current_player):
                    piece_count += 1
                    if piece_count == 3:
                        score += 100
                    elif piece_count == 2:
                        score += 20
                    elif piece_count == 1:
                        score += 1

                elif board[row][col] == 'p' + str(other_player):
                    if streak != other_player:
                        piece_count = 0
                    piece_count += 1
                    if piece_count == 3:
                        score -= 100
                    elif piece_count == 2:
                        score -= 20
                    elif piece_count == 1:
                        score -= 1
        return score

    def is_winning(self, board): #don't ask me df is going on here.
        if GameBoard.check_winner(board) and self._turn:
            return True
        return False



"""
    # minimax algorithm to determine best move
    def minimax(self, board, depth, maximizingPlayer):
        if depth == 0:
            return math.inf
        valid_locations = self.get_valid_locations(board)
        if maximizingPlayer:
            bestScore = -math.inf
            for col in range(len(valid_locations)):
                boardCopy = board
                boardCopy = self.add_token(boardCopy, col, self._turn)
                score = self.minimax(boardCopy, depth - 1, False)
                bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = math.inf
            for col in range(len(valid_locations)):
                boardCopy = board
                player = self.change_player(self._turn)
                boardCopy = self.add_token(boardCopy, col, player)
                score = self.minimax(boardCopy, depth - 1, True)
                bestScore = min(score, bestScore)
            return bestScore
"""



