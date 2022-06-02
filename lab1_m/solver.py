import time

from board import SudokuBoard
import plot as sudoku_plt


class SudokuSolver:
    def __init__(self, base_grid, k):
        self.MAX_ITER_COUNT = 500
        self.k = k

        self.base_board = SudokuBoard(base_grid)
        if not self.base_board.is_valid():
            raise ValueError("Некорректный исходный судоку!")

        self.plotter = sudoku_plt.SudokuPlot.make_board_printer(self.base_board.base)
        self.current_boards = [self.base_board, ]

    def solve(self):
        self.base_board.initialize_board()
        self.base_board.update_board_char()
        self.base_board.update_fitness()

        count = 0
        res_board = self.base_board
        prev_board = None

        while count < self.MAX_ITER_COUNT and res_board.fitness > 0 \
                and not res_board.equals(prev_board):
            self.plotter(res_board.grid)
            print("Значение эвристики: {}\n\n".format(res_board.fitness))

            # Генерация потомков текущего поколения
            tmp_all_arr = self.generate_children_boards()
            # Добавляем потомков в общий список, чтобы они конкурировали с предыдущими
            self.current_boards.extend(tmp_all_arr)

            prev_board = res_board
            # В общем полученном множестве отбираем k элементов
            new_board = self.erase_boards(prev_board)
            # Обновляем лучший вариант, если значение целевой функции оказалось меньше
            if new_board.fitness < res_board.fitness:
                res_board = new_board
            count += 1

        if count >= self.MAX_ITER_COUNT:
            raise ValueError("Невозможно решить заданный судоку")

        if not res_board.is_valid(ignore_nulls=False):
            raise ValueError("Получен некорректный судоку")

        return res_board.grid

    def generate_children_boards(self):
        tmp_all_arr = []
        for board in self.current_boards:
            tmp_all_arr.extend(board.generate_children_for_board())
        return tmp_all_arr

    def erase_boards(self, prev_board):
        self.current_boards.sort(key=lambda x: x.fitness)
        self.current_boards = self.current_boards[:self.k]

        if len(self.current_boards) == 0:
            return prev_board

        return self.current_boards[0]

    def solve_with_time(self):
        ts = time.time()
        solved_sudoku_table = self.solve()
        te = time.time()

        return solved_sudoku_table, te - ts
