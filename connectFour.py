import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def createBoard():
    board = np.zeros((6, 7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0
    
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    #Check all horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
            
    #Check all vertical locations for a win
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    
    #Check for positively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    
    #Check for negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def print_board(board):
    print(np.flip(board, 0))

board = createBoard()
print_board(board)
game_over = False
turn = 0

while not game_over:
    
    #Ask for Player 1's Input
    if turn == 0:
        col =  int(input("Player 1 make your selction (0 - 6)"))
        # 'col' represents the column where the player will drop the coin
        
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
            
            if winning_move(board, 1):
                print("Player 1 wins !! CONGRATULATIONS")
                game_over = True
        
    #Ask for Player 2's Input
    else:
        col =  int(input("Player 2 make your selction (0 - 6)"))
        # 'col' represents the column where the player will drop the coin
        
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            
            if winning_move(board, 2):
                print("Player 2 wins !! CONGRATULATIONS")
                game_over = True
    
    print_board(board)
    turn += 1
    turn = turn % 2