from Board import Board

class Move:
    def __init__(self, userTurn, col):
        self.userTurn = userTurn
        self.placement = col
        self.valid = False

    def isValid(self):
        if not self.valid:
            if self.placement < 8:
                if self.placement >= 0:
                    self.valid = True
        return self.valid

    def makeMove(self, boardState):
        if self.isValid() and self.userTurn == boardState.userTurn:
            colIndex = self.placement - 1
            rowIndex = -1

            for i in range(boardState.height): # goes to the selected column and finds the lowest spot
                if boardState.content[i][colIndex] == 0:
                    rowIndex = i
                else:
                    break

            if rowIndex != -1: # a valid move is found
                newBoard = boardState.copyBoard()

                if self.userTurn:
                    newBoard.content[rowIndex][colIndex] = 1
                else:
                    newBoard.content[rowIndex][colIndex] = -1
                newBoard.userTurn = not boardState.userTurn # since a move was made, turns switch
                newBoard.parentMove = self.placement
                return newBoard
            else:
                print("Column is filled already, please try again.")
                return None
            
        else:
            print("Move is invalid, please try again.")
            return None

    def printMove(self):
        print("Move --> Column: {}, userTurn: {}, isValid: {}".format(self.placement, self.userTurn, self.valid))