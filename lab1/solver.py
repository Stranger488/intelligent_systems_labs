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
        prev_board = SudokuBoard(np.full((self.base_board.dim, self.base_board.dim), -1, dtype=int))

        while count < self.MAX_ITER_COUNT and res_board.fitness > 0 \
                and not res_board.equals(prev_board):
            if steps:
                print("Решение на текущем этапе: ")
                plotter = sudoku_plt.SudokuPlot.make_board_printer(res_board.base)
                plotter(res_board.grid)
                print("Значение эвристики: {}\n\n".format(res_board.fitness))

            # Генерация k потомков текущего поколения
            tmp_all_arr = self.generate_children_boards(self.current_boards)
            # Обновляем их значения fitness и отбираем k досок
            tmp_all_arr, _ = self.erase_boards(tmp_all_arr)

            # Генерируем из полученного поколения еще k потомков
            next_tmp_all_arr = self.generate_children_boards(tmp_all_arr)
            tmp_all_arr.extend(next_tmp_all_arr)

            prev_board = res_board
            # В общем полученном множестве отбираем k элементов
            self.current_boards, res_board = self.erase_boards(tmp_all_arr)
            count += 1

        if count >= self.MAX_ITER_COUNT:
            raise ValueError("Невозможно решить заданный судоку")

        if not res_board.is_valid(ignore_nulls=False):
            raise ValueError("Получен некорректный судоку")

        return res_board.grid

    def erase_boards(self, boards_arr):
        self.union_boards(boards_arr)
        boards_arr.sort(key=lambda x: x.fitness)
        boards_arr = boards_arr[:self.k]

        return boards_arr, boards_arr[0]

    @staticmethod
    def union_boards(boards_arr):
        for i, board_outer in enumerate(boards_arr):
            for j, board_inner in enumerate(boards_arr):
                if i != j:
                    if board_outer.equals(board_inner):
                        boards_arr.remove(board_inner)

    @staticmethod
    def generate_children_boards(boards_arr):
        tmp_all_arr = []
        for board in boards_arr:
            tmp_all_arr.extend(board.generate_children_for_board())
        return tmp_all_arr

    def solve_with_time(self, steps=True):
        ts = time.time()
        solved_sudoku_table = self.solve(steps)
        te = time.time()

        return solved_sudoku_table, te - ts
