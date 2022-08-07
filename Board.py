class Board:
    height, width = 6,7

    def __init__(self):
        self.content = [[0 for i in range(self.width)] for j in range(self.height)]
        self.userWinner = False
        self.oppWinner = False
        self.userTurn = True
        self.userPiece = 'x'
        self.oppPiece = 'o'
        self.parentMove = None
        self.utility = 0

    def setPieces(self, user, opp):
        self.userPiece = user
        self.oppPiece = opp

    def verticalWin(self, yCor, xCor, piece):
        matches = 0
        for i in range(yCor, self.height): # vertical matches above
            if self.content[i][xCor] == piece:
                matches += 1
        if matches == 4:
            return True

        matches = 0
        for i in range(0, (yCor + 1)):
            if self.content[i][xCor] == piece:
                matches += 1
        if matches == 4:
            return True
        return False

    def isWon(self, piece):
        for i in range(self.height - 3):
            for j in range(self.width - 3):
                value = self.content[i][j]
                if value == piece: # a spot is occupied
                    win = True
        return False

    def isTerminal(self):
        if self.userWinner == True:
            self.utility = 1000
            return True
        elif self.oppWinner == True:
            self.utility = -1000
            return True
        else:
            print("testing")
            self.userWinner = self.isWon(1)
            if not self.userWinner: # if the user did not win, then check if the opponent won
                self.oppWinner = self.isWon(-1)
                if not self.oppWinner:
                    return False
            return True

    def printBoard(self):
        for i in range(1,8):
            print(i, end=" ")
        print("")
        for i in range(13):
            print('_', end="")
        print("")

        for row in self.content:
            for val in row:
                if val == 1:
                    print(self.userPiece, end=" ")
                elif val == -1:
                    print(self.oppPiece, end=" ")
                else:
                    print('-', end=" ")
            print("")
        print("")

    def copyBoard(self):
        boardState = Board()
        for i in range(self.height):
            for j in range(self.width):
                boardState.content[i][j] = self.content[i][j]
        boardState.userWinner = self.userWinner
        boardState.oppWinner = self.oppWinner
        boardState.userTurn = self.userTurn
        boardState.userPiece = self.userPiece
        boardState.oppPiece = self.oppPiece
        boardState.parentMove = self.parentMove
        return boardState

    def printData(self):
        for row in self.content:
            print(row)

    def openColumn(self, col):
        colIndex = col - 1
        if colIndex >= 0 and colIndex < self.width:
            if self.content[0][colIndex] == 0: # if the top spot in a column is open
                return True
        return False
       
