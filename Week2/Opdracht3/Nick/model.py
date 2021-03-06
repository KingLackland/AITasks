import random
import itertools
import math
import numpy

MAX_DEPTH = 6
CHANCE_LIST = [[2, 0.9], [4, 0.1]]  # 90% change on 2, 10% on 4


def merge_left(b):
    # merge the board left
    # this is the function that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b


def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[0, 0, 0, 2], [0, 0, 2, 4], [0, 0, 8, 2], [4, 8, 4, 2]]
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]


# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}


def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                if x == y or x == 0 or y == 0:
                    return True
        return False

    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False


def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge function an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue


def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'


def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [(2, 4, 8, 4), (0, 2, 2, 8), (0, 0, 0, 4), (0, 0, 0, 2)]
    assert merge_down(b) == [(0, 0, 0, 4), (0, 0, 0, 8), (0, 2, 8, 4), (2, 4, 2, 2)]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [(2, 8, 4, 0), (16, 0, 2, 0), (4, 0, 0, 0), (0, 0, 0, 0)]
    assert (merge_down(b)) == [(0, 0, 0, 0), (2, 0, 0, 0), (16, 0, 4, 0), (4, 8, 2, 0)]
    assert (move_exists(b)) == True
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    # g = Game()
    # for i in range(11):
    #     g.add_two_four(b)


def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))


def get_move(board):
    h_move = None
    h_score = -math.inf
    depth = 5
    if len(get_empty_cells(board)) < 5:  # If the empty cells are more than 4 set the depth to 5 to increase performance
        depth = 6

    for direction in MERGE_FUNCTIONS.keys():
        new_board = MERGE_FUNCTIONS[direction](board)
        if board == new_board:  # Check if the direction doesn't change the board for performance boost
            continue
        score = value(new_board, depth, "MAX")
        if score > h_score:
            h_score = score
            h_move = direction
    return h_move


def value(board, depth, player):
    if depth == 0:
        if not move_exists(board):  # if depth 0 move would result in loss return -math.inf score
            return -math.inf
        return calculate_heuristic(board)
    if player == "MAX":
        return max_value(board, depth)
    else:
        return exp_value(board, depth)


def max_value(board, depth):
    v = -math.inf
    for direction in MERGE_FUNCTIONS.keys():
        new_board = MERGE_FUNCTIONS[direction](board)
        v = max(v, value(new_board, depth-1, "EXP"))
    return v


def exp_value(board, depth):
    total = 0
    amount = 0
    for cell in get_empty_cells(board):  # Check the score for every empty cell
        amount += 1
        new_board = board[:]
        x, y = cell
        for z in range(2):
            new_board[x][y] = CHANCE_LIST[z][0]
            p = CHANCE_LIST[z][1]
            total += p * value(new_board, depth-1, "MAX")
    if amount == 0:
        return value(board, depth-1, "MAX")
    return total/amount


def get_empty_cells(board):
    empty_cells = []
    for x in range(4):
        for y in range(4):
            if board[x][y] == 0:
                empty_cells.append([x, y])
    return empty_cells


def calculate_heuristic(board):  # Get the sum of all different heuristics
    heuristic = 0
    # heuristic += snake_heuristic(board)
    heuristic += top_left_heuristic(board)
    heuristic -= cluster_heuristics(board)
    return heuristic


# Snake heuristic performed worse than top_left - cluster heuristic
def snake_heuristic(b):  # Give higher score in a snake pattern starting in the top left corner
    board = numpy.array(b)
    h = numpy.array([[pow(4, 15), pow(4, 14), pow(4, 13), pow(4, 12)],
                     [pow(4, 8), pow(4, 9), pow(4, 10), pow(4, 11)],
                     [pow(4, 7), pow(4, 6), pow(4, 5), pow(4, 4)],
                     [pow(4, 0), pow(4, 1), pow(4, 2), pow(4, 3)]])
    return numpy.sum(h*board)


def top_left_heuristic(b):  # Give higher score to top left cells
    board = numpy.array(b)
    h = numpy.array([[30, 15, 5, 3],
                     [15, 5, 3, 1],
                     [5, 3, 1, 0],
                     [3, 1, 0, 0]])
    return numpy.sum(h*board)


def cluster_heuristics(board):  # Give a penalty to cells with a different value next to each other
    penalty = 0
    for x in range(4):
        for y in range(4):
            if y >= 0:  # left
                penalty = penalty + abs(board[x][y] - board[x][y-1])
            if x >= 0:  # top
                penalty = penalty + abs(board[x][y] - board[x][y-1])
            if y < 3:  # right
                penalty = penalty + abs(board[x][y] - board[x][y+1])
            if x < 3:  # bottom
                penalty = penalty + abs(board[x][y] - board[x+1][y])
    return penalty


