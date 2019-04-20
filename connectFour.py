import numpy as np

def createBoard():
    board = np.zeros((6, 7))
    return board

board = createBoard()
game_over = False
turn = 0

while not game_over:
    
    #Ask for Player 1 Input
    if turn == 0:
        selection =  int(input("Player 1 make your selction (0 - 6)"))
        
    #Ask for Player 2 Input
    else:
        selection =  int(input("Player 2 make your selction (0 - 6)"))
        
    turn += 1
    turn = turn % 2