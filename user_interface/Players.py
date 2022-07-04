import names
import math
import user_interface.GameBoard as GameBoard
import random
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
        super(AI, self).__init__(names.get_first_name(), turn, "AI")
        self.tree = None
        self.depth = 3

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

    def get_valid_locations(self, board):
        valid_locations = []
        for i in range(0, len(board)):
            if ' ' in board[i][len(board[i]) - 1]:
                valid_locations.append(i)
        return valid_locations

    def get_AIMove(self, board):
        valid_locations = self.get_valid_locations(board)
        best_score = -math.inf
        best_col = random.choice(valid_locations)

        for location in valid_locations:
            board_copy = copy.deepcopy(board)
            # copy from updated played board
            board_copy[location][board_copy[location].index(' ')] = 'p' + str(self._turn)

            score = self.evaluate_points(board_copy, self._turn)
            # clear last move
            if score > best_score:
                best_col = location
                best_score = score

        return best_col

    def alphabeta(self, board, depth, a, b, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)

        if depth == 0 or len(valid_locations) == 0 or self.is_winning(1) or self.is_winning(2):
            return None, self.evaluate_points(board, self._turn)

        if maximizingPlayer:
            column = random.choice(valid_locations)
            best_score = -math.inf
            for col in valid_locations:
                current_board = self.add_token(board, col, self._turn)
                score = self.alphabeta(current_board, depth - 1, a, b, False)
                best_score = max(best_score, score)
                column = col
                a = max(a, best_score)
                if a >= b:
                    break
            return column, best_score
        else:
            column = random.choice(valid_locations)
            best_score = math.inf
            for col in valid_locations:
                current_player = self.change_player(self._turn)
                current_board = self.add_token(board, col, current_player)
                score = self.alphabeta(current_board, depth - 1, a, b, True)
                best_score = min(best_score, score)
                column = col
                b = min(b, best_score)
                if b <= a:
                    break
        return column, best_score

    def evaluate_points(self, board, current_player):
        score = 0
        # vertical
        score += self.count_points(board)
        # horizontal
        score += self.count_points(GameBoard.transpose(board))
        # diag
        score += self.count_points(GameBoard.diagonals(board))
        # anti_diag
        score += self.count_points(GameBoard.anti_diagonals(board))

        return score

    def count_points(self, board):
        other_player = 1 if self._turn == 2 else 2
        if self.is_winning(board, self._turn):
            score = 10000
        elif self.is_winning(board, other_player):
            score = -10000
        else:
            score = 0
            for col in range(0, len(board)):
                for row in range(0, len(board[col])):
                    try:
                        if board[col][row] == 'p' + str(self._turn):
                            score += 1
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == 'p' + str(self._turn):
                            score += 10
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == board[col][row + 2] == 'p' + str(self._turn):
                            score += 50
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == board[col][row + 2] == board[col][
                            row + 3] == 'p' + str(self._turn):
                            score += 100000
                    except:
                        pass
                    try:
                        if board[col][row] == 'p' + str(other_player):
                            score -= 2
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == 'p' + str(other_player):
                            score -= 15
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == 'p' + str(other_player) and board[col][
                            row + 3] == 'p' + str(self.turn):
                            score += 100
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == board[col][row + 2] == 'p' + str(other_player):
                            score -= 70
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == board[col][row + 2] == 'p' + str(other_player) and \
                                board[col][row + 3] == 'p' + str(self.turn):
                            score += 11000
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row - 1] == board[col][row - 2] == 'p' + str(other_player) and \
                                board[col][row - 3] == 'p' + str(self.turn):
                            score += 11000
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == board[col][row + 3] == 'p' + str(other_player) and \
                                board[col][row + 2] == 'p' + str(self.turn):
                            score += 11000
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == board[col][row + 2] == 'p' + str(other_player) and \
                                board[col][row + -1] == 'p' + str(self.turn):
                            score += 11000
                    except:
                        pass

                    try:
                        if board[col][row] == board[col][row + 1] == board[col][row + 2] == board[col][
                            row + 3] == 'p' + str(other_player):
                            score -= 10000
                    except:
                        pass
                    try:
                        if board[col][row] == board[col][row + 1] == board[col][row + 2] == board[col][
                            row + 4] == 'p' + str(other_player):
                            score -= 10000
                    except:
                        pass
        return score

    def winning_move(self, board, current_player):
        for col in range(0, len(board)):
            for row in range(0, len(board[col])):
                try:
                    if board[col][row] == board[col][row + 1] == board[col][row + 2] == board[col][
                        row + 3] == 'p' + str(current_player):
                        return True
                except IndexError:
                    pass

    def is_winning(self, board, current_player):
        if self.winning_move(board, current_player):
            return True
        if self.winning_move(GameBoard.transpose(board), current_player):
            return True
        if self.winning_move(GameBoard.diagonals(board), current_player):
            return True
        if self.winning_move(GameBoard.anti_diagonals(board), current_player):
            return True
    # def is_winning(self, board):  # don't ask me df is going on here.
    #     if GameBoard.check_winner(board):
    #         return True
    #     return False


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
