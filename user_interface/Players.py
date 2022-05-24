import names
import math


class Player:
    def __init__(self, name, turn, _type):
        self._name = name
        self._turn = turn
        self._type = _type

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

    def next_move(self, board):
        pass

    def alphabeta(self, board, depth, a, b, maximizingPlayer):
        valid_locations = get_valid_locations()
        if depth == 0:
            return board
        if maximizingPlayer:
            v = -math.inf
            for col in valid_locations:
                v = max(v, self.alphabeta(col, depth - 1, a, b, False))
                a = max(a, v)
                if a >= b:
                    break
                return v
        else:
            v = math.inf
            for col in valid_locations:
                v = min(v, self.alphabeta(col, depth - 1, a, b, True))
                b = min(b,v)
                if b <= a:
                    break
                return v



