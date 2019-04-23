import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 1
AI_PIECE = 2

def createBoard():
    board = np.zeros((6, 7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Returns 'True' if a column is empty in the last row 
def is_valid_location(board, col):
    return board[5][col] == 0

# Returns the topmost vacant row in the board
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

def evaluate_window(window, piece):
    score = 0
    # To keep in check which player is playing currently
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
    
    if window.count(piece) == 4: # Winning arrangement
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1: # Any possible arrangement where there are atleast 3 similar pieces and 1 empty space
        score += 10
    elif window.count(piece) == 2 and window.count(2) == 2:
        score += 5
    
    # To block the opponent's pieces from connecting four
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 80
        
    return score

def score_position(board, piece):
    score = 0
    
    # Score the centre column
    centre_array = [int(i) for i in list(board[:, 3])]
    centre_count = centre_array.count(piece)
    score += centre_count * 6
    
    # Score horizontally
    for r in range(ROW_COUNT): # For traversing through each row 1-by-1
        row_array = [int(i) for i in list(board[r, :])] # Storing the whole row as a list in an array 1-by-1
        for c in range(COLUMN_COUNT - 3): # Taking into consideration all possible columns in the above said row
            window = row_array[c: c + 4] # Creating a window of 4 and sliding it 1-by-1
            
            score += evaluate_window(window, piece)
                
    # Score vertically
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r: r + 4]
            
            score += evaluate_window(window, piece)
                
    # Score a positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            
            score += evaluate_window(window, piece)
                
    # Score a negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            
            score += evaluate_window(window, piece)
    
    
    return score

# Check for a terminal node
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Implementation of minimax algorithm
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
    
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
        
    if maximizingPlayer: # The maximizing player is the AI_PIECE
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            
            # Now we need to get the best score as well as the column that produces it
            new_score = minimax(b_copy, depth - 1, False)[1] # We input FALSE because we want the PLAYER_PIECE to be next
            if new_score > value:
                value = new_score
                column = col
        return column, value
            
    else: # Minimizing player is the PLAYER_PIECE
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            
            new_score = minimax(b_copy, depth - 1, True)[1] # We input TRUE because we want the AI_PIECE to be next
            if new_score < value:
                value = new_score
                column = col
        return column, value

# To get all the empty columns
def get_valid_locations(board):
    
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations # Returns a list of columns that are empty/available

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations) # Randomly alloted just any column value
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy() # Since we are using 'numpy', hence we need to manually copy the board to another one
        drop_piece(temp_board, row, col, piece) # This is to simulate the board and check in which column would it be best to drop the piece in the original board
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col # Would be used to drop the piece in the original board
    
    return best_col

def draw_board(board):
    
    # Creating all the squares one by one
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # To draw the outer blue rectangle
            # Syntax = " rect(Surface, color, rectangle, width = 0) "
            pygame.draw.rect(screen, (0, 10, 230), (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))

            #To draw the inner black circles
            # Syntax = " circle(Surface, color, pos, radius, width = 0) "
            pygame.draw.circle(screen, (0, 0, 0), (int(c * SQUARESIZE + SQUARESIZE/2),int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                # To draw the red coin for player 1
                pygame.draw.circle(screen, (255, 0, 0), (int(c * SQUARESIZE + SQUARESIZE/2),height - int(r * SQUARESIZE + SQUARESIZE/2)), RADIUS)
                
            elif board[r][c] == AI_PIECE:
                # To draw the yellow coin for player 2
                pygame.draw.circle(screen, (255, 255, 0), (int(c * SQUARESIZE + SQUARESIZE/2),height - int(r * SQUARESIZE + SQUARESIZE/2)), RADIUS)
    
    pygame.display.update()

def print_board(board):
    print(np.flip(board, 0))

board = createBoard()
print_board(board)
game_over = False

# We want the first turn to be randomly allocated to either the player or the AI
turn = random.randint(0, 1)

pygame.init()

# We assume the circles to be as squares first
SQUARESIZE = 100

# The width and height of the screen
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

RADIUS = int((SQUARESIZE / 2) - 5)

size = (width, height)

# Creation/Initialization of the pygame window screen
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    
    # 'pygame' is an event-based library
    for event in pygame.event.get():
        
        # Checking whether the user has tried to close the window
        if event.type == pygame.QUIT:
            sys.exit()
        
        # Putting a coin in the empty buffer at the top while mouse is moving freely
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARESIZE/2)), RADIUS)
            
        
        pygame.display.update()
        
        # Checking whether the type of event is a click in the pygame window
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
            
            #Ask for Player 1's Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                # 'col' represents the column where the player will drop the coin
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    
                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins !! CONGRATULATIONS", 1, (255, 0, 0))
                        screen.blit(label, (40, 10))
                        game_over = True
                        
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)
                
    #Ask for Player 2's Input which is the AI in this case
    if turn == 1 and not game_over:
        
        # col = random.randint(0, COLUMN_COUNT - 1)
        # col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 3, True) # The middle parameter i.e., depth decides the difficulty level
        # Greater the depth, more difficult the game
        
        # 'col' represents the column where the AI-player will drop the coin
        
        if is_valid_location(board, col):
            
            #Adding a delay to the AI players move otherwise the user experience might not be that good
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            
            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 wins !! CONGRATULATIONS", 1, (255, 255, 0))
                screen.blit(label, (40, 10))
                game_over = True
        
            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2
            
            if game_over:
                pygame.time.wait(3000)
