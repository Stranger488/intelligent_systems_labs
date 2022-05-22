import numpy as np


class SudokuBoard:
    def __init__(self, board):
        self.grid = np.copy(board)
        self.base = int(np.sqrt(self.grid.shape[0]))
        self.dim = self.base * self.base

    def get_square_i(self, row_i, col_i):
        square_row_i = row_i // self.base
        square_col_i = col_i // self.base

        return square_row_i, square_col_i
