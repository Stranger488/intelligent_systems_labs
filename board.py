import numpy as np


class SudokuBoard:
    def __init__(self, board):
        self.grid = np.copy(board)
        self.base = int(np.sqrt(self.grid.shape[0]))
        self.dim = self.base * self.base

        self.min_length = self.dim
        self.update_min_length(self.dim)

        self.fitness = np.inf
        self.update_fitness()

    def get_square_i(self, row_i, col_i):
        square_row_i = row_i // self.base
        square_col_i = col_i // self.base

        return square_row_i, square_col_i

    def update_min_length(self, min_length):
        self.min_length = min_length

    def update_fitness(self):
        empty_cells = 0

        for row_i in range(self.dim):
            for col_i in range(self.dim):
                value = self.grid[row_i, col_i]
                if value == 0:
                    empty_cells += 1

        self.fitness = empty_cells + self.min_length

    def get_most_constrained_cell(self):
        result_row_i = 0
        result_col_i = 0

        min_length = self.dim + 1
        min_candidates = []

        for row_i in range(self.dim):
            for col_i in range(self.dim):
                if self.grid[row_i, col_i] == 0:
                    tmp_candidates = self.get_candidate_values_for_cell(row_i, col_i)
                    tmp_len = self.get_len_of_candidate_values(tmp_candidates)
                    if tmp_len < min_length:
                        min_length = tmp_len
                        min_candidates = tmp_candidates
                        result_row_i = row_i
                        result_col_i = col_i

        result_candidates = []
        for i, val in enumerate(min_candidates):
            if val:
                result_candidates.append(i + 1)

        return result_row_i, result_col_i, result_candidates, min_length

    def get_len_of_candidate_values(self, candidate_values):
        count = 0

        for mask in candidate_values:
            if mask:
                count += 1

        return count

    def get_candidate_values_for_cell(self, row_i, col_i):
        # Варианты значений для ячейки кодируются bool-массивом
        candidate_values = np.full(self.dim, True, dtype=bool)

        # поиск по столбцу
        for tmp_row_i in range(self.dim):
            if tmp_row_i != row_i:
                value = self.grid[tmp_row_i, col_i]
                if value > 0:
                    candidate_values[value - 1] = False

        # поиск по строке
        for tmp_col_i in range(self.dim):
            if tmp_col_i != col_i:
                value = self.grid[row_i, tmp_col_i]
                if value > 0:
                    candidate_values[value - 1] = False

        square_row_i, square_col_i = self.get_square_i(row_i, col_i)
        # поиск по квадрату
        for tmp_row_i in range(square_row_i * self.base, (square_row_i + 1) * self.base):
            for tmp_col_i in range(square_col_i * self.base, (square_col_i + 1) * self.base):
                if tmp_row_i != row_i and tmp_col_i != col_i:
                    value = self.grid[tmp_row_i, tmp_col_i]
                    if value > 0:
                        candidate_values[value - 1] = False

        return candidate_values

    def is_valid(self):
        # Проверка по всем строкам
        for row_i in range(self.dim):
            tmp_values_row = np.full(self.dim, False, dtype=bool)
            tmp_values_col = np.full(self.dim, False, dtype=bool)
            for col_i in range(self.dim):
                value = self.grid[row_i, col_i]
                if value != 0:
                    if tmp_values_row[value - 1]:
                        return False
                    else:
                        tmp_values_row[value - 1] = True

                value = self.grid[col_i, row_i]
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
                        value = self.grid[row_i, col_i]
                        if value != 0:
                            if tmp_values[value - 1]:
                                return False
                            else:
                                tmp_values[value - 1] = True

        return True
