import time

import numpy as np

import plot as sudoku_plt
from board import SudokuBoard


# Алгоритм локального кооперативного k-лучевого поиска
class SudokuSolver:
    def __init__(self, base_sudoku, k):
        self.MAX_ITER_COUNT = 500
        self.k = k

        self.base_board = SudokuBoard(base_sudoku)
        if not self.base_board.is_valid():
            raise ValueError("Некорректный исходный судоку!")

        self.current_boards = [self.base_board, ]

    def solve(self, steps=True):
        count = 0
        res_board = self.base_board
        prev_board = SudokuBoard(np.full((self.base_board.dim, self.base_board.dim), 0, dtype=int))

        while count < self.MAX_ITER_COUNT and res_board.fitness > 0 \
                and not res_board.equals(prev_board):
            if steps:
                print("Решение на текущем этапе: ")
                plotter = sudoku_plt.SudokuPlot.make_board_printer(res_board.base)
                plotter(res_board.grid)
                print("Значение эвристики: {}\n\n".format(res_board.fitness))

            # Генерация k потомков текущего поколения
            self.generate_children_boards()
            # Обновляем их значения fitness и отбираем k досок
            self.erase_current_boards()

            # Генерируем из общего множества еще k потомков
            self.generate_children_boards()
            prev_board = res_board
            res_board = self.erase_current_boards()
            count += 1

        if res_board is None or count >= self.MAX_ITER_COUNT:
            raise ValueError("Невозможно решить заданный судоку")

        if not res_board.is_valid(ignore_nulls=False):
            raise ValueError("Получен некорректный судоку")

        return res_board.grid

    def erase_current_boards(self):
        self.union_boards()
        self.current_boards.sort(key=lambda x: x.fitness)
        self.current_boards = self.current_boards[:self.k]

        return self.current_boards[0]

    def union_boards(self):
        for i, board_outer in enumerate(self.current_boards):
            for j, board_inner in enumerate(self.current_boards):
                if i != j:
                    if board_outer.equals(board_inner):
                        self.current_boards.remove(board_inner)

    def generate_children_boards(self):
        tmp_all_arr = []
        for board in self.current_boards:
            tmp_all_arr.extend(board.generate_children_for_board())
        self.current_boards.extend(tmp_all_arr)

    def solve_with_time(self, steps=True):
        ts = time.time()
        solved_sudoku_table = self.solve(steps)
        te = time.time()

        return solved_sudoku_table, te - ts
