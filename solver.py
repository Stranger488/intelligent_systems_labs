import time
import numpy as np
import plot as sudoku_plt
from board import SudokuBoard


# Алгоритм локального кооперативного k-лучевого поиска
class SudokuSolver:
    def __init__(self, base_sudoku, k):
        self.k = k

        self.base_board = SudokuBoard(base_sudoku)
        if not self.is_valid(self.base_board):
            raise ValueError("Invalid sudoku!")

        base_board_fitness = self.fitness_func(self.base_board, self.base_board.dim)
        self.current_els = [(base_board_fitness, self.base_board), ]

    @staticmethod
    def fitness_func(sudoku_board, min_length):
        empty_cells = 0

        for row_i in range(sudoku_board.dim):
            for col_i in range(sudoku_board.dim):
                value = sudoku_board.grid[row_i, col_i]
                if value == 0:
                    empty_cells += 1

        return empty_cells + min_length

    @staticmethod
    def get_candidate_values_for_cell(sudoku_board, row_i, col_i):
        # Варианты значений для ячейки кодируются bool-массивом
        candidate_values = np.full(sudoku_board.dim, True, dtype=bool)

        # поиск по столбцу
        for tmp_row_i in range(sudoku_board.dim):
            if tmp_row_i != row_i:
                value = sudoku_board.grid[tmp_row_i, col_i]
                if value > 0:
                    candidate_values[value - 1] = False

        # поиск по строке
        for tmp_col_i in range(sudoku_board.dim):
            if tmp_col_i != col_i:
                value = sudoku_board.grid[row_i, tmp_col_i]
                if value > 0:
                    candidate_values[value - 1] = False

        square_row_i, square_col_i = sudoku_board.get_square_i(row_i, col_i)
        # поиск по квадрату
        for tmp_row_i in range(square_row_i * sudoku_board.base, (square_row_i + 1) * sudoku_board.base):
            for tmp_col_i in range(square_col_i * sudoku_board.base, (square_col_i + 1) * sudoku_board.base):
                if tmp_row_i != row_i and tmp_col_i != col_i:
                    value = sudoku_board.grid[tmp_row_i, tmp_col_i]
                    if value > 0:
                        candidate_values[value - 1] = False

        return candidate_values

    @staticmethod
    def get_len_of_candidate_values(candidate_values):
        count = 0

        for mask in candidate_values:
            if mask:
                count += 1

        return count

    @staticmethod
    def get_most_constrained_cell(sudoku_board):
        result_row_i = 0
        result_col_i = 0

        min_length = sudoku_board.dim + 1
        min_candidates = []

        for row_i in range(sudoku_board.dim):
            for col_i in range(sudoku_board.dim):
                if sudoku_board.grid[row_i, col_i] == 0:
                    tmp_candidates = SudokuSolver.get_candidate_values_for_cell(sudoku_board, row_i, col_i)
                    tmp_len = SudokuSolver.get_len_of_candidate_values(tmp_candidates)
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

    @staticmethod
    def is_valid(sudoku_board):
        # Проверка по всем строкам
        for row_i in range(sudoku_board.dim):
            tmp_values = np.full(sudoku_board.dim, False, dtype=bool)
            for col_i in range(sudoku_board.dim):
                value = sudoku_board.grid[row_i, col_i]
                if value != 0:
                    if tmp_values[value - 1]:
                        return False
                    else:
                        tmp_values[value - 1] = True

        # Проверка по всем столбцам
        for col_i in range(sudoku_board.dim):
            tmp_values = np.full(sudoku_board.dim, False, dtype=bool)
            for row_i in range(sudoku_board.dim):
                value = sudoku_board.grid[row_i, col_i]
                if value != 0:
                    if tmp_values[value - 1]:
                        return False
                    else:
                        tmp_values[value - 1] = True

        # Проверка по всем квадратам
        for square_row_i in range(sudoku_board.base):
            for square_col_i in range(sudoku_board.base):
                tmp_values = np.full(sudoku_board.dim, False, dtype=bool)
                for row_i in range(square_row_i * sudoku_board.base, (square_row_i + 1) * sudoku_board.base):
                    for col_i in range(square_col_i * sudoku_board.base, (square_col_i + 1) * sudoku_board.base):
                        value = sudoku_board.grid[row_i, col_i]
                        if value != 0:
                            if tmp_values[value - 1]:
                                return False
                            else:
                                tmp_values[value - 1] = True

        return True

    def solve(self, steps=True):
        result = None
        is_solved = False

        while not is_solved:
            self.current_els.sort(key=lambda x: x[0])
            self.current_els = self.current_els[:self.k]

            best_el = self.current_els[0]
            best_board = best_el[1]
            best_board_fitness = best_el[0]

            if best_board_fitness == 0:
                is_solved = True
                result = self.current_els[0][1]
            else:
                if steps:
                    print("Решение на текущем этапе: ")
                    plot = sudoku_plt.SudokuPlot(best_board.grid, best_board.base)
                    plot.print_grid()
                    print("Значение эвристики: {}\n\n\n".format(best_board_fitness))

                tmp_els_lst = []
                for _, board in self.current_els:
                    best_cell_row, best_cell_col, candidates, min_length = \
                        SudokuSolver.get_most_constrained_cell(board)

                    if len(candidates) == 0 and min_length == board.dim + 1:
                        self.current_els[0] = (0, self.current_els[0][1])

                    for candidate_value in candidates:
                        tmp_board = SudokuBoard(board.grid)
                        tmp_board.grid[best_cell_row, best_cell_col] = candidate_value
                        fitness = self.fitness_func(tmp_board, min_length)

                        tmp_els_lst.append((fitness, tmp_board))
                self.current_els.extend(tmp_els_lst)

        if result is None:
            raise ValueError("Unable to solve sudoku")

        if not self.is_valid(result):
            raise ValueError("Invalid result sudoku")

        return result.grid

    def solve_with_time(self, steps=True):
        ts = time.time()
        solved_sudoku_table = self.solve(steps)
        te = time.time()

        return solved_sudoku_table, te - ts
