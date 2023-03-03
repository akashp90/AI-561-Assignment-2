import random
import math


class Node:
    children = []
    x_cord = None
    y_cord = None
    score = 0
    last_piece_placed_by = ""
    parent = None
    flat_board = []
    board = []

    def __init__(
        self, parent=None, score=0, last_piece_placed_by="", flat_board=[], board=[]
    ):
        self.parent = parent

        # Calculate the score of the board for the player who just placed the last piece
        self.score = self.calculate_score(last_piece_placed_by)
        self.last_piece_placed_by = last_piece_placed_by
        self.flat_board = flat_board
        self.board = board

    def __eq__(self, other):
        return self.x_cord == other.x_cord and self.y_cord == other.y_cord

    def __str__(self):
        if self.board is not None:
            return print_board(self.board)

    def calculate_score(self, player):
        # Get the list of all desiarable shapes
        number_stretch_twos = find_stretch_twos_count(
            self.board, self.flat_board, player
        )

        return number_stretch_twos


def find_stretch_twos_count(board, player):
    stretch_twos_count = []
    player_piece_identifier = player[0].lower()
    player_position_indexes = find(flat_board, player_piece_identifier)
    for pos in player_position_indexes:
        x, y = convert_index_to_x_y(pos)
        for i in [y - 2, y + 2]:
            for j in [x - 2, x + 2]:
                if is_location_valid(i, j) and board[i][j] == player_piece_identifier:
                    stretch_twos_count += 1

    # Divide by 2 since a stretch two can be formed both ways
    return stretch_twos_count/2


def empty_board(board, turn):
    flat_list = [item for sublist in board for item in sublist]
    if "w" in flat_list or "b" in flat_list:
        return False
    else:
        return True


def is_second_white_turn(board, turn):
    flat_list = [item for sublist in board for item in sublist]
    if flat_list.count("w") == 1 and flat_list.count("b") == 1 and turn == "WHITE":
        return True
    else:
        return False


def is_first_black_turn(board, turn):
    flat_list = [item for sublist in board for item in sublist]
    if flat_list.count("w") == 1 and flat_list.count("b") == 0 and turn == "BLACK":
        return True
    else:
        return False


def pick_inner_corner_randomly(board, check_existing=False):
    # Randomly choose one of the corners of the inner board
    # (Y, X) tuples
    inner_corners = [(6, 6), (6, 12), (12, 12), (12, 6)]
    choice = random.choice(inner_corners)

    if board[choice[0]][choice[1]] == "b" and check_existing:
        return random.choice(inner_corners)

    return choice


def is_location_valid(x, y):
    # print("Validity check for: " + str(x) + "," + str(y))
    return x >= 0 and x <= 18 and y >= 0 and y <= 18


def get_available_surrounding_locs(board, x, y):
    # Check if there is an available neighbour immediate
    surrounding_locs = []
    for i in [y - 1, y, y + 1]:
        for j in [x - 1, x, x + 1]:
            if is_location_valid(i, j) and (i, j) != (x, y) and board[i][j] == ".":
                # Send horizontal_index, vertical_index i.e. x,y
                surrounding_locs.append((j, i))

    return surrounding_locs


def value_at_of_x_y(flat_board, x, y):
    return flat_board[19 * y + x]


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def convert_index_to_x_y(index):
    # Integer part is the Y or vertical pos
    calc = math.modf(index / BOARD_SIZE)
    y = int(calc[1])
    x = round(calc[0] * BOARD_SIZE)

    return (x, y)


def get_positions_which_form_pairs(board, flat_board, turn):
    pair_list = []

    # Step 1: Get all our positions

    if turn == "BLACK":
        black_position_indexes = find(flat_board, "b")
        black_positions_x_y = [convert_index_to_x_y(c) for c in black_position_indexes]
        pieces = black_positions_x_y
    else:
        white_position_indexes = find(flat_board, "w")
        white_positions_x_y = [convert_index_to_x_y(c) for c in white_position_indexes]
        pieces = white_positions_x_y

    for piece in pieces:
        pair_forming_locations = get_available_surrounding_locs(
            board, piece[0], piece[1]
        )
        # print("Pair forming locations")
        # print(pair_forming_locations)
        pair_list = pair_list + pair_forming_locations

    return pair_list


