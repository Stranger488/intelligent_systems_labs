class SudokuPlot:
    def __init__(self, sudoku_grid_ptr, base):
        self.grid = sudoku_grid_ptr
        self.base = base

        def expand_line(line):
            # Печать левой границы, ячеек, разделенных группами, печать правой границы
            return line[0] + line[5:9].join([line[1:5] * (self.base - 1)] * self.base) + line[9:13]

        self.border_top = expand_line("╔═══╤═══╦═══╗")
        self.inner_template = expand_line("║ . │ . ║ . ║")
        self.inner_separator = expand_line("╟───┼───╫───╢")
        self.separator = expand_line("╠═══╪═══╬═══╣")
        self.border_bottom = expand_line("╚═══╧═══╩═══╝")

    def print_grid(self):
        print(self.border_top)

        for row_i in range(self.base * self.base):
            row_line = self.inner_template
            for col_i in range(self.base * self.base):
                value = self.grid[row_i, col_i]
                if value == 0:
                    row_line = row_line.replace(".", " ", 1)
                elif value < 10:
                    row_line = row_line.replace(".", str(value), 1)
                else:
                    row_line = row_line.replace(". ", str(value), 1)

            print(row_line)

            if row_i == self.base * self.base - 1:
                # последняя строка
                print(self.border_bottom)
            elif (row_i + 1) % self.base == 0:
                # последняя строка группы
                print(self.separator)
            else:
                print(self.inner_separator)
