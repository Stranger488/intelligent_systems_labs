import argparse
import numpy as np

import solver as sudoku_solver

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
    [2, 0, 4,   0, 0, 8,    0, 0, 0]
], dtype=int)


def main(k=20):
    # print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)

    solver = sudoku_solver.SudokuSolver(sudoku_table, k)

    print("Заданная судоку таблица: ")
    solver.plotter(sudoku_table)

    solved_sudoku_table, time_estimated = solver.solve_with_time()

    print("Решенная судоку таблица: ")
    solver.plotter(solved_sudoku_table)

    print("Время решения: {} секунд".format(time_estimated))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--k', action='store', type=int,
                            help='Параметр k алгоритма')
    arguments = arg_parser.parse_args()

    main(arguments.k)
