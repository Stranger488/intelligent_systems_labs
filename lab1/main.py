import numpy as np

import plot as sudoku_plot
import solver_k as sudoku_solver

# Экстремальный судоку, вариант №7
sudoku_table = np.array([
    # [0, 8, 0,   0, 0, 0,    0, 0, 1],
    # [1, 0, 0,   0, 0, 0,    3, 9, 0],
    # [5, 0, 0,   0, 0, 0,    0, 0, 0],
    #
    # [0, 6, 0,   0, 0, 0,    0, 3, 2],
    # [0, 3, 0,   0, 5, 9,    0, 0, 0],
    # [0, 0, 0,   0, 0, 7,    9, 6, 0],
    #
    # [0, 0, 0,   0, 9, 0,    4, 0, 7],
    # [0, 0, 0,   0, 1, 3,    0, 8, 0],
    # [2, 0, 4,   0, 0, 8,    0, 0, 0]

    [0, 8, 0, 9, 6, 0, 0, 0, 1],
    [1, 0, 0, 0, 8, 0, 3, 9, 0],
    [5, 0, 0, 1, 0, 0, 8, 0, 0],

    [0, 6, 0, 8, 0, 0, 0, 3, 2],
    [0, 3, 0, 0, 5, 9, 0, 0, 0],
    [0, 0, 0, 0, 0, 7, 9, 6, 0],

    [3, 1, 0, 2, 9, 0, 4, 0, 7],
    [0, 0, 0, 4, 1, 3, 0, 8, 0],
    [2, 0, 4, 0, 0, 8, 0, 0, 0]
], dtype=int)


def main():
    solver = sudoku_solver.SudokuSolver(sudoku_table)
    plotter = sudoku_plot.SudokuPlot.make_board_printer(solver.base_board.base)

    print("Заданная судоку таблица: ")
    plotter(sudoku_table)

    solved_sudoku_table, time_estimated = solver.solve_with_time()

    print("Решенная судоку таблица: ")
    plotter(solved_sudoku_table)

    print("Время решения: {} секунд".format(time_estimated))


if __name__ == "__main__":
    main()
