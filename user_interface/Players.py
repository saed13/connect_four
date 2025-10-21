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
        self.depth = 5  # Increased depth for stronger play

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

    def order_moves(self, valid_locations, board_width):
        """Order moves to prioritize center columns for better alpha-beta pruning"""
        center = board_width // 2
        # Sort by distance from center (closer to center = higher priority)
        return sorted(valid_locations, key=lambda col: abs(col - center))

    def get_AIMove(self, board):
        """Use minimax with alpha-beta pruning to find the best move"""
        valid_locations = self.get_valid_locations(board)

        if not valid_locations:
            return None

        # Order moves to check center columns first for better pruning
        valid_locations = self.order_moves(valid_locations, len(board))

        best_col = valid_locations[0]
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for col in valid_locations:
            board_copy = copy.deepcopy(board)
            board_copy = self.add_token(board_copy, col, self._turn)

            # Call minimax for opponent's turn (minimizing player)
            _, score = self.alphabeta(board_copy, self.depth - 1, alpha, beta, False)

            if score > best_score:
                best_score = score
                best_col = col

            alpha = max(alpha, best_score)

        return best_col

    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        """Minimax algorithm with alpha-beta pruning"""
        valid_locations = self.get_valid_locations(board)
        other_player = self.change_player(self._turn)

        # Terminal conditions
        is_terminal = (depth == 0 or
                      len(valid_locations) == 0 or
                      self.is_winning(board, self._turn) or
                      self.is_winning(board, other_player))

        if is_terminal:
            if self.is_winning(board, self._turn):
                return None, 100000000  # AI wins
            elif self.is_winning(board, other_player):
                return None, -100000000  # Opponent wins
            elif len(valid_locations) == 0:
                return None, 0  # Draw
            else:
                # Depth limit reached, evaluate position
                return None, self.evaluate_points(board, self._turn)

        # Order moves for better pruning
        valid_locations = self.order_moves(valid_locations, len(board))

        if maximizingPlayer:
            best_score = -math.inf
            best_col = valid_locations[0]

            for col in valid_locations:
                board_copy = copy.deepcopy(board)
                board_copy = self.add_token(board_copy, col, self._turn)
                _, score = self.alphabeta(board_copy, depth - 1, alpha, beta, False)

                if score > best_score:
                    best_score = score
                    best_col = col

                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break  # Beta cutoff

            return best_col, best_score
        else:
            best_score = math.inf
            best_col = valid_locations[0]

            for col in valid_locations:
                board_copy = copy.deepcopy(board)
                board_copy = self.add_token(board_copy, col, other_player)
                _, score = self.alphabeta(board_copy, depth - 1, alpha, beta, True)

                if score < best_score:
                    best_score = score
                    best_col = col

                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cutoff

            return best_col, best_score

    def evaluate_points(self, board, current_player):
        """Enhanced evaluation function with positional bonuses"""
        score = 0

        # Evaluate all four directions
        score += self.count_points(board)
        score += self.count_points(GameBoard.transpose(board))
        score += self.count_points(GameBoard.diagonals(board))
        score += self.count_points(GameBoard.anti_diagonals(board))

        # Add center column preference bonus
        score += self.evaluate_center_control(board)

        return score

    def evaluate_center_control(self, board):
        """Reward controlling center columns (more strategic positions)"""
        score = 0
        center_col = len(board) // 2
        other_player = self.change_player(self._turn)

        # Check center column
        center_count_ai = 0
        center_count_opp = 0

        if center_col < len(board):
            for row in range(len(board[center_col])):
                if board[center_col][row] == 'p' + str(self._turn):
                    center_count_ai += 1
                elif board[center_col][row] == 'p' + str(other_player):
                    center_count_opp += 1

        # Give bonus for center control
        score += center_count_ai * 3
        score -= center_count_opp * 3

        # Check adjacent center columns
        for offset in [-1, 1]:
            col = center_col + offset
            if 0 <= col < len(board):
                for row in range(len(board[col])):
                    if board[col][row] == 'p' + str(self._turn):
                        score += 2
                    elif board[col][row] == 'p' + str(other_player):
                        score -= 2

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
