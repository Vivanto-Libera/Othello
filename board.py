import numpy as np

class Board:
    EMPTY = 0
    BLACK = 1
    WHITE = -1

    directions = {'Up':(-1, 0), 'Up_Right':(-1, 1), 'Right':(0, 1), 'Down_Right':(1, 1), 'Down':(1, 0), 'Down_Left':(1, -1), 'Left':(0, -1), 'Up_Left':(-1, -1)}

    def __init__(self):
        self.board = [[self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY, self.WHITE, self.BLACK, self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY, self.BLACK, self.WHITE, self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],]
        self.turn = self.BLACK
        self.legal_move = None
        self.pass_count = 0

    def legalMoves(self):
        moves = []
        self.legal_move = 0
        for row in range(0, 8):
            for col in range(0, 8):
                if self.board[row][col] == self.EMPTY and (row, col) not in moves:
                    for (r, c) in self.directions.values():
                        new_col = col + c
                        new_row = row + r
                        if new_col in range(0, 8) and new_row in range(0, 8):
                            if self.board[new_row][new_col] == -self.turn:
                                while True:
                                    new_col += c
                                    new_row += r
                                    if new_col not in range(0, 8) or new_row not in range(0, 8):
                                        break
                                    if self.board[new_row][new_col] == self.turn:
                                        self.legal_move += 1
                                        moves.append((row, col))
                                        break
        if self.legal_move == 0:
            moves.append((-1, -1))
        return moves
    
    def applyMove(self, move):
        if move == (-1, -1):
            self.pass_count += 1
        else:
            row, col = move
            flipdirections = []
            self.board[row][col]  = self.turn
            for d, (r, c) in self.directions.items():
                new_col = col + c
                new_row = row + r
                if new_col in range(0, 8) and new_row in range(0, 8):
                    if self.board[new_row][new_col] == -self.turn:
                        while True:
                            new_col += c
                            new_row += r
                            if new_col not in range(0, 8) or new_row not in range(0, 8) or self.board[new_row][new_col] == self.EMPTY:
                                break
                            if self.board[new_row][new_col] == self.turn:
                                flipdirections.append(d)
                                break
            for d in flipdirections:
                r, c = self.directions[d]
                new_col = col + c
                new_row = row + r
                while self.board[new_row][new_col] == -self.turn:
                    self.board[new_row][new_col] = self.turn
                    new_col += c
                    new_row += r
            self.pass_count = 0
        self.legal_move = None
        self.turn = -self.turn

    def isTerminal(self):
        winner = None
        is_end = False
        if self.pass_count == 2:
            is_end = True
            black_count = 0
            white_count = 0
            for rows in self.board:
                for square in rows:
                    if square == self.BLACK:
                        black_count += 1
                    elif square == self.WHITE:
                        white_count += 1
            if black_count > white_count:
                winner = self.BLACK
            elif black_count < white_count:
                winner = self.WHITE
            else:
                winner = self.EMPTY
        return (is_end, winner)
                    
    def networkInput(self):
        playerPlane = np.zeros([8, 8])
        opponentPlane = np.zeros([8, 8])
        for row in range(0, 8):
            for col in range(0, 8):
                if self.board[row][col] == self.turn:
                    playerPlane[row][col] = 1
                elif self.board[row][col] == -self.turn:
                    opponentPlane[row][col] = 1
        moves = self.legalMoves()
        movePlane = np.zeros([8, 8])
        for (r, c) in moves:
            movePlane[r][c] = 1
        return np.stack([playerPlane, opponentPlane, movePlane], axis=2)

    def getNetworkOutputIndex(self, move):
        index = 0
        if(move != (-1, -1)):
            r, c = move
            index = r * 8 + c
        else:
            index = 64
        return index

    def printBoard(self):
        rowIndex = '87654321'
        colIndex = 'a  b  c  d  e  f  g  h'
        for row in range(0, 8):
            print()
            print(rowIndex[row], end='  ')
            for col in range(0, 8):
                if self.board[row][col] == self.EMPTY:
                    print('.', end='  ')
                elif self.board[row][col] == self.BLACK:
                    print('o', end='  ')
                else:
                    print('x', end='  ')
        print(f"\n   {colIndex}")