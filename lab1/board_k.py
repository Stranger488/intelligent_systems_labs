from math import inf

import numpy as np
from numpy.random import default_rng

rand = default_rng()


class SudokuBoard:
    def __init__(self, grid):
        self.grid = self.deepcopy_board(grid)
        self.base = int(np.sqrt(len(self.grid[0])))
        self.dim = self.base * self.base

        self.fitness = inf

    def deepcopy_board(self, board):
        ret = []
        for row in board:
            ret_row = []
            for elem in row:
                ret_row.append(elem)
            ret.append(ret_row)
        return ret

    def update_fitness(self):
        collisions = 0
        # run collision check for each cell
        for i in range(self.dim):
            for j in range(self.dim):
                val = self.grid[i][j]
                # check row for collisions
                for n in range(self.dim):
                    if n != i and self.grid[n][j] == val:
                        collisions += 1

                # check column for collisions
                for m in range(self.dim):
                    if m != j and self.grid[i][m] == val:
                        collisions += 1

                # check block for collisions
                squareX = j // self.base
                squareY = i // self.base
                for n in range(self.base):
                    for m in range(self.base):
                        if not (self.base * squareX + m == j or self.base * squareY + n == i) and \
                                self.grid[self.base * squareY + n][self.base * squareX + m] == val:
                            collisions += 1
        self.fitness = collisions

    def is_valid(self, ignore_nulls=True):
        # Проверка по всем строкам
        for row_i in range(self.dim):
            tmp_values_row = [False for _ in range(self.dim)]
            tmp_values_col = [False for _ in range(self.dim)]
            for col_i in range(self.dim):
                value = self.grid[row_i][col_i]
                if not ignore_nulls and value == 0:
                    return False

                if value != 0:
                    if tmp_values_row[value - 1]:
                        return False
                    else:
                        tmp_values_row[value - 1] = True

                value = self.grid[col_i][row_i]
                if value != 0:
                    if tmp_values_col[value - 1]:
                        return False
                    else:
                        tmp_values_col[value - 1] = True

        # Проверка по всем квадратам
        for square_row_i in range(self.base):
            for square_col_i in range(self.base):
                tmp_values = np.full(self.dim, False, dtype=bool)
                for row_i in range(square_row_i * self.base, (square_row_i + 1) * self.base):
                    for col_i in range(square_col_i * self.base, (square_col_i + 1) * self.base):
                        value = self.grid[row_i][col_i]
                        if value != 0:
                            if tmp_values[value - 1]:
                                return False
                            else:
                                tmp_values[value - 1] = True

        return True

    def equals(self, board):
        if self.check_grid_equals(board.grid) \
                and self.fitness == board.fitness:
            return True

        return False

    def check_grid_equals(self, grid):
        for row_i in range(self.dim):
            for col_i in range(self.dim):
                if self.grid[row_i][col_i] != grid[row_i][col_i]:
                    return False

        return True
