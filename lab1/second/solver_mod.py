import random
import time
from multiprocessing import Pool
import itertools

import numpy as np

import plot as sudoku_plt
from board_mod import SudokuBoard


# Алгоритм локального кооперативного k-лучевого поиска
class SudokuSolver:
    def __init__(self, base_sudoku):
        self.base = 3
        self.dim = 9
        self.pool_size = 4
        self.MAX_ITER_COUNT = 500
        self.k = 9

        self.base_board = SudokuBoard(base_sudoku)
        if not self.base_board.is_valid():
            raise ValueError("Некорректный исходный судоку!")

        self.candidates_arr = self.base_board.initialize_board()
        self.base_board.update_fitness()

    def solve(self, steps=True):
        count = 0
        res_board = self.base_board
        prev_board = SudokuBoard(np.full((self.base_board.dim, self.base_board.dim), -1, dtype=int))

        while count < self.MAX_ITER_COUNT and res_board.fitness > 0 \
                and not res_board.equals(prev_board):
            if steps:
                print("Решение на текущем этапе: ")
                plotter = sudoku_plt.SudokuPlot.make_board_printer(res_board.base)
                plotter(res_board.grid)
                print("Значение эвристики: {}\n\n".format(res_board.fitness))

            # Генерация k потомков текущего поколения
            tmp_all_arr = self.generate_children_boards()

            # prev_board = res_board
            # В общем полученном множестве отбираем k элементов
            new_board = self.erase_boards(tmp_all_arr, prev_board)
            if new_board.fitness < res_board.fitness:
                res_board = new_board
            count += 1

        if count >= self.MAX_ITER_COUNT:
            raise ValueError("Невозможно решить заданный судоку")

        if not res_board.is_valid(ignore_nulls=False):
            raise ValueError("Получен некорректный судоку")

        return res_board.grid

    def erase_boards(self, boards_arr, prev_board):
        # self.union_boards(boards_arr)
        boards_arr.sort(key=lambda x: x.fitness)
        boards_arr = boards_arr[:self.k]

        if len(boards_arr) == 0:
            return prev_board

        return boards_arr[0]

    @staticmethod
    def union_boards(boards_arr):
        for i, board_outer in enumerate(boards_arr):
            for j, board_inner in enumerate(boards_arr):
                if i != j:
                    if board_outer.equals(board_inner):
                        boards_arr.remove(board_inner)

    def generate_children_boards(self):
        tmp_all_arr = []

        with Pool(self.pool_size) as p:
            res = p.map(self.generate_new_states, range(self.dim))
            tmp_all_arr = [item for sublist in res for item in sublist]

        return tmp_all_arr

    def generate_new_states(self, i):
        all_permut = list(itertools.permutations(self.candidates_arr[i]))

        # all_permut = []
        # for _ in range(self.k * self.k * self.k * self.k * self.k):
        #     new_arr = self.fixed_arr[i][:]
        #     random.shuffle(new_arr)
        #     all_permut.append(new_arr)
        # all_permut = list(itertools.islice(itertools.permutations(self.fixed_arr[i]), 10000))
        # random.shuffle(self.candidates_arr[i])

        new_boards = []

        row_i = i // self.base
        col_i = i % self.base
        for permut in all_permut:
            ind = 0
            board = SudokuBoard(self.base_board.grid)
            for square_row_i in range(row_i * self.base, (row_i + 1) * self.base):
                for square_col_i in range(col_i * self.base, (col_i + 1) * self.base):
                    value = board.grid[square_row_i][square_col_i]
                    if value in permut:
                        board.grid[square_row_i][square_col_i] = permut[ind]
                        ind += 1
            board.update_fitness()
            new_boards.append(board)

        return new_boards

    def solve_with_time(self, steps=True):
        ts = time.time()
        solved_sudoku_table = self.solve(steps)
        te = time.time()

        return solved_sudoku_table, te - ts
