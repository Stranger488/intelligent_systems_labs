import random
from math import sqrt, inf


class SudokuBoard:
    def __init__(self, grid):
        self.grid = grid[:]
        self.base = int(sqrt(len(self.grid[0])))
        self.dim = self.base * self.base

        self.fixed = set()
        self.all_variants_arr = [[] for _ in range(self.dim)]

        self.fitness = inf

        self.most_constrained = (-1, -1)
        self.constr_res_cands = [-1 for _ in range(self.dim + 1)]
        self.constr_collisions = 82

    # Получить индексы первой ячейки квадрата, в котором находится переданная ячейка
    def get_square_i(self, row_i, col_i):
        square_row_i = row_i // self.base
        square_col_i = col_i // self.base

        return square_row_i, square_col_i

    # Проверка валидности доски (то есть проверка пересечений) (можно проверять также 0 или не проверять)
    def is_valid(self, ignore_nulls=True):
        # Проверка по всем строкам
        for row_i in range(self.dim):
            tmp_values_row = [False for _ in range(self.dim)]
            tmp_values_col = [False for _ in range(self.dim)]
            for col_i in range(self.dim):
                value = self.grid[row_i][col_i]
                if not ignore_nulls and value == 0:
                    return False

                if value != 0:
                    if tmp_values_row[value - 1]:
                        return False
                    else:
                        tmp_values_row[value - 1] = True

                value = self.grid[col_i][row_i]
                if value != 0:
                    if tmp_values_col[value - 1]:
                        return False
                    else:
                        tmp_values_col[value - 1] = True

        # Проверка по всем квадратам
        for square_row_i in range(self.base):
            for square_col_i in range(self.base):
                tmp_values = [False for _ in range(self.dim)]
                for row_i in range(square_row_i * self.base, (square_row_i + 1) * self.base):
                    for col_i in range(square_col_i * self.base, (square_col_i + 1) * self.base):
                        value = self.grid[row_i][col_i]
                        if value != 0:
                            if tmp_values[value - 1]:
                                return False
                            else:
                                tmp_values[value - 1] = True

        return True

    # Начальная инициализация доски
    def initialize_board(self):
        # Для всех 9-ти квадратов
        for i in range(self.dim):
            # Получаем массив кандидатов для текущего квадрата
            candidate_values = [True for _ in range(self.dim)]

            # Рассматриваем весь квадрат
            row_i = i // self.base
            col_i = i % self.base
            for square_row_i in range(row_i * self.base, (row_i + 1) * self.base):
                for square_col_i in range(col_i * self.base, (col_i + 1) * self.base):
                    value = self.grid[square_row_i][square_col_i]
                    # Если там уже стоит значение больше 0, то цифра недоступна для вставки
                    if value > 0:
                        candidate_values[value - 1] = False
                        self.fixed.add((square_row_i, square_col_i))

            # Массив кандидатов, если по индексу получили True, то цифра доступна для вставки
            result_candidates = self.get_result_candidates(candidate_values)
            self.generate_new_square(i, result_candidates)

    def generate_new_square(self, i, result_candidates):
        # Перемешать кандидатов
        random.shuffle(result_candidates)

        # Расставляем на место, где 0 кандидатов случайных в рамках каждого квадрата
        ind = 0
        row_i = i // self.base
        col_i = i % self.base
        for square_row_i in range(row_i * self.base, (row_i + 1) * self.base):
            for square_col_i in range(col_i * self.base, (col_i + 1) * self.base):
                value = self.grid[square_row_i][square_col_i]
                if value == 0:
                    self.grid[square_row_i][square_col_i] = result_candidates[ind]
                    ind += 1

    def update_board_char(self):
        # Рассматриваем каждую ячейку, кроме fixed
        for i in range(self.dim):
            for j in range(self.dim):
                if (i, j) not in self.fixed:
                    # result_candidates - смотрим только по fixed,
                    # collisions - число пересечений смотрим по ВСЕМ ячейкам
                    result_candidates, collisions = self.get_candidate_values_for_cell(i, j)

                    # Номер строки, номер столбца, число пересечений
                    self.all_variants_arr[self.grid[i][j] - 1].append((i, j, collisions))

                    if len(result_candidates) < len(self.constr_res_cands):
                        self.constr_collisions = collisions
                        self.most_constrained = (i, j)
                        self.constr_res_cands = result_candidates

    def update_fitness(self):
        # Выбрать все количество пересечений
        arr_ = [r[2] for el in self.all_variants_arr for r in el]

        # Складываем длину массива кандидатов для самой ограниченной ячейки и общее число пересечений для каждой ячейки
        # self.fitness = 81 - len(self.fixed) + sum(arr_)
        self.fitness = 81 - len(self.fixed)
        # self.fitness = sum(arr_)
    @staticmethod
    def get_result_candidates(candidate_values):
        return [i + 1 for i, val in enumerate(candidate_values) if val]

    def get_candidate_values_for_cell(self, row_i, col_i):
        # Варианты значений для ячейки кодируются bool-массивом
        candidate_values = [True for _ in range(self.dim)]
        collisions_for_cell = 0

        # Текущее значение в проверяемой ячейке
        val = self.grid[row_i][col_i]

        # поиск по столбцу
        for tmp_row_i in range(self.dim):
            if tmp_row_i != row_i:
                value = self.grid[tmp_row_i][col_i]
                # Исключаем кандидата, беря во внимание только fixed
                if (tmp_row_i, col_i) in self.fixed:
                    candidate_values[value - 1] = False
                # Для пересечений смотрим на все ячейки
                if value == val:
                    collisions_for_cell += 1

        # поиск по строке
        for tmp_col_i in range(self.dim):
            if tmp_col_i != col_i:
                value = self.grid[row_i][tmp_col_i]
                # Исключаем кандидата, беря во внимание только fixed
                if (row_i, tmp_col_i) in self.fixed:
                    candidate_values[value - 1] = False
                # Для пересечений смотрим на все ячейки
                if value == val:
                    collisions_for_cell += 1

        square_row_i, square_col_i = self.get_square_i(row_i, col_i)
        # поиск по квадрату
        for tmp_row_i in range(square_row_i * self.base, (square_row_i + 1) * self.base):
            for tmp_col_i in range(square_col_i * self.base, (square_col_i + 1) * self.base):
                if tmp_row_i != row_i and tmp_col_i != col_i:
                    value = self.grid[tmp_row_i][tmp_col_i]
                    # Исключаем кандидата, беря во внимание только fixed
                    if (tmp_row_i, tmp_col_i) in self.fixed:
                        candidate_values[value - 1] = False
                    # Для пересечений смотрим на все ячейки
                    if value == val:
                        collisions_for_cell += 1

        result_candidates = self.get_result_candidates(candidate_values)

        return result_candidates, collisions_for_cell

    def generate_children_for_board(self):
        tmp_boards_lst = []

        for cand in self.constr_res_cands:
            for i, j, _ in self.all_variants_arr[cand - 1]:
                tmp_board = SudokuBoard(self.grid)
                tmp_board.fixed = self.fixed.copy()

                i, j, _ = self.get_cand_idx(cand)
                tmp_board.grid[i][j] = tmp_board.grid[self.most_constrained[0]][self.most_constrained[1]]
                tmp_board.grid[self.most_constrained[0]][self.most_constrained[1]] = cand
                tmp_board.fixed.add(self.most_constrained)

                tmp_board.update_board_char()
                tmp_board.update_fitness()

                tmp_boards_lst.append(tmp_board)

        return tmp_boards_lst

    def get_cand_idx(self, val):
        self.all_variants_arr[val - 1].sort(key=lambda x: -x[2])
        return self.all_variants_arr[val - 1][0]

    def equals(self, board):
        if board is not None and self.check_grid_equals(board.grid) \
                and self.fitness == board.fitness:
            return True

        return False

    def check_grid_equals(self, grid):
        for row_i in range(self.dim):
            for col_i in range(self.dim):
                if self.grid[row_i][col_i] != grid[row_i][col_i]:
                    return False

        return True
