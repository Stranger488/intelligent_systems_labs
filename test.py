from functools import reduce
from random import randint
from math import sqrt

GENERATION_SIZE = 300
BRANCHING_FACTOR = 60

def heuristic(board, gridsize=4, blocksize=2):
    collisions = 0
    # run collision check for each cell
    for i in range(gridsize):
        for j in range(gridsize):
            val = board[i][j]
            # check row for collisions
            for n in range(gridsize):
                if n != i and board[n][j] == val:
                    collisions += 1

            # check column for collisions
            for m in range(gridsize):
                if m != j and board[i][m] == val:
                    collisions += 1

            # check block for collisions
            squareX = j // blocksize
            squareY = i // blocksize
            for n in range(blocksize):
                for m in range(blocksize):
                    if not (blocksize * squareX + m == j or blocksize * squareY + n == i) and board[blocksize * squareY + n][blocksize * squareX + m] == val:
                        collisions += 1
    return collisions


def deepcopy_board(board):
    ret = []
    for row in board:
        ret_row = []
        for elem in row:
            ret_row.append(elem)
        ret.append(ret_row)
    return ret


def generate_successor(board, size, fixed):
    choices = list(map(lambda x: list(filter(lambda y: (x[0], y) not in fixed, x[1])),
        enumerate([list(range(size)) for x in range(size)])))

    row = randint(0,size-1)
    index1 = randint(0, len(choices[row])-1)
    choice1 = choices[row][index1]
    del choices[row][index1]
    index2 = randint(0, len(choices[row])-1)
    choice2 = choices[row][index2]
    del choices[row][index2]
    ret = deepcopy_board(board)
    ret[row][choice2], ret[row][choice1] = ret[row][choice1], ret[row][choice2]
    return ret


def generate_board(original_board, size, fixed):
    board = deepcopy_board(original_board)
    choices = [list(filter(lambda y: y not in x, range(1, size+1)))
        for x in original_board
    ]

    for i in range(size):
        for j in range(size):
            if (i,j) not in fixed:
                index = randint(0, len(choices[i])-1)
                board[i][j] = choices[i][index]
                del choices[i][index]

    return board


def solver(original_board = [
        # [0, 0, 8, 2, 0, 0, 0, 0, 1],
        # [0, 0, 7, 0, 0, 0, 4, 0, 0],
        # [0, 3, 0, 5, 0, 0, 0, 8, 7],
        # [0, 0, 5, 4, 0, 1, 8, 0, 0],
        # [9, 0, 0, 0, 0, 0, 0, 0, 4],
        # [3, 0, 0, 7, 0, 8, 0, 0, 9],
        # [0, 9, 0, 6, 0, 0, 0, 1, 8],
        # [0, 0, 3, 0, 0, 0, 5, 0, 0],
        # [1, 0, 2, 9, 0, 0, 0, 0, 0]

        [0, 8, 0,   0, 0, 0,    0, 0, 1],
        [1, 0, 0,   0, 0, 0,    3, 9, 0],
        [5, 0, 0,   0, 0, 0,    0, 0, 0],

        [0, 6, 0,   0, 0, 0,    0, 3, 2],
        [0, 3, 0,   0, 5, 9,    0, 0, 0],
        [0, 0, 0,   0, 0, 7,    9, 6, 0],

        [0, 0, 0,   0, 9, 0,    4, 0, 7],
        [0, 0, 0,   0, 1, 3,    0, 8, 0],
        [2, 0, 4,   0, 0, 8,    0, 0, 0]

        # [1, 0, 3, 0],
        # [0, 0, 0, 0],
        # [2, 0, 4, 0],
        # [0, 0, 0, 0]
    ], size=9):

    fixed_values = set([])

    for i in range(size):
        for j in range(size):
            if original_board[i][j] != 0:
                fixed_values.add((i, j))

    solved = False
    solution = None
    boards = []
    # generate initial set
    for i in range(GENERATION_SIZE):
        board = generate_board(original_board, size, fixed_values)
        boards.append(board)
    ## reset boards list to take both heuristics and states
    boards = [(heuristic(board, gridsize=size, blocksize=int(sqrt(size))), board) for board in boards]

    while not solved:
        # order by heuristic value of boards
        boards.sort(key=lambda x: x[0])
        # take top 10 (lower heuristic values)
        boards = boards[:GENERATION_SIZE]
        # check first board
        if boards[0][0] == 0:
            # if heuristic is 0, set solved to true and set as solution
            solved = True
            solution = boards[0][1]
        else:
            # else, generate successors and loop
            ## generate successor boards
            successors = []
            for board in boards:
                print("Heuristic score: %d" % board[0])
                print(reduce(lambda accumulator, x: accumulator + "\n" + str(x), board[1], ""))
                for i in range(BRANCHING_FACTOR):
                    successors.append(generate_successor(board[1], size, fixed_values))
            ## add each successor to current list with heuristic value
            for s in successors:
                boards.append((heuristic(s, gridsize=size, blocksize=int(sqrt(size))), s))

    return solution

if __name__ == "__main__":
    print(reduce(lambda accumulator, x: accumulator + "\n" + str(x), solver(), ""))