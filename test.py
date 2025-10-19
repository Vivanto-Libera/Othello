import keras
from board import Board
import random
import numpy as np

newModel = keras.models.load_model("new_model.keras")

def fst(a):
    return a[0]

def new_vs_old(board):
    record = []
    while(not fst(board.isTerminal())):
        if(board.turn == Board.WHITE):
            q = oldModel.predict(np.array([board.networkInput()]))
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
            record.append(sel_move)
            continue
        else:
            q = newModel.predict(np.array([board.networkInput()]))
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
            record.append(sel_move)
            continue
    terminal, winner = board.isTerminal()
    return winner

def old_vs_new(board):
    record = []
    while(not fst(board.isTerminal())):
        if(board.turn == Board.BLACK):
            q = oldModel.predict(np.array([board.networkInput()]))
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
            record.append(sel_move)
            continue
        else:
            q = newModel.predict(np.array([board.networkInput()]))
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
            record.append(sel_move)
            continue
    terminal, winner = board.isTerminal()
    return winner

newWins = 0
oldWins = 0
#a = int(input("Input old number:"))
#oldModel = keras.models.load_model('model_it'+str(a)+'.keras')
oldModel = keras.models.load_model('old_model.keras')
all = 0
for i in range(0,50):
    board = Board()
    winner = new_vs_old(board)
    if(winner == Board.WHITE):
        oldWins += 1
    if(winner == Board.BLACK):
        newWins += 1
    all += 1
    board = Board()
    winner = old_vs_new(board)
    if(winner == Board.BLACK):
        oldWins += 1
    if(winner == Board.WHITE):
        newWins += 1
    all += 1

print("Old Network vs New Network: "+str(oldWins/all) + "/"+str(newWins/all))
