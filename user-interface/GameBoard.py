class GameBoard:
    board = []
    p1 = True
    p1symbol = "X"
    p2symbol = "O"

    def __init__(self):
        self.column = None
        self.p = None
        self.board = [[], [], [], [], [], []]
        for e in self.board:
            for i in range(0, 7):
                e.append(" ")

    def __str__(self):
        currentBoard = ""
        for e in self.board:
            for i in e:
                currentBoard +=  i + " "
            currentBoard += "\n"
        return currentBoard

    def askInput(self):
        self.p = 1 if self.p1 else 2
        self.column = input(f"Player {self.p}, enter your move[1-7]:")
        p1 = not self.p1
        return int(self.column)

    def addToken(self, column):
        currentBoard = self.board
        column = column - 1
        for i in range(6, 0, -1):
            if currentBoard[column][i] == " ":
                currentBoard[column][i] = self.p1symbol
                break
        self.board = currentBoard
        return self.board

gameBoard = GameBoard()
while True:
    x = gameBoard.askInput()
    y = gameBoard.addToken(x)
    print(y)
