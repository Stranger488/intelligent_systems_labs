import time
import plot as sudoku_plt
from board import SudokuBoard


# Алгоритм локального кооперативного k-лучевого поиска
class SudokuSolver:
    def __init__(self, base_sudoku, k):
        self.MAX_ITER_COUNT = 50
        self.k = k

        self.base_board = SudokuBoard(base_sudoku)
        if not self.base_board.is_valid():
            raise ValueError("Invalid sudoku!")

        self.current_boards = [self.base_board, ]

    def solve(self, steps=True):
        count = 0
        result_board = self.base_board

        while count < self.MAX_ITER_COUNT and result_board.fitness > 0:
            if steps:
                print("Решение на текущем этапе: ")
                plot = sudoku_plt.SudokuPlot(result_board.grid, result_board.base)
                plot.print_grid()
                print("Значение эвристики: {}\n\n".format(result_board.fitness))

            # Генерация k потомков текущего поколения
            self.generate_children_boards()
            # Обновляем их значения fitness и отбираем k досок
            self.erase_current_boards()

            # Генерируем из общего множества еще k потомков
            self.generate_children_boards()
            result_board = self.erase_current_boards()
            count += 1

        if result_board is None or count >= self.MAX_ITER_COUNT:
            raise ValueError("Unable to solve sudoku")

        if not result_board.is_valid():
            raise ValueError("Invalid result sudoku")

        return result_board.grid

    def erase_current_boards(self):
        self.current_boards.sort(key=lambda x: x.fitness)
        self.current_boards = self.current_boards[:self.k]

        return self.current_boards[0]

    def generate_children_boards(self):
        tmp_all_arr = []
        for board in self.current_boards:
            tmp_all_arr.extend(self.generate_children_for_board(board))
        self.current_boards.extend(tmp_all_arr)

    @staticmethod
    def generate_children_for_board(board):
        tmp_boards_lst = []
        best_cell_row, best_cell_col, candidates, min_length = \
            board.get_most_constrained_cell()

        for candidate_value in candidates:
            tmp_board = SudokuBoard(board.grid)
            tmp_board.grid[best_cell_row, best_cell_col] = candidate_value
            tmp_board.update_min_length(min_length - 1)
            tmp_board.update_fitness()

            tmp_boards_lst.append(tmp_board)

        return tmp_boards_lst

    def solve_with_time(self, steps=True):
        ts = time.time()
        solved_sudoku_table = self.solve(steps)
        te = time.time()

        return solved_sudoku_table, te - ts
