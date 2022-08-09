from Board import Board
from Move import Move

def test_moves(board):
    userP = input("Which piece would like to use? (x or o)\n").lower
    if userP == "o":
        board.setPieces('o', 'x')
    else:
        board.setPieces('x', 'o')
    while True:
        board.printBoard()
        converted = False
        newBoard = None
        while not converted:
            column = input("Where would you like to place a piece?\n")
            try:
                column = int(column)
                userMove = Move(board.userTurn, column)
                newBoard = userMove.makeMove(board)
                # userMove.printMove()
                if newBoard == None:
                    continue
                converted = True
            except:
                print("Invalid input, try again")
        if newBoard.isTerminal():
            print("User won: " + str(newBoard.userWinner))
            print("Opp won: " + str(newBoard.oppWinner))
            break
        board = newBoard

def main():
    b1 = Board()
    test_moves(b1)

if __name__ == "__main__":
    main()