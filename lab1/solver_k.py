import random
import time
from functools import partial
from multiprocessing import Pool

import numpy as np

import plot as sudoku_plt


# Алгоритм локального кооперативного k-лучевого поиска
from lab1.board_k import SudokuBoard


class SudokuSolver:
    def __init__(self, base_sudoku):
        self.base = 3
        self.dim = 9

        self.pool_size = 4
        self.MAX_ITER_COUNT = 500
        self.k = 400
        self.generations_size = 100

        self.base_board = SudokuBoard(base_sudoku)
        if not self.base_board.is_valid():
            raise ValueError("Некорректный исходный судоку!")

        self.current_boards = []

        self.fixed_arr = self.initialize_board(self.base_board)

    def k_func(self, iter_num):
        return self.k + iter_num

    def initialize_board(self, board):
        fixed = set([])

        for i in range(board.dim):
            for j in range(board.dim):
                if board.grid[i][j] != 0:
                    fixed.add((i, j))

        self.fixed_arr = fixed

        for i in range(self.k):
            new_board = self.generate_board(self.base_board)
            self.current_boards.append(new_board)

        return fixed

    def generate_board(self, board):
        new_board = SudokuBoard(board.grid)
        choices = [list(filter(lambda y: y not in x, range(1, board.dim + 1)))
                   for x in board.grid
                   ]

        for i in range(board.dim):
            for j in range(board.dim):
                if (i, j) not in self.fixed_arr:
                    index = random.randint(0, len(choices[i]) - 1)
                    new_board.grid[i][j] = choices[i][index]
                    del choices[i][index]

        new_board.update_fitness()

        return new_board

    def generate_successor(self, board):
        choices = list(map(lambda x: list(filter(lambda y: (x[0], y) not in self.fixed_arr, x[1])),
                           enumerate([list(range(board.dim)) for x in range(board.dim)])))

        row = random.randint(0, board.dim - 1)
        index1 = random.randint(0, len(choices[row]) - 1)
        choice1 = choices[row][index1]
        del choices[row][index1]
        index2 = random.randint(0, len(choices[row]) - 1)
        choice2 = choices[row][index2]
        del choices[row][index2]

        ret = SudokuBoard(board.grid)
        ret.grid[row][choice2], ret.grid[row][choice1] = ret.grid[row][choice1], ret.grid[row][choice2]
        ret.update_fitness()

        return ret

    def solve(self, steps=True):
        count = 0
        res_board = self.base_board

        while count < self.MAX_ITER_COUNT and res_board.fitness > 0:
            self.current_boards.sort(key=lambda x: x.fitness)
            self.current_boards = self.current_boards[:self.generations_size]
            res_board = self.current_boards[0]

            if steps:
                print("Решение на текущем этапе: ")
                sudoku_plt.SudokuPlot.make_board_printer(res_board.base)(res_board.grid)
                print("Значение эвристики: {}\n\n".format(res_board.fitness))

            with Pool(self.pool_size) as p:
                func = partial(self.thread_func, count)
                res = p.map(func, range(self.generations_size))
                successors = [item for sublist in res for item in sublist]
            self.current_boards.extend(successors)
            count += 1

        if count >= self.MAX_ITER_COUNT:
            raise ValueError("Невозможно решить заданный судоку")

        if not res_board.is_valid(ignore_nulls=False):
            raise ValueError("Получен некорректный судоку")

        return res_board.grid

    def thread_func(self, count, i):
        successors = []
        for _ in range(self.k_func(count)):
            successors.append(self.generate_successor(self.current_boards[i]))
        return successors

    def solve_with_time(self, steps=True):
        ts = time.time()
        solved_sudoku_table = self.solve(steps)
        te = time.time()

        return solved_sudoku_table, te - ts