def get_open_positions_in_range(board, flat_board, start, end, padding=0):
    # Start and end are indexes
    start_pos = convert_index_to_x_y(start)

    if end is not None:
        end_pos = convert_index_to_x_y(end)
    else:
        end_pos = (start_pos[0] + 3, start_pos[1] + 3)

    open_positions = []
    step_y = 1 if start_pos[1] < end_pos[1] else -1
    step_x = 1 if start_pos[0] < end_pos[0] else -1
    # print("Start post")
    # print(start_pos)

    # print("end_pos")
    # print(end_pos)

    # print("Range 1")
    # print(range(start_pos[1] - padding, end_pos[1] + padding, step_y))
    # print("step y")
    # print(step_y)

    # print("Range 2")
    # print(range(start_pos[0] - padding, end_pos[0] + padding, step_x))
    # print("step x")
    # print(step_x)

    for y in range(start_pos[1] - padding, end_pos[1] + padding, step_y):
        for x in range(start_pos[0] - padding, end_pos[0] + padding, step_x):
            print("Checking for (x,y) = " + str(x) + "," + str(y))
            if is_location_valid(x, y) and board[y][x] == ".":
                open_positions.append((x, y))

    return open_positions


def flatten_board(board):
    return [item for sublist in board for item in sublist]


def get_promising_moves(
    board, turn, time_remaining, num_white_captured, num_black_captured, flat_board
):
    # Step 1. Eliminate positions which will form our pair
    positions_which_form_pairs = get_positions_which_form_pairs(board, flat_board, turn)
    # print("positions_which_form_pairs")
    # print(positions_which_form_pairs)
    # print("Lenth of above: " + str(len(positions_which_form_pairs)))

    if turn == "BLACK":
        index_first = flat_board.index("b")
        if flat_board.count("b") == 1:
            index_last = None
        else:
            index_last = flat_board[::-1].index("b")

        # print("index first")
        # print(index_first)
        # print("index_last")
        # print(index_last)
    else:
        index_first = flat_board.index("w")
        if flat_board.count("w") == 1:
            index_last = None
        else:
            index_last = flat_board[::-1].index("w")

    # In early stages, try to limit your search space to only some limited
    # part of the board
    somewhat_available_positions = get_open_positions_in_range(
        board, flat_board, index_first, index_last, padding=1
    )
    # print("somewhat_available_positions")
    # print(somewhat_available_positions)
    # print("Length = "+ str(len(somewhat_available_positions)))

    promising_moves = list(
        set(somewhat_available_positions) - set(positions_which_form_pairs)
    )
    # print("promising_moves Length = " + str(len(promising_moves)))

    return promising_moves


def best_next_move(board, turn, time_remaining, num_white_captured, num_black_captured):
    if empty_board(board, turn):
        print("empty_board")
        x = 9
        y = 9
        return (y, x)
    elif is_first_black_turn(board, turn):
        print("First black")
        # Place first black in any corner
        return pick_inner_corner_randomly(board)
    elif is_second_white_turn(board, turn):
        # Place second white on any available corner
        print("Second white")
        return pick_inner_corner_randomly(board, check_existing=True)
    else:
        flat_board = flatten_board(board)
        movable_positions = get_promising_moves(
            board,
            turn,
            time_remaining,
            num_white_captured,
            num_black_captured,
            flat_board,
        )
        current_state = Node(
            parent=None,
            score=0,
            last_piece_placed_by="",
            flat_board=flat_board,
            board=board,
        )
        # print("Movable positions: ")
        # print(movable_positions)

        # print("Pick something randomly from above")

        # TODO
        # From the list of movable_positions, create nodes which represent
        # the next board if that move is taken;

        for move_position in movable_positions:
            updated_board = add_piece_at_location(board, move_position, turn)
            next_node = Node(
                parent=current_state,
                last_piece_placed_by=turn,
                flat_board=flatten_board(board),
                board=updated_board,
            )

        return random.choice(movable_positions)


file = open("some_board.txt", "r")
file_lines = file.readlines()
# Convert read bytes into ints wherever applicable
turn = file_lines[0].strip()
time_remaining = float(file_lines[1].strip())
num_white_captured, num_black_captured = file_lines[2].strip().split(",")


def map_integer_to_alphabet():
    pass


def print_board(board):
    for board_row in board:
        print(board_row)


def add_piece_at_location(board, pos, turn):
    new_board = board
    new_board[pos[1]][pos[0]] = turn[0].lower()

    return new_board


board = []
BOARD_SIZE = 19
for i in range(3, 22):
    board_row = file_lines[i].strip()
    board_row = [x for x in board_row]
    board.append(board_row)


print("Board: ")
print_board(board)

move_position = best_next_move(
    board, turn, time_remaining, num_white_captured, num_black_captured
)
print("Decide to move to ")
print(move_position)

print("New board")
print_board(add_piece_at_location(board, move_position, turn))
