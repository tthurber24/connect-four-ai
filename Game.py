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
                    if cpuMinimax == None:
                        return
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

def inputMove(board):
    converted = False
    newBoard = None
    while not converted:
        column = input("Where would you like to place a piece?\n")
        try:
            column = int(column)
            userMove = Move(board.turnP1, column)
            newBoard = userMove.makeMove(board)
            if newBoard == None:
                print("Error making move, please try again.")
                continue
            converted = True
        except:
            print("Invalid input, try again")
    return newBoard

def minimaxMove(board):
    success = False
    while not success:
        cpuMinimax = minimax(board, 4, True)
        if cpuMinimax == None:
            print("Error computing minimax.")
            continue
        index = cpuMinimax[1]
        print("The computer places a piece in column " + str(index+1) + "!")

        cpuMove = Move(board.turnP1, (index+1))
        newBoard = cpuMove.makeMove(board)
        if newBoard == None:
            print("Error making minimax-computed move")
            continue
        success = True
    return newBoard

def gameloop(board, players):
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
        
        if board.turnP1:
            print("Player 1's turn:")
            board = inputMove(board)
        else:
            print("Player 2's turn:")
            if players == 2: # if multiplayer
                board = inputMove(board)
            else: # if singleplayer
                board = minimaxMove(board)

def gameplay(board):
    print("Welcome to Connect 4!")

    # Selecting the game mode
    players = 1
    playerSelect = False
    while not playerSelect:
        players = input("Enter 1 for single player or 2 for multiplayer:\n")
        try:
            players = int(players)
            if players == 1 or players == 2:
                playerSelect = True
            else: # inputed a number other than 1 or 2
                print("Please enter either 1 or 2.")
        except: # did not input a number
            print("Invalid input, please try again.")

    # Selecting the game pieces
    validSelect = False
    while not validSelect:
        userP = input("Would you (Player 1) like to be x or o?\n")
        try:
            userP = str(userP).lower()
            if userP == "o":
                board.setPieces('o', 'x')
                validSelect = True
                print("Player 2 will be 'x'")
            elif userP == "x":
                board.setPieces('x', 'o')
                validSelect = True
                print("PLayer 2 will be 'o'")
            else: # inputed a string but it wasn't x or o
                print("Please input either x or o")
        except:
            print("Invalid input, try again.")

    gameloop(board, players)

def main():
    b1 = Board()
    gameplay(b1)

if __name__ == "__main__":
    main()