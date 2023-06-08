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
def main():
    b1 = Board()
    multiplayer(b1)

if __name__ == "__main__":
    main()