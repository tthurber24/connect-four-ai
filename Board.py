class Board:
    height, width = 6,7

    def __init__(self):
        self.content = [[0 for i in range(self.width)] for j in range(self.height)]
        self.winnerP1 = False
        self.winnerP2 = False
        self.turnP1 = True
        self.piece1 = 'x'
        self.piece2 = 'o'
        self.parentMove = None
        self.utility = 0

    def setPieces(self, user, opp):
        self.piece1 = user
        self.piece2 = opp

    def isWon(self, piece):
        vMatchCount = self.vertMatch(piece)
        hMatchCount = self.horiMatch(piece)
        dMatchCount = self.diagMatch(piece)

        fours = vMatchCount[2] + hMatchCount[2] + dMatchCount[2]
        if fours > 0: # if there's at least 1 four in a row
            return True
        return False

    def isFull(self):
        for yCor in range(self.height):
            for xCor in range(self.width):
                if self.content[yCor][xCor] == 0:
                    return False
        return True

    def isTerminal(self):
        if self.winnerP1 == True:
            self.utility = -100
            return True
        elif self.winnerP2 == True:
            self.utility = 100
            return True
        else:
            self.winnerP1 = self.isWon(1)
            if not self.winnerP1: # if player 1 did not win, then check if the opponent won
                self.winnerP2 = self.isWon(-1)
                if not self.winnerP2: # if player 2 did not win
                    if self.isFull():
                        return True
                    return False
            return True
        
    def getUtility(self):
        if self.isTerminal():
            if self.winnerP1:
                return -100
            elif self.winnerP2:
                return 100
            else:
                return 0
        else:
            return self.heuristic()

    def updateMatches(self, matchCounts, matchNum):
        (twos, threes, fours) = matchCounts
        if matchNum == 2:
            twos += 1
        elif matchNum == 3:
            threes += 1
        elif matchNum == 4:
            fours += 1
        return twos, threes, fours

    # returns a tuple with the number of vertical pairs, 3s-in-a-row, and 4s-in-a-row
    def vertMatch(self, piece):
        twos, threes, fours = 0, 0, 0

        for xCor in range(self.width): # for each column
            yCor = 0
            matches = 0
            while yCor < self.height: # count contiguous matching pieces
                if self.content[yCor][xCor] == piece:
                    matches += 1
                else: # End of a contiguous sequence
                    twos, threes, fours = self.updateMatches((twos, threes, fours), matches)
                    matches = 0
                yCor += 1
            twos, threes, fours = self.updateMatches((twos, threes, fours), matches)
        return (twos, threes, fours)

    # returns a tuple with the number of horizontal pairs, 3s-in-a-row, and 4s-in-a-row
    def horiMatch(self, piece):
        twos, threes, fours = 0, 0, 0

        for yCor in range(self.height): # for each row
            xCor = 0
            matches = 0
            while xCor < self.width: # count contiguous matching pieces
                if self.content[yCor][xCor] == piece:
                    matches += 1
                else: # End of a contiguous sequence
                    twos, threes, fours = self.updateMatches((twos, threes, fours), matches)
                    matches = 0
                xCor += 1
            twos, threes, fours = self.updateMatches((twos, threes, fours), matches)
        return (twos, threes, fours)

    def diagLoop(self, matchCounts, piece, yCor, xCor, yOp, xOp):
        (twos, threes, fours) = matchCounts

        matches = 0
        while xCor in range(self.width) and yCor in range(self.height):
            if self.content[yCor][xCor] == piece:
                matches += 1
            else: # End of a contiguous sequence
                twos, threes, fours = self.updateMatches((twos, threes, fours), matches)
                matches = 0

            if yOp == "+":
                yCor += 1
            elif yOp == "-":
                yCor -= 1
            else:
                print("No y-op specified...")
                yCor += 1
            
            if xOp == "+":
                xCor += 1
            elif xOp == "-":
                xCor -= 1
            else:
                print("No x-op specified...")
                xCor += 1
            
        twos, threes, fours = self.updateMatches((twos, threes, fours), matches)
        return twos, threes, fours

    # returns a tuple with the number of diagonal pairs, 3s-in-a-row, and 4s-in-a-row
    def diagMatch(self, piece):
        twos, threes, fours = 0, 0, 0

        for yIndex in range(self.height):
            yCor = yIndex

            # Down and to the right
            xCor = 0
            (twos, threes, fours) = self.diagLoop((twos, threes, fours), piece, yCor, xCor, "+", "+")

            # Up and to the right
            (twos, threes, fours) = self.diagLoop((twos, threes, fours), piece, yCor, xCor, "-", "+")

            # Down and to the left
            xCor = self.width - 1
            (twos, threes, fours) = self.diagLoop((twos, threes, fours), piece, yCor, xCor, "+", "-")

            # Up and to the left
            (twos, threes, fours) = self.diagLoop((twos, threes, fours), piece, yCor, xCor, "-", "-")

        return (twos, threes, fours)

    def heuristic(self):
        vMatchCount = self.vertMatch(-1)
        hMatchCount = self.horiMatch(-1)
        dMatchCount = self.diagMatch(-1)

        twos = vMatchCount[0] + hMatchCount[0] + dMatchCount[0]
        threes = vMatchCount[1] + hMatchCount[1] + dMatchCount[1]

        score = (twos*3) + (threes*10)
        return score

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
                    print(self.piece1, end=" ")
                elif val == -1:
                    print(self.piece2, end=" ")
                else:
                    print('-', end=" ")
            print("")
        print("")

    def copyBoard(self):
        boardState = Board()
        for i in range(self.height):
            for j in range(self.width):
                boardState.content[i][j] = self.content[i][j]
        boardState.winnerP1 = self.winnerP1
        boardState.winnerP2 = self.winnerP2
        boardState.turnP1 = self.turnP1
        boardState.piece1 = self.piece1
        boardState.piece2 = self.piece2
        boardState.parentMove = self.parentMove
        return boardState

    def printData(self):
        for row in self.content:
            print(row)

    def openColumn(self, colIndex):
        if colIndex >= 0 and colIndex < self.width:
            if self.content[0][colIndex] == 0: # if the top spot in a column is open
                return True
        return False
       
def main():
    testB = Board()
    testB.content[5][5] = -1
    testB.content[4][5] = -1
    testB.content[3][5] = -1
    testB.content[5][4] = -1
    testB.content[4][4] = -1
    testB.printBoard()
    print(testB.heuristic())

if __name__ == "__main__":
    main()