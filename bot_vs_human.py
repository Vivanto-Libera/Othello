import keras
from board import Board
import random
import numpy as np

def fst(a):
    return a[0]
COLS = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,}

model = keras.models.load_model("new_model.keras")
color = input('Do you want play black or white, enter b or w to select')
if color == 'b':
     botColor = Board.WHITE
else:
     botColor = Board.BLACK
board = Board()
while(not fst(board.isTerminal())):
        board.printBoard()
        if(board.turn == botColor):
            q = model.predict(np.array([board.networkInput()]))
            masked_output = [ 0 for x in range(0,65)]
            for m in board.legalMoves():
                m_idx = board.getNetworkOutputIndex(m)
                masked_output[m_idx] = q[0][0][m_idx]
            best_idx = np.argmax(masked_output)
            sel_move = None
            for m in board.legalMoves():
                m_idx = board.getNetworkOutputIndex(m)
                if(best_idx == m_idx):
                    sel_move = m
            board.applyMove(sel_move)
            continue
        else:
            moves = board.legalMoves()
            if board.legal_move == 0:
                board.applyMove((-1, -1))
                print("You passed.")
                continue
            while True:
                move = input('Your Move:')
                col = COLS[move[0]]
                row = 8 - int(move[1])
                if (row, col) in moves:
                     board.applyMove((row, col))
                     break
            continue
            
terminal, winner = board.isTerminal()
board.printBoard()
print(winner)