from math import inf

import numpy as np
from numpy.random import default_rng

rand = default_rng()


class SudokuBoard:
    def __init__(self, grid):
        self.grid = grid.copy()
        self.base = int(np.sqrt(len(self.grid[0])))
        self.dim = self.base * self.base

        self.fitness = inf

    def update_fitness(self):
        res = 0

        # Проверка по всем строкам и столбцам
        for row_i in range(self.dim):
            tmp_values_row = [False for _ in range(self.dim)]
            tmp_values_col = [False for _ in range(self.dim)]
            for col_i in range(self.dim):
                row_val = self.grid[row_i][col_i]

                # Если значение уже просмотрено, то это означает пересечение
                if tmp_values_row[row_val - 1]:
                    res += 1
                # Отмечаем значение просмотренным
                tmp_values_row[row_val - 1] = True

                col_val = self.grid[col_i][row_i]
                if tmp_values_col[col_val - 1]:
                    res += 1
                tmp_values_col[col_val - 1] = True

        # Проверка по всем квадратам
        # for square_row_i in range(self.base):
        #     for square_col_i in range(self.base):
        #         tmp_values = np.full(self.dim, False, dtype=bool)
        #         for row_i in range(square_row_i * self.base, (square_row_i + 1) * self.base):
        #             for col_i in range(square_col_i * self.base, (square_col_i + 1) * self.base):
        #                 value = self.grid[row_i][col_i]
        #
        #                 if tmp_values[value - 1]:
        #                     res += 1
        #                 tmp_values[value - 1] = True

        self.fitness = res
        return res

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

    def initialize_board(self):
        cand = []

        for i in range(self.dim):
            # Получаем массив кандидатов для текущего квадрата
            candidate_values = [True for _ in range(self.dim)]

            row_i = i // self.base
            col_i = i % self.base
            for square_row_i in range(row_i * self.base, (row_i + 1) * self.base):
                for square_col_i in range(col_i * self.base, (col_i + 1) * self.base):
                    value = self.grid[square_row_i][square_col_i]
                    if value > 0:
                        candidate_values[value - 1] = False

            result_candidates = [i + 1 for i, val in enumerate(candidate_values) if val]
            cand.append(result_candidates)

            self.generate_new_square(i, result_candidates)

        return cand

    def generate_new_square(self, i, result_candidates):
        rand.shuffle(result_candidates)

        ind = 0
        row_i = i // self.base
        col_i = i % self.base
        for square_row_i in range(row_i * self.base, (row_i + 1) * self.base):
            for square_col_i in range(col_i * self.base, (col_i + 1) * self.base):
                value = self.grid[square_row_i][square_col_i]
                if value in result_candidates or value == 0:
                    self.grid[square_row_i][square_col_i] = result_candidates[ind]
                    ind += 1
