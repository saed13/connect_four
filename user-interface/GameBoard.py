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
            for i in range(0, 8):
                e.append(" ")

    def __str__(self):
        transposed = self.transpose(self.board)

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
            x = self.askInput
            print(x)

    @property
    def askInput(self):
        """

        :return:
        """
        self.p = 1 if self.p1 else 2
        column = input(f"Player {self.p}, enter your move[1-7]:")

        result = self.addToken(int(column))
        return result

    def addToken(self, column):
        """

        :param column:
        :return:
        """
        currentBoard = self.board
        column = column - 1

        for i in range(7, -1, -1):
            if currentBoard[column][i] == " ":
                currentBoard[column][i] = self.p1symbol if self.p1 else self.p2symbol

                self.p1 = not self.p1
                self.p2 = not self.p2
                break

        self.board = currentBoard
        return str(gameBoard)

    def transpose(self, matrix):
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


gameBoard = GameBoard()

gameBoard.startGame()



