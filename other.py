# For the sake of calculation we take rows as alphanumeric and columns as numeric.
# Ради расчетов строки представлены как буквы, колонки как цифры
rows = "ABCDEFGHI"
columns = "123456789"
boxes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
         'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
         'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
         'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
         'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
         'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
         'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
         'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
         'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']  # каждая возможная комбинация в таблице


def grid_values(grid):
    # Take in the Unsolved Sudoku Sequence and replaces the unsolved boxes initially with all
    # possible values which can get into that cell. Lastly returns a dictionary containing the
    # values at all cell positions along with cells.
    # Берет нерешенную последовательность Судоку и заменяет нерешенные ячейки всеми возможными значениями, которые можно туда поместить
    # Возвращает словарь, содержащий значения для каждой ячейки

    values = []
    every_digits = "123456789"
    for c in grid:
        if c == ".":  # замена каждого нерешенного значения каждым возможным значением
            values.append(every_digits)
        else:  # если уже решено, то без изменений
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))  # таблицу судоку со всеми возможными значениями в ячейках


def make_combinations(m, n):
    # Принимает iterable и создает все их возможные комбинации
    # Возвращает список всех возможных комбинаций

    return [x + y for x in m for y in n]


def eliminate(values):
    #
    # Eliminate the redundant numbers from the unsolved cells if the number already appeared once
    # in the peer of the current cell.
    # What we do here is we erase that redundant number from the unsolved value cells if appeared once.

    solved_cells = [box for box in values.keys() if len(values[box]) == 1]  # cell is solved if there's only one digit
    for box in solved_cells:
        value_at_cell = values[box]  # retrieve the current value at that cell.
    for peer in peers[box]:  # check for the cell's peers if the value appears again.
        values[peer] = values[peer].replace(value_at_cell, '')
    return values  # return the modified values dictionary.


def only_choice(values):
    # If in order to satisfy the constraints of the Sudoku Puzzle there is only a single viable option
    # we fill in the Cell with that option only and thereby obtain a solve for the cell.

    for unit in all_units:  # searching across all the vicinity of the cell.
        # print(unit)
        # print("\n\n")
        # print(values)
        for digit in '123456789':
            to_be_filled = [cell for cell in unit if unit in values[unit]]
            if len(to_be_filled) == 1:  # if there exists only a single cell in the unit which is not solved
                values[to_be_filled[0]] = digit  # We fill in the cell with its proper answer.
    return values


def naked_twins(values):
    # If there are two unsolved cells in a same unit exist such that it can only be filled by only
    # two specific digits, then those two digits can be safely removed from all other cells in the same unit.

    twins_possible = [unit for unit in values.keys() if len(values[unit]) == 2]
    twins = [[unit1, unit2] for unit1 in twins_possible for unit2 in peers[unit1]
             if set(values[unit1]) == (set(values[unit2]))]  # confimed Naked Twins
    for twin in twins:
        unit1 = twin[0]
        unit2 = twin[2]
        peers1 = set(peers[unit1])
        peers2 = set(peers[unit2])
        common_peers = peers1 & peers2  # finding the intersection between the peers of the two naked twin element
        for peer in common_peers:
            if len(values[peer]) > 1:
                for value in values[unit1]:
                    values[peer] = values[peer].replace(value, '')  # Erasing the values.
    return values

def reduce_puzzle(values):
    # Applying the 4 Constraint Satisfaction Algorithms until it is not further reducible.
    # Checking if the Number of Solved Cells between the iteration.

    solved_values = [unit for unit in values.keys() if len(values[unit]) == 1]  # considering solved cells
    stuck = False  # boolean flag to determine the end of loop
    while not stuck:
        prev_solved_values = len([unit for unit in values.keys() if len(values[unit]) == 1])  # checkpoint 1
        values = eliminate(values)  # applying Elimination CSP
        values = only_choice(values)  # applying Only Choice CSP
        values = naked_twins(values)  # applying Naked Twins CSP
        after_solved_values = len([unit for unit in values.keys() if len(values[unit]) == 1])
        stuck = after_solved_values == prev_solved_values  # Getting out of loop is the number of solved cell is still the same as the previous iteration.

        if len([unit for unit in values.keys() if len(values[unit]) == 0]):
            return False  # if there's problems in the internal representation of the sudoku grid return False.
    return values  # return the reduced grid values.


def search(values):
    # 880f the sudoku grid is not further reducible by constraint satisfaction
    # a few of the cells will be left with different options and with DFS with search for the optimal
    # values for those yet-unsolved cells.

    values = reduce_puzzle(
        values)  # We call the Reduction Function to reduce the puzzle further based on the search results across iterations.
    if values is False:
        return False
    if all(len(values[b]) == 1 for b in boxes):
        print("Sudoku Problem Solved!")
        return values
    m, n = min((len(values[b]), b) for b in boxes if len(values[b]) > 1)
    for value in values[n]:
        new_sudoku = values.copy()
        new_sudoku[n] = value
        attempted = search(new_sudoku)
        if attempted:
            return attempted


def display(values):
    #
    # Display the values as a 2-D grid.
    # Input: The sudoku in dictionary form
    #
    width = 1 + max(len(values[b]) for b in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in columns))
        if r in 'CF':
            print(line)
    return


columns_reversed = columns[::-1]  # reversing the columns for calculating the Diagonal Units.

row_units = [make_combinations(r, columns) for r in rows]
column_units = [make_combinations(rows, c) for c in columns]
sub_square_units = [make_combinations(m, n) for m in ('ABC', 'DEF', 'GHI')
                    for n in ('123', '456', '789')]
diagonal_1_units = [[rows[i] + columns[i] for i in range(len(rows))]]
diagonal_2_units = [[rows[i] + columns_reversed[i] for i in range(len(rows))]]
diagonal_units = diagonal_1_units + diagonal_2_units
all_units = row_units + column_units + sub_square_units + diagonal_units
units = dict((b, [u for u in all_units if b in u]) for b in boxes)
peers = dict((b, set(sum(units[b], [])) - {b}) for b in boxes)

diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
values = grid_values(diag_sudoku_grid)
print(all_units)
print("\n\n")
print(values)
values = reduce_puzzle(values)
values = search(values)
display(values)
