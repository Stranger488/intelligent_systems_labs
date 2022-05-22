import numpy as np
import time

import solver as sudoku_solver
import plot as sudoku_plot


# Экстремальный судоку, вариант №7
sudoku_table = np.array([
    [0, 8, 0,   0, 0, 0,    0, 0, 1],
    [1, 0, 0,   0, 0, 0,    3, 9, 0],
    [5, 0, 0,   0, 0, 0,    0, 0, 0],

    [0, 6, 0,   0, 0, 0,    0, 3, 2],
    [0, 3, 0,   0, 5, 9,    0, 0, 0],
    [0, 0, 0,   0, 0, 7,    9, 6, 0],

    [0, 0, 0,   0, 9, 0,    4, 0, 7],
    [0, 0, 0,   0, 1, 3,    0, 8, 0],
    [2, 0, 4,   0, 0, 8,    0, 0, 0],
], dtype=int)

# Ширина поиска
k = 20


def main():
    solver = sudoku_solver.SudokuSolver(sudoku_table, k)
    plot = sudoku_plot.SudokuPlot(sudoku_table, solver.base_board.base)

    print("Заданная судоку таблица: \n")
    plot.print_grid()

    solved_sudoku_table, time_estimated = solver.solve_with_time()

    print("Решенная судоку таблица: \n")
    plot.grid = solved_sudoku_table
    plot.print_grid()

    print("Время решения: {} секунд".format(time_estimated))


if __name__ == "__main__":
    main()
