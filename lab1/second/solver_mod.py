import random
import time
from multiprocessing import Pool
import itertools
from functools import partial

import numpy as np

import plot as sudoku_plt
from board_mod import SudokuBoard


# Алгоритм локального кооперативного k-лучевого поиска
class SudokuSolver:
    def __init__(self, base_sudoku):
        self.base = 3
        self.dim = 9
        self.pool_size = 4
        self.MAX_ITER_COUNT = 1000
        self.k = 10

        self.base_board = SudokuBoard(base_sudoku)
        if not self.base_board.is_valid():
            raise ValueError("Некорректный исходный судоку!")

        self.candidates_arr = self.base_board.initialize_board()
        self.base_board.update_fitness()

        self.perm_all = [[] for _ in range(self.dim)]
        self.boards_all = [self.base_board, ]

    def gen_all_permut_for_block(self, i):
        return list(itertools.permutations(self.candidates_arr[i]))

    def gen_permut_for_block(self, i):
        return list(itertools.islice(itertools.permutations(self.candidates_arr[i]), 1000))

    def solve(self, steps=True):
        count = 0
        res_board = self.base_board
        prev_board = SudokuBoard(np.full((self.base_board.dim, self.base_board.dim), -1, dtype=int))

        # with Pool(self.pool_size) as p:
        #     self.perm_all = p.map(self.gen_all_permut_for_block, range(self.dim))

        for i in range(self.dim):
            self.perm_all[i] = self.gen_permut_for_block(i)

        while count < self.MAX_ITER_COUNT and res_board.fitness > 0:
            if steps:
                print("Решение на текущем этапе: ")
                plotter = sudoku_plt.SudokuPlot.make_board_printer(res_board.base)
                plotter(res_board.grid)
                print("Значение эвристики: {}\n\n".format(res_board.fitness))

            # Генерация потомков текущего поколения
            self.boards_all.extend(self.generate_new_boards())

            # prev_board = res_board
            # В общем полученном множестве отбираем k элементов
            new_board = self.erase_boards(prev_board)
            if new_board.fitness < res_board.fitness:
                res_board = new_board
            count += 1

        if count >= self.MAX_ITER_COUNT:
            raise ValueError("Невозможно решить заданный судоку")

        if not res_board.is_valid(ignore_nulls=False):
            raise ValueError("Получен некорректный судоку")

        return res_board.grid

    def erase_boards(self, prev_board):
        # self.union_boards(boards_arr)
        self.boards_all.sort(key=lambda x: x.fitness)
        self.boards_all = self.boards_all[:self.k]

        if len(self.boards_all) == 0:
            return prev_board

        return self.boards_all[0]

    @staticmethod
    def union_boards(boards_arr):
        for i, board_outer in enumerate(boards_arr):
            for j, board_inner in enumerate(boards_arr):
                if i != j:
                    if board_outer.equals(board_inner):
                        boards_arr.remove(board_inner)

    def generate_new_boards(self):
        res_all = []

        # with Pool(self.pool_size) as p:
        #     res_all = p.map(self.thread_func, range(len(self.boards_all)))
        #     rr = [item for sublist in res_all for item in sublist]

        for board_ind, board in enumerate(self.boards_all):
            for i in range(self.dim):
                res_all.extend(self.thread_func(board_ind))
                # with Pool(self.pool_size) as p:
                #     func = partial(self.generate_new_board, board, i)
                #     res = p.map(func, range(len(self.perm_all[i])))
                #     res_all.extend(res)

        return res_all

    def thread_func(self, board_ind):
        r = []
        for i in range(self.dim):
            for j, perm in enumerate(self.perm_all[i]):
                r.append(self.generate_new_board(self.boards_all[board_ind], i, j))
        return r

    def generate_new_board(self, board, ind, j):
        cur_perm = self.perm_all[ind][j]

        row_i = ind // self.base
        col_i = ind % self.base

        index = 0
        board = SudokuBoard(board.grid)
        for square_row_i in range(row_i * self.base, (row_i + 1) * self.base):
            for square_col_i in range(col_i * self.base, (col_i + 1) * self.base):
                value = board.grid[square_row_i][square_col_i]
                if value in cur_perm:
                    board.grid[square_row_i][square_col_i] = cur_perm[index]
                    index += 1
        board.update_fitness()

        return board

    def solve_with_time(self, steps=True):
        ts = time.time()
        solved_sudoku_table = self.solve(steps)
        te = time.time()

        return solved_sudoku_table, te - ts
