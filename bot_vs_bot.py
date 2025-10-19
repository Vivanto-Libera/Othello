import keras
from board import Board
import random
import numpy as np

newModel = keras.models.load_model("new_model.keras")
aboard = Board()

def fst(a):
    return a[0]

def bot_vs_bot(board):
    while(not fst(board.isTerminal())):
        board.printBoard()
        q = newModel.predict(np.array([board.networkInput()]))
        masked_output = [ 0 for x in range(0,65)]
        for m in board.legalMoves():
            m_idx = board.getNetworkOutputIndex(m)
            masked_output[m_idx] = q[0][0][m_idx]
        print(masked_output)
        best_idx = np.argmax(masked_output)
        sel_move = None
        for m in board.legalMoves():
            m_idx = board.getNetworkOutputIndex(m)
            if(best_idx == m_idx):
                sel_move = m
        board.applyMove(sel_move)
        continue
    terminal, winner = board.isTerminal()
    return winner

bot_vs_bot(aboard)
