from Board import Board
from Move import Move

def test_moves(board):
    print("test")

def multiplayer(board):
    validSelect = False
    while not validSelect:
        userP = input("Would you like to be x or o?\n")
        try:
            userP = str(userP).lower()
            if userP == "o":
                board.setPieces('o', 'x')
                validSelect = True
            elif userP == "x":
                board.setPieces('x', 'o')
                validSelect = True
            else: # inputed a string but it wasn't x or o
                print("Please input either x or o")
                validSelect = False
        except:
            print("Invalid input, try again.")
    
    while True: # gameplay loop
        board.printBoard()
        if board.isTerminal():
            if board.winnerP1:
                print("Player 1 wins!")
            elif board.winnerP2:
                print("Player 2 wins!")
            else:
                print("There was a tie!")
            break
        converted = False
        newBoard = None
        while not converted:
            if board.turnP1:
                print("Player 1's turn:")
            else:
                print("Player 2's turn:")
            column = input("Where would you like to place a piece?\n")
            try:
                column = int(column)
                userMove = Move(board.turnP1, column)
                newBoard = userMove.makeMove(board)
                if newBoard == None:
                    continue
                converted = True
            except:
                print("Invalid input, try again")
        board = newBoard

def getOpenCols(board):
    cols = []
    for i in range(board.width):
        if board.openColumn(i):
            cols.append(i)
    return cols

def minimax(board, depth, isMax):
    if depth == 0 or board.isTerminal():
        return (board.getUtility(), -1)
    else:
        val = 0
        bestColIndex = -1

        if isMax:
            val = -1000
        else:
            val = 1000
        openCols = getOpenCols(board)
        for colIndex in openCols: # for each possible move, check the child and run minimax on it
            childMove = Move(board.turnP1, (colIndex + 1))
            childBoard = childMove.makeMove(board)
            if childBoard == None:
                print("Error computing minimax")
                return None
            
            if isMax:
                check = minimax(childBoard, (depth - 1), False)
                if check[0] > val: # if the current child produces a better result, update best column and utility
                    bestColIndex = colIndex
                    val = check[0]
            else: # if minimizing
                check = minimax(childBoard, (depth - 1), True)
                if check[0] < val:
                    bestColIndex = colIndex
                    val = check[0]
        return (val, bestColIndex)

def singleplayer(board):
    validSelect = False
    while not validSelect:
        userP = input("Would you like to be x or o?\n")
        try:
            userP = str(userP).lower()
            if userP == "o":
                board.setPieces('o', 'x')
                validSelect = True
            elif userP == "x":
                board.setPieces('x', 'o')
                validSelect = True
            else: # inputed a string but it wasn't x or o
                print("Please input either x or o")
                validSelect = False
        except:
            print("Invalid input, try again.")

        while True: # gameplay loop
            print()
            board.printBoard()
            if board.isTerminal():
                if board.winnerP1:
                    print("Player 1 wins!")
                elif board.winnerP2:
                    print("Player 2 wins!")
                else:
                    print("There was a tie!")
                break
            converted = False
            newBoard = None
            while not converted:
                if board.turnP1:
                    print("Player 1's turn:")
                    column = input("Where would you like to place a piece?\n")
                    try:
                        column = int(column)
                        userMove = Move(board.turnP1, column)
                        newBoard = userMove.makeMove(board)
                        if newBoard == None:
                            continue
                        converted = True
                    except:
                        print("Invalid input, try again")
                else:
                    print("Player 2's turn:")
                    cpuMinimax = minimax(board, 4, True)
                    index = cpuMinimax[1]
                    print("The computer places a piece in column " + str(index+1) + "!")
                    # print("Heuristic result:", cpuMinimax[0])

                    cpuMove = Move(board.turnP1, (index+1))
                    newBoard = cpuMove.makeMove(board)
                    if newBoard == None:
                        print("Error making minimax-computed move")
                        continue
                    converted = True
            board = newBoard

def main():
    b1 = Board()
    singleplayer(b1)

if __name__ == "__main__":
    main()