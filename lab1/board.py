from math import inf

import numpy as np


class SudokuBoard:
    def __init__(self, grid):
        self.grid = grid.copy()
        self.base = int(np.sqrt(len(self.grid[0])))
        self.dim = self.base * self.base

        self.min_length = self.dim

        self.fitness = inf
        self.update_fitness()

        self.best_cell_row, self.best_cell_col, self.cur_candidates, self.min_length = self.get_most_constrained_cell()

    def get_square_i(self, row_i, col_i):
        square_row_i = row_i // self.base
        square_col_i = col_i // self.base

        return square_row_i, square_col_i

    def update_fitness(self):
        empty_cells = 0

        for row_i in range(self.dim):
            for col_i in range(self.dim):
                value = self.grid[row_i][col_i]
                if value == 0:
                    empty_cells += 1

        self.fitness = empty_cells + self.min_length

    def get_most_constrained_cell(self):
        result_row_i = -1
        result_col_i = -1

        min_length = self.dim + 1
        min_candidates = []

        for row_i in range(self.dim):
            for col_i in range(self.dim):
                if self.grid[row_i][col_i] == 0:
                    tmp_candidates = self.get_candidate_values_for_cell(row_i, col_i)
                    tmp_len = self.get_len_of_candidate_values(tmp_candidates)
                    if tmp_len < min_length:
                        min_length = tmp_len
                        min_candidates = tmp_candidates
                        result_row_i = row_i
                        result_col_i = col_i

        if min_length == self.dim + 1:
            min_length = 0

        result_candidates = []
        for i, val in enumerate(min_candidates):
            if val:
                result_candidates.append(i + 1)

        return result_row_i, result_col_i, result_candidates, min_length

    @staticmethod
    def get_len_of_candidate_values(candidate_values):
        count = 0

        for mask in candidate_values:
            if mask:
                count += 1

        return count

    def get_candidate_values_for_cell(self, row_i, col_i):
        # Варианты значений для ячейки кодируются bool-массивом
        candidate_values = [True for _ in range(self.dim)]

        # поиск по столбцу
        for tmp_row_i in range(self.dim):
            if tmp_row_i != row_i:
                value = self.grid[tmp_row_i][col_i]
                if value > 0:
                    candidate_values[value - 1] = False

        # поиск по строке
        for tmp_col_i in range(self.dim):
            if tmp_col_i != col_i:
                value = self.grid[row_i][tmp_col_i]
                if value > 0:
                    candidate_values[value - 1] = False

        square_row_i, square_col_i = self.get_square_i(row_i, col_i)
        # поиск по квадрату
        for tmp_row_i in range(square_row_i * self.base, (square_row_i + 1) * self.base):
            for tmp_col_i in range(square_col_i * self.base, (square_col_i + 1) * self.base):
                if tmp_row_i != row_i and tmp_col_i != col_i:
                    value = self.grid[tmp_row_i][tmp_col_i]
                    if value > 0:
                        candidate_values[value - 1] = False

        return candidate_values

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

    def generate_children_for_board(self):
        tmp_boards_lst = []

        for candidate_value in self.cur_candidates:
            tmp_board = SudokuBoard(self.grid)
            tmp_board.grid[self.best_cell_row][self.best_cell_col] = candidate_value
            tmp_board.best_cell_row, tmp_board.best_cell_col, tmp_board.cur_candidates, tmp_board.min_length \
                = tmp_board.get_most_constrained_cell()
            tmp_board.update_fitness()

            tmp_boards_lst.append(tmp_board)

        return tmp_boards_lst

    def equals(self, board):
        if self.check_grid_equals(board.grid) \
                and self.check_cur_cand(board.cur_candidates) \
                and self.min_length == board.min_length \
                and self.fitness == board.fitness \
                and self.best_cell_row == board.best_cell_row \
                and self.best_cell_col == board.best_cell_col:
            return True

        return False

    def check_grid_equals(self, grid):
        for row_i in range(self.dim):
            for col_i in range(self.dim):
                if self.grid[row_i][col_i] != grid[row_i][col_i]:
                    return False

        return True

    def check_cur_cand(self, cur_candidates):
        return set(self.cur_candidates) == set(cur_candidates)
