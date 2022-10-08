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

    # def verticalWin(self, yCor, xCor, piece):
    #     matches = 0
    #     for i in range(yCor, self.height): # vertical matches above
    #         if self.content[i][xCor] == piece:
    #             matches += 1
    #         else:
    #             break
    #     if matches == 4:
    #         return True

    #     matches = 0
    #     for i in range(0, (yCor + 1)): # vertical matches below
    #         if self.content[i][xCor] == piece:
    #             matches += 1
    #         else:
    #             break
    #     if matches == 4:
    #         return True
    #     return False

    # def horizontalWin(self, yCor, xCor, piece):
    #     matches = 0
    #     for i in range(xCor, self.width): # horizontal matches right
    #         if self.content[yCor][i] == piece:
    #             matches += 1
    #         else:
    #             break
    #     if matches == 4:
    #         return True

    #     matches = 0
    #     for i in range(0, (xCor + 1)): # horizontal matches left
    #         if self.content[yCor][i] == piece:
    #             matches += 1
    #         else:
    #             break
    #     if matches == 4:
    #         return True
    #     return False

    # def diagonalWin(self, yCor, xCor, piece):
    #     matches = 0

    #     # matches to the top left
    #     for i in range(4):
    #         yCheck = yCor - i
    #         xCheck = xCor - i
    #         if yCheck < 0 or xCheck < 0:
    #             break
    #         if self.content[yCheck][xCheck] == piece:
    #             matches += 1
    #     if matches == 4:
    #         return True

    #     matches = 0
    #     # matches to the top right
    #     for i in range(4):
    #         yCheck = yCor - i
    #         xCheck = xCor + i
    #         if yCheck < 0 or xCheck >= self.width:
    #             break
    #         if self.content[yCheck][xCheck] == piece:
    #             matches += 1
    #     if matches == 4:
    #         return True
        
    #     matches = 0
    #     # matches to the bottom left
    #     for i in range(4):
    #         yCheck = yCor + i
    #         xCheck = xCor - i
    #         if yCheck >= self.height or xCheck < 0:
    #             break
    #         if self.content[yCheck][xCheck] == piece:
    #             matches += 1
    #     if matches == 4:
    #         return True

    #     matches = 0
    #     # matches to the bottom right
    #     for i in range(4):
    #         yCheck = yCor + i
    #         xCheck = xCor + i
    #         if yCheck >= self.height or xCheck >= self.width:
    #             break
    #         if self.content[yCheck][xCheck] == piece:
    #             matches += 1
    #     if matches == 4:
    #         return True

    #     return False

    def isWon(self, piece):
        vMatchCount = self.vertMatch(piece)
        hMatchCount = self.horiMatch(piece)
        dMatchCount = self.diagMatch(piece)

        fours = vMatchCount[2] + hMatchCount[2] + dMatchCount[2]
        if fours > 0: # if there's at least 1 four in a row
            return True
        return False

    def isTerminal(self):
        if self.userWinner == True:
            self.utility = 100
            return True
        elif self.oppWinner == True:
            self.utility = -100
            return True
        else:
            self.userWinner = self.isWon(1)
            if not self.userWinner: # if the user did not win, then check if the opponent won
                self.oppWinner = self.isWon(-1)
                if not self.oppWinner:
                    return False
            return True

    def getUtility(self):
        if self.isTerminal():
            if self.userWinner:
                return -100
            elif self.oppWinner:
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

        print(vMatchCount)
        print(hMatchCount)
        print(dMatchCount)

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