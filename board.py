class Board:
    EMPTY = 0
    BLACK = 1
    WHITE = -1

    directions = {'Up':(1, 0), 'Up_Right':(1, 1), 'Right':(0, 1), 'Down_Right':(-1, 1), 'Down':(-1, 0), 'Down_Left':(-1, -1), 'Left':(0, -1), 'Up_Left':(1, -1)}

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

    def legalMoves(self):
        moves = []
        self.legal_move = 0
        for col in range(0, 7):
            for row in range(0, 7):
                if self.board[col][row] == self.EMPTY:
                    for (c, r) in self.directions.values:
                        new_col = col + c
                        new_row = row + r
                        if new_col in range(0, 7) and new_row in range(0, 7):
                            if self.board[new_col][new_row] == -self.turn:
                                while True:
                                    new_col += 1
                                    new_row += 1
                                    if new_col not in range(0, 7) or new_row not in range(0, 7):
                                        break
                                    if self.board[new_col][new_row] == self.turn:
                                        self.legal_move += 1
                                        moves.append((new_col, new_row))
                                        break
        return moves







              