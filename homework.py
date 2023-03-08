import random
import math
import copy
import itertools


class Node:
    children = []
    x_cord = None
    y_cord = None
    score = 0
    last_piece_placed_by = ""
    parent = None
    flat_board = []
    board = []
    children = []
    depth_level = 0
    best_child = None
    value = 0
    alpha = 0
    beta = 0
    is_terminal = None
    num_black_captured = 0
    num_white_captured = 0

    def __eq__(self, other):
        return self.calculate_score() == other.calculate_score()

    def __hash__(self):
        return hash(("score", self.score))

    def __init__(
        self,
        parent=None,
        score=0,
        last_piece_placed_by="",
        flat_board=[],
        board=[],
        last_piece_placed_location=(),
        depth_level=0,
        best_child=None,
        is_terminal=None,
        num_white_captured=0,
        num_black_captured=0
    ):
        self.depth_level = depth_level
        self.parent = parent
        self.last_piece_placed_location = last_piece_placed_location
        self.num_white_captured = num_white_captured
        self.num_black_captured = num_black_captured

        # Calculate the score of the board for the player who just placed the last piece
        self.flat_board = flat_board
        self.board = board

        if last_piece_placed_by == "":
            white_count = flat_board.count("w")
            black_count = flat_board.count("b")

            self.last_piece_placed_by = (
                "BLACK" if white_count < black_count else "WHITE"
            )
        else:
            self.last_piece_placed_by = last_piece_placed_by

        # self.score = self.calculate_score(main_turn)
        # self.opponent_score = self.calculate_score(get_opposite_player(self.last_piece_placed_by))

    def __eq__(self, other):
        if isinstance(self, str) or isinstance(other, str):
            return False

        return self.x_cord == other.x_cord and self.y_cord == other.y_cord

    def __str__(self):
        if self.board is not None:
            return print_board(self.board)

    def calculate_score(self):
        self.player_score = self.calculate_score_for_player(main_turn)
        self.opponent_score = self.calculate_score_for_player(
            get_opposite_player(main_turn)
        )

        self.score = self.player_score - self.opponent_score
        return self.score

    def calculate_score_for_player(self, player):
        # Get the list of all desiarable shapes

        number_winning_pente = find_winning_pente_count(
            self.board, self.flat_board, player
        )
        if number_winning_pente > 0:
            # 5 in a row, terminal state
            self.is_terminal = True


        number_closed_pente = find_closed_pente_count(
            self.board, self.flat_board, player
        )

        number_stretch_twos = find_stretch_twos_count(
            self.board, self.flat_board, player
        )

        CAPTURE_SCORE = 0
        if (
            len(self.last_piece_placed_by) > 0
            and len(self.last_piece_placed_location) > 0
        ):
            opposite_piece_captured_bool, self.board = opposite_piece_captured(
                self.board,
                self.flat_board,
                player,
                self.last_piece_placed_by,
                self.last_piece_placed_location
            )

            if opposite_piece_captured_bool:
                print("Idhar?")
                print(player)
                if self.last_piece_placed_by == 'WHITE':
                    # Black piece captured;
                    self.num_black_captured += 2
                    CAPTURE_SCORE = self.num_black_captured * 250
                    print("Should not increment")
                    print(self.num_black_captured)
                    print_board(self.board)
                else:
                    # White pieces captured
                    self.num_white_captured += 2
                    CAPTURE_SCORE = self.num_white_captured * 250
                    print("Incrementing")
                

                # print("Capture score")
                # print(CAPTURE_SCORE)

        if player == "WHITE":
            if num_black_captured == 10:
                # If white player captures 10, game over
                CAPTURE_SCORE = 100000
                self.is_terminal = True
            else:
                CAPTURE_SCORE = self.num_black_captured * 250 - self.num_white_captured
        else:
            if num_white_captured == 10:
                # If black player captures 10, game over
                CAPTURE_SCORE = 100000
                self.is_terminal = True
            else:
                CAPTURE_SCORE = self.num_white_captured * 250 - self.num_black_captured

        number_of_open_triads = find_open_triads_count(
            self.board, self.flat_board, player
        )
        

        number_of_open_quads = find_open_quad_count(self.board, self.flat_board, player)

        number_of_open_pente = find_open_pente_count(
            self.board, self.flat_board, player
        )


        number_of_pairs = find_pairs_count(self.board, self.flat_board, player)
        RISKY_PAIRS_SCORE = 1 * number_of_pairs

        
        WIN_SCORE = number_winning_pente * 100000
        OPEN_PENTE_SCORE = 10000 * number_of_open_pente
        OPEN_QUADS_SCORE = number_of_open_quads * 500
        OPEN_TRIADS_SCORE = number_of_open_triads * 100
        STRETCH_TWO_SCORE = 2 * number_stretch_twos
        CLOSED_PENTE_SCORE = number_closed_pente * 20000

        calc_score = (
            STRETCH_TWO_SCORE
            + RISKY_PAIRS_SCORE
            + CAPTURE_SCORE
            + OPEN_TRIADS_SCORE
            + OPEN_QUADS_SCORE
            + OPEN_PENTE_SCORE
            + WIN_SCORE
            + CLOSED_PENTE_SCORE
        )
        # print("Score: ")
        # print(calc_score)
        # if CAPTURE_SCORE > 0:
        #     print("For node")
        #     print_node(self)
        #     print("Captured Score: " + str(CAPTURE_SCORE))
        #     print("Full score: " + str(calc_score))
        #     pass

        return calc_score


def get_opposite_player_identifier(player):
    if player == "BLACK" or player == "b":
        return "w"
    elif player == "WHITE" or player == "w":
        return "b"


def get_opposite_player(player):
    if player == "BLACK" or player == "b":
        return "WHITE"
    elif player == "WHITE" or player == "w":
        return "BLACK"


def opposite_piece_captured(
    board, flat_board, player_unused, last_piece_placed_by, last_piece_placed_location
):
    captures_count = 0
    player = last_piece_placed_by[0].lower()
    opponent = get_opposite_player_identifier(player)
    col, row = last_piece_placed_location
    # Horizontal captures
    if col >= 2 and col <= 16:
        if (
            board[row][col - 1] == opponent
            and board[row][col - 2] == opponent
            and board[row][col - 3] == player
        ):
            board = remove_captured_pieces(board, row, col-1)
            board = remove_captured_pieces(board, row, col-2)
            return True, board
        if (
            col <= 14
            and board[row][col + 1] == opponent
            and board[row][col + 2] == opponent
            and board[row][col + 3] == player
        ):
            board = remove_captured_pieces(board, row, col+1)
            board = remove_captured_pieces(board, row, col+2)
            return True, board

    # Vertical captures
    if row >= 2 and row <= 16:
        if (
            board[row - 1][col] == opponent
            and board[row - 2][col] == opponent
            and board[row - 3][col] == player
        ):
            board = remove_captured_pieces(board, row-1, col)
            board = remove_captured_pieces(board, row-2, col)
            return True, board
        if (
            row <= 14
            and board[row + 1][col] == opponent
            and board[row + 2][col] == opponent
            and board[row + 3][col] == player
        ):
            board = remove_captured_pieces(board, row+1, col)
            board = remove_captured_pieces(board, row+2, col)
            return True, board

    # Check diagonal captures (NW-SE)
    if row >= 3 and row <= 15 and col >= 3 and col <= 15:
        if (
            board[row - 1][col - 1] == opponent
            and board[row - 2][col - 2] == opponent
            and board[row - 3][col - 3] == player
        ):
            board = remove_captured_pieces(board, row-1, col-1)
            board = remove_captured_pieces(board, row-1, col-2)
            return True, board

        if (
            row <= 14
            and col <= 14
            and board[row + 1][col + 1] == opponent
            and board[row + 2][col + 2] == opponent
            and board[row + 3][col + 3] == player
        ):
            board = remove_captured_pieces(board, row+1, col+1)
            board = remove_captured_pieces(board, row+2, col+2)
            return True, board

    # Check diagonal captures (SW-NE)
    if row >= 3 and row <= 15 and col >= 3 and col <= 15:
        if (
            board[row - 1][col + 1] == opponent
            and board[row - 2][col + 2] == opponent
            and board[row - 3][col + 3] == player
        ):
            board = remove_captured_pieces(board, row+1, col-1)
            board = remove_captured_pieces(board, row+2, col-2)
            return True, board
        if (
            row <= 14
            and col >= 2
            and board[row + 1][col - 1] == opponent
            and board[row + 2][col - 2] == opponent
            and board[row + 3][col - 3] == player
        ):
            board = remove_captured_pieces(board, row+1, col-1)
            board = remove_captured_pieces(board, row+2, col-2)
            return True, board

    return False, board


def find_pairs_count(board, flat_board, player):
    pair_list = []
    player_piece_identifier = player[0].lower()
    player_position_indexes = find(flat_board, player_piece_identifier)
    player_position_cordinates = [
        convert_index_to_x_y(c) for c in player_position_indexes
    ]

    for piece in player_position_cordinates:
        x, y = piece
        for ver in [y - 1, y, y + 1]:
            for hor in [x - 1, x, x + 1]:
                if (
                    is_location_valid(hor, ver)
                    and (hor, ver) != (x, y)
                    and board[ver][hor] == player_piece_identifier
                ):
                    # Send horizontal_index, vertical_index i.e. x,y
                    pair_list.append((x, y, hor, ver))

    return len(set(pair_list))


def find_winning_pente_count(board, flat_board, player):
    pente_count = 0
    pente = []
    player = player[0].lower()
    player_position_indexes = find(flat_board, player)

    player_position_cordinates = [
        convert_index_to_x_y(c) for c in player_position_indexes
    ]
    # print("Checking for board")
    # print_board(board)

    # TODO: CHeck the border conditions
    for pos in player_position_cordinates:
        # Horizontal
        col, row = pos
        if col >= 2 and col <= 16:
            if (
                board[row][col - 1] == player
                and board[row][col - 2] == player
                and board[row][col - 3] == player
                and board[row][col - 4] == player
            ):
                pente_count += 1
            if (
                col <= 14
                and board[row][col + 1] == player
                and board[row][col + 2] == player
                and board[row][col + 3] == player
                and board[row][col + 4] == player
            ):
                pente_count += 1

        # Vertical captures
        if row >= 2 and row <= 16:
            if (
                board[row - 1][col] == player
                and board[row - 2][col] == player
                and board[row - 3][col] == player
                and board[row - 4][col] == player
            ):
                pente_count += 1
            if (
                row <= 14
                and board[row + 1][col] == player
                and board[row + 2][col] == player
                and board[row + 3][col] == player
                and board[row + 4][col] == player
            ):
                pente_count += 1

        # Check diagonal captures (NW-SE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col - 1] == player
                and board[row - 2][col - 2] == player
                and board[row - 3][col - 3] == player
                and board[row - 4][col - 4] == player
            ):
                pente_count += 1
            if (
                row <= 14
                and col <= 14
                and board[row + 1][col + 1] == player
                and board[row + 2][col + 2] == player
                and board[row + 3][col + 3] == player
                and board[row + 4][col + 4] == player
            ):
                pente_count += 1

        # Check diagonal captures (SW-NE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col + 1] == player
                and board[row - 2][col + 2] == player
                and board[row - 3][col + 3] == player
                and board[row - 4][col + 4] == player
            ):
                pente_count += 1
            if (
                row <= 14
                and col >= 2
                and board[row + 1][col - 1] == player
                and board[row + 2][col - 2] == player
                and board[row + 3][col - 3] == player
                and board[row + 4][col - 4] == player
            ):
                pente_count += 1

    # print("triads count: ")
    # print(triads_count)
    return pente_count


def find_open_pente_count(board, flat_board, player):
    pente_count = 0
    pente = []
    player = player[0].lower()
    player_position_indexes = find(flat_board, player)

    player_position_cordinates = [
        convert_index_to_x_y(c) for c in player_position_indexes
    ]
    # print("Checking for board")
    # print_board(board)

    # TODO: CHeck the border conditions
    for pos in player_position_cordinates:
        # Horizontal
        col, row = pos
        if col >= 2 and col <= 16:
            if (
                board[row][col - 1] == player
                and board[row][col - 2] == player
                and board[row][col - 3] == player
                and board[row][col - 4] == "."
            ):
                pente_count += 1
            if (
                col <= 14
                and board[row][col + 1] == player
                and board[row][col + 2] == player
                and board[row][col + 3] == player
                and board[row][col + 4] == "."
            ):
                pente_count += 1

        # Vertical captures
        if row >= 2 and row <= 16:
            if (
                board[row - 1][col] == player
                and board[row - 2][col] == player
                and board[row - 3][col] == player
                and board[row - 4][col] == "."
            ):
                pente_count += 1
            if (
                row <= 14
                and board[row + 1][col] == player
                and board[row + 2][col] == player
                and board[row + 3][col] == player
                and board[row + 4][col] == "."
            ):
                pente_count += 1

        # Check diagonal captures (NW-SE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col - 1] == player
                and board[row - 2][col - 2] == player
                and board[row - 3][col - 3] == player
                and board[row - 4][col - 4] == "."
            ):
                pente_count += 1
            if (
                row <= 14
                and col <= 14
                and board[row + 1][col + 1] == player
                and board[row + 2][col + 2] == player
                and board[row + 3][col + 3] == player
                and board[row + 4][col + 4] == "."
            ):
                pente_count += 1

        # Check diagonal captures (SW-NE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col + 1] == player
                and board[row - 2][col + 2] == player
                and board[row - 3][col + 3] == player
                and board[row - 4][col + 4] == "."
            ):
                pente_count += 1
            if (
                row <= 14
                and col >= 2
                and board[row + 1][col - 1] == player
                and board[row + 2][col - 2] == player
                and board[row + 3][col - 3] == player
                and board[row + 4][col - 4] == "."
            ):
                pente_count += 1

    # print("triads count: ")
    # print(triads_count)
    return pente_count


def find_closed_pente_count(board, flat_board, player):
    pente_count = 0
    pente = []
    player = player[0].lower()
    player_position_indexes = find(flat_board, player)

    player_position_cordinates = [
        convert_index_to_x_y(c) for c in player_position_indexes
    ]
    # print("Checking for board")
    # print_board(board)

    # TODO: CHeck the border conditions
    for pos in player_position_cordinates:
        # Horizontal
        col, row = pos
        if col >= 2 and col <= 16:
            if (
                board[row][col - 1] == player
                and board[row][col - 2] == "."
                and board[row][col - 3] == player
                and board[row][col - 4] == player
            ):
                pente_count += 1
            if (
                col <= 14
                and board[row][col + 1] == player
                and board[row][col + 2] == "."
                and board[row][col + 3] == player
                and board[row][col + 4] == player
            ):
                pente_count += 1

        # Vertical captures
        if row >= 2 and row <= 16:
            if (
                board[row - 1][col] == player
                and board[row - 2][col] == "."
                and board[row - 3][col] == player
                and board[row - 4][col] == player
            ):
                pente_count += 1
            if (
                row <= 14
                and board[row + 1][col] == player
                and board[row + 2][col] == "."
                and board[row + 3][col] == player
                and board[row + 4][col] == player
            ):
                pente_count += 1

        # Check diagonal captures (NW-SE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col - 1] == player
                and board[row - 2][col - 2] == "."
                and board[row - 3][col - 3] == player
                and board[row - 4][col - 4] == player
            ):
                pente_count += 1
            if (
                row <= 14
                and col <= 14
                and board[row + 1][col + 1] == player
                and board[row + 2][col + 2] == "."
                and board[row + 3][col + 3] == player
                and board[row + 4][col + 4] == player
            ):
                pente_count += 1

        # Check diagonal captures (SW-NE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col + 1] == player
                and board[row - 2][col + 2] == "."
                and board[row - 3][col + 3] == player
                and board[row - 4][col + 4] == player
            ):
                pente_count += 1
            if (
                row <= 14
                and col >= 2
                and board[row + 1][col - 1] == player
                and board[row + 2][col - 2] == "."
                and board[row + 3][col - 3] == player
                and board[row + 4][col - 4] == player
            ):
                pente_count += 1

    return pente_count


def find_open_quad_count(board, flat_board, player):
    quads_count = 0
    quads = []
    player = player[0].lower()
    player_position_indexes = find(flat_board, player)

    player_position_cordinates = [
        convert_index_to_x_y(c) for c in player_position_indexes
    ]
    # print("Checking for board")
    # print_board(board)

    for pos in player_position_cordinates:
        # Horizontal
        col, row = pos
        # if (col, row) == (10, 6):
        #     print("Detect")
        #     print(board[row][col + 1])
        #     print(board[row][col + 2])
        #     print(board[row][col + 3])
        #     print("Cond")
        #     print(board[row][col + 1] == player)

        #     print()

        if col >= 2 and col <= 16:
            if (
                board[row][col - 1] == player
                and board[row][col - 2] == player
                and board[row][col - 3] == player
                and board[row][col - 4] == "."
            ):
                quads_count += 1
            if (
                col <= 14
                and board[row][col + 1] == player
                and board[row][col + 2] == player
                and board[row][col + 3] == player
                and board[row][col + 4] == "."
            ):
                quads_count += 1

        # Vertical captures
        if row >= 2 and row <= 16:
            if (
                board[row - 1][col] == player
                and board[row - 2][col] == player
                and board[row - 3][col] == player
                and board[row - 4][col] == "."
            ):
                quads_count += 1
            if (
                row <= 14
                and board[row + 1][col] == player
                and board[row + 2][col] == player
                and board[row + 3][col] == player
                and board[row + 4][col] == "."
            ):
                quads_count += 1

        # Check diagonal captures (NW-SE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col - 1] == player
                and board[row - 2][col - 2] == player
                and board[row - 3][col - 3] == player
                and board[row - 4][col - 4] == "."
            ):
                quads_count += 1
            if (
                row <= 14
                and col <= 14
                and board[row + 1][col + 1] == player
                and board[row + 2][col + 2] == player
                and board[row + 3][col + 3] == player
                and board[row + 4][col + 4] == "."
            ):
                quads_count += 1

        # Check diagonal captures (SW-NE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col + 1] == player
                and board[row - 2][col + 2] == player
                and board[row - 3][col + 3] == player
                and board[row - 4][col + 4] == "."
            ):
                quads_count += 1
            if (
                row <= 14
                and col >= 2
                and board[row + 1][col - 1] == player
                and board[row + 2][col - 2] == player
                and board[row + 3][col - 3] == player
                and board[row + 4][col - 4] == "."
            ):
                quads_count += 1

    # print("triads count: ")
    # print(triads_count)
    return quads_count


def find_open_triads_count(board, flat_board, player):
    triads_count = 0
    triads = []
    player = player[0].lower()
    player_position_indexes = find(flat_board, player)

    player_position_cordinates = [
        convert_index_to_x_y(c) for c in player_position_indexes
    ]
    # print("Checking for board")
    # print_board(board)

    for pos in player_position_cordinates:
        # Horizontal
        col, row = pos
        # if (col, row) == (10, 6):
        #     print("Detect")
        #     print(board[row][col + 1])
        #     print(board[row][col + 2])
        #     print(board[row][col + 3])
        #     print("Cond")
        #     print(board[row][col + 1] == player)

        #     print()

        if col >= 2 and col <= 16:
            if (
                board[row][col - 1] == player
                and board[row][col - 2] == player
                and board[row][col - 3] == "."
            ):
                triads_count += 1
            if (
                col <= 14
                and board[row][col + 1] == player
                and board[row][col + 2] == player
                and board[row][col + 3] == "."
            ):
                triads_count += 1

        # Vertical captures
        if row >= 2 and row <= 16:
            if (
                board[row - 1][col] == player
                and board[row - 2][col] == player
                and board[row - 3][col] == "."
            ):
                triads_count += 1
            if (
                row <= 14
                and board[row + 1][col] == player
                and board[row + 2][col] == player
                and board[row + 3][col] == "."
            ):
                triads_count += 1

        # Check diagonal captures (NW-SE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col - 1] == player
                and board[row - 2][col - 2] == player
                and board[row - 3][col - 3] == "."
            ):
                triads_count += 1
            if (
                row <= 14
                and col <= 14
                and board[row + 1][col + 1] == player
                and board[row + 2][col + 2] == player
                and board[row + 3][col + 3] == "."
            ):
                triads_count += 1

        # Check diagonal captures (SW-NE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col + 1] == player
                and board[row - 2][col + 2] == player
                and board[row - 3][col + 3] == "."
            ):
                triads_count += 1
            if (
                row <= 14
                and col >= 2
                and board[row + 1][col - 1] == player
                and board[row + 2][col - 2] == player
                and board[row + 3][col - 3] == "."
            ):
                triads_count += 1

    # print("triads count: ")
    # print(triads_count)
    return triads_count


def find_stretch_twos_count(board, flat_board, player):
    stretch_twos = []
    player_piece_identifier = player[0].lower()
    player_position_indexes = find(flat_board, player_piece_identifier)
    for pos in player_position_indexes:
        x, y = convert_index_to_x_y(pos)
        # print("Looking at piece at x, y")
        # print(str(x) + "," + str(y))
        for ver in [y - 2, y, y + 2]:
            for hor in [x - 2, x, x + 2]:
                if (
                    is_location_valid(hor, ver)
                    and board[ver][hor] == player_piece_identifier
                    and (hor, ver) != (x, y)
                ):
                    # print("Found a stretch 2")
                    # print("board[" + str(ver) +"][" + str(hor) + "]")
                    # print(board[ver][hor])
                    stretch_twos.append((x, y, hor, ver))

    # Divide by 2 since a stretch two can be formed both ways
    return len(set(stretch_twos))


def empty_board(board, turn):
    flat_list = [item for sublist in board for item in sublist]
    if "w" in flat_list or "b" in flat_list:
        return False
    else:
        return True


def is_second_white_turn(board, turn):
    flat_list = [item for sublist in board for item in sublist]

    if flat_list.count("w") == 1 and flat_list.count("b") == 1:
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


def get_surrounding_locs(board, x, y, player):
    surrounding_locs = []
    player_piece_identifier = player[0].lower()
    # print("surrounding_locs for x, y" + str(x) + "," + str(y))
    for ver in [y - 1, y, y + 1]:
        for hor in [x - 1, x, x + 1]:
            if (
                is_location_valid(hor, ver)
                and (hor, ver) != (x, y)
                and board[ver][hor] == player_piece_identifier
            ):
                # Send horizontal_index, vertical_index i.e. x,y
                surrounding_locs.append((hor, ver))

    # print(surrounding_locs)
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


def convert_x_y_to_index(location):
    x, y = location
    return y * BOARD_SIZE + y


def get_positions_in_range(board, flat_board, start, padding=5):
    # Start and end are indexes
    start_x, start_y = convert_index_to_x_y(start)

    open_positions = []

    for y in range(max(start_y - padding, 0), min(start_y + padding, 19)):
        for x in range(max(start_x - padding, 0), min(start_x + padding, 19)):
            # print("Checking for (x,y) = " + str(x) + "," + str(y))
            if is_location_valid(x, y) and board[y][x] == ".":
                # print("Yep")
                open_positions.append((x, y))
            else:
                # print("Nope")
                pass

    return open_positions


def flatten_board(board):
    return [item for sublist in board for item in sublist]


def find_first_last_indexes(flat_board, player):
    player_piece_identifier = player[0].lower()
    index_first = flat_board.index(player_piece_identifier)
    if flat_board.count(player_piece_identifier) == 1:
        index_last = None
    else:
        index_last = flat_board[::-1].index(player_piece_identifier)

    return (index_first, index_last)


def get_average_x_y_for_player(board, player_piece_identifier):
    count = 0
    x_count = 0
    y_count = 0
    for row in range(0, 19):
        for col in range(0, 19):
            if board[row][col] == player_piece_identifier:
                count += 1
                x_count += col
                y_count += row

    if count == 0:
        return (9, 9)

    return (int(x_count / count), int(y_count / count))


def get_next_nodes_for_node(node, turn, time_remaining):
    board = node.board
    if empty_board(board, turn):
        print("empty_board")
        x = 9
        y = 9
        # Convert these to nodes with the wanted move with a high score
        # to ensure these get picked
        updated_board = add_piece_at_location(board, (9, 9), turn)
        first_move_node = Node(
            parent=Node,
            last_piece_placed_by=turn,
            flat_board=flatten_board(updated_board),
            board=updated_board,
            last_piece_placed_location=(9, 9),
            depth_level=node.depth_level + 1,
            score=100000,
        )
        print("IDhar toh aara")
        return [first_move_node]
    elif is_first_black_turn(board, turn):
        print("First black")
        # Place first black in any corner
        random_inner_corner = pick_inner_corner_randomly(board)
        updated_board = add_piece_at_location(board, random_inner_corner, turn)
        first_move_node = Node(
            parent=Node,
            last_piece_placed_by=turn,
            flat_board=flatten_board(updated_board),
            board=updated_board,
            last_piece_placed_location=random_inner_corner,
            depth_level=node.depth_level + 1,
            is_terminal=True,
            score=100000,
        )
        return [first_move_node]
    elif is_second_white_turn(board, turn):
        # Place second white on any available corner
        print("Second whiteee")
        random_inner_corner = pick_inner_corner_randomly(board, check_existing=True)
        updated_board = add_piece_at_location(board, random_inner_corner, turn)
        first_move_node = Node(
            parent=Node,
            last_piece_placed_by=turn,
            flat_board=flatten_board(updated_board),
            board=updated_board,
            last_piece_placed_location=random_inner_corner,
            depth_level=node.depth_level + 1,
            is_terminal=True,
            score=100000,
        )
        return [first_move_node]
    else:
        # if node.last_piece_placed_location:
        #     center_search_space = convert_x_y_to_index(node.last_piece_placed_location)
        # else:
        #     center_search_space = convert_x_y_to_index((9, 9))

        average_position = get_average_x_y_for_player(board, turn[0].lower())
        average_position = convert_x_y_to_index(average_position)

        search_space = get_positions_in_range(
            board, node.flat_board, average_position, padding=15
        )
        # print("search_space: ")
        # print(search_space)

        updated_board = []
        next_nodes = []
        best_score_yet = 0
        for move_position in search_space:
            updated_board = add_piece_at_location(board, move_position, turn)
            next_node = Node(
                parent=node,
                last_piece_placed_by=turn,
                flat_board=flatten_board(updated_board),
                board=updated_board,
                last_piece_placed_location=move_position,
                depth_level=node.depth_level + 1,
                num_white_captured=node.num_white_captured,
                num_black_captured=node.num_black_captured
            )
            next_nodes.append(next_node)

        return next_nodes


def partition_list(l, delimiter):
    return [list(y) for x, y in itertools.groupby(l, lambda z: z == delimiter) if not x]


def get_best_move_for_node(
    node, depth, alpha, beta, maximising_player, max_node=None, min_node=None
):
    interesting_node = False
    if node.last_piece_placed_location == (8, 6):
        interesting_node = True
        print("At interesting node")
        print_node(node)

    # MiniMax with alpha beta pruning
    if maximising_player:
        turn = main_turn
    else:
        turn = get_opposite_player(main_turn)

    if depth == 0 or node.is_terminal:
        return (node.calculate_score(), node)

    children_nodes = get_next_nodes_for_node(node, turn, 0)
    node_score = lambda node_1: node_1.calculate_score()
    children_nodes.sort(key=node_score, reverse=True)
    children_nodes = list(set(children_nodes))
    node.children = children_nodes

    #print("Node position: " + str(node.last_piece_placed_location))
    #print("Score: " + str(node.calculate_score()))
    # print("Children")
    # for c in children_nodes:
    #     print(c.calculate_score())

    if maximising_player:
        # maxEva = -float('inf')
        maxEva = children_nodes[0].calculate_score()
        for child in children_nodes:
            val, n = get_best_move_for_node(
                child, depth - 1, alpha, beta, False, max_node, min_node
            )
            # print("Value returned = :" + str(val))
            if val > maxEva:
                #print("Updating maxEva to " + str(val))
                maxEva = val
                max_node = n

            if maxEva > alpha:
                #print("Updating alpha to " + str(val))
                alpha = maxEva
                max_node = n

            if beta <= alpha:
                #print("Pruned at max")
                break

        # if max_node is not None:
        #     # print("Returning max: ")
        #     # print(maxEva)
        #     # print(max_node.calculate_score())
        #     # print("alpha")
        #     # print(alpha)

        return maxEva, max_node
    else:
        # minEva = float('inf')
        minEva = children_nodes[0].calculate_score()
        for child in children_nodes:
            val, n = get_best_move_for_node(
                child, depth - 1, alpha, beta, True, max_node, min_node
            )
            # print("Value returned = :" + str(val))
            if val < minEva:
                #print("Updating minEva to " + str(val))
                minEva = val
                min_node = n

            if minEva < beta:
                #print("Updating beta to " + str(minEva))
                beta = minEva
                min_node = n

            if beta <= alpha:
                #print("Pruned at min")
                break

        return minEva, min_node


def get_next_move(board, turn, time_remaining, num_white_captured, num_black_captured):
    if empty_board(board, turn):
        return (9, 9)
    elif is_first_black_turn(board, turn):
        return pick_inner_corner_randomly(board)
    elif is_second_white_turn(board, turn):
        # Place second white on any available corner
        return pick_inner_corner_randomly(board, check_existing=True)
    else:
        root_node = Node(
            parent=None,
            score=0,
            last_piece_placed_by=get_opposite_player(main_turn),
            flat_board=flatten_board(board),
            board=board,
            depth_level=0,
            num_black_captured=num_black_captured,
            num_white_captured=num_white_captured
        )

        print("Trying to run minimax with alpha beta")
        # Run it with False :)
        val, s = get_best_move_for_node(
            root_node, 3, -float("inf"), float("inf"), True, None, None
        )
        
        node = s
        #print("printing nodess")        
        while 1:
            if s.depth_level == 1:
                break
            
            s = s.parent

        root = s.parent
        #print("Printing children of root")
        #for c in root.children:
            #print_node(c)
            
        #print("Depth of node")
        #print(s.depth_level)
        #print("Node:")
        #print_node(s)

        return s.last_piece_placed_location


file = open("some_board.txt", "r")
file_lines = file.readlines()
# Convert read bytes into ints wherever applicable
turn = file_lines[0].strip()
main_turn = turn
time_remaining = float(file_lines[1].strip())
num_black_captured, num_white_captured = file_lines[2].strip().split(",")
num_black_captured = int(num_black_captured)
num_white_captured = int(num_white_captured)
print("Num black and white")
print(num_black_captured)
print(num_white_captured)

def map_x_y_to_board_coordinates(pos):
    x, y = pos
    chars = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
    ]

    coordinates = str(19 - (y + 1)) + chars[x]
    return coordinates


def print_board(board, as_strings=True):
    for board_row in board:
        if as_strings:
            print("".join(board_row))
        else:
            print(board_row)


def print_node(node):
    print_board(node.board)
    print("Last piece placed by: " + node.last_piece_placed_by)
    print("Last piece placed at location: " + str(node.last_piece_placed_location))
    print("Children length: " + str(len(node.children)))
    print("Depth level: " + str(node.depth_level))
    print("Score of player: " + str(node.player_score))
    print("Score of opponenet: " + str(node.opponent_score))
    print("num_white_captured:" + str(node.num_white_captured))
    print("num_black_captured: " + str(node.num_black_captured))


def print_nodes(nodes):
    for node in nodes:
        print_node(node)
        print("*******")


def add_piece_at_location(board, pos, turn, highlight_last=False):
    new_board = copy.deepcopy(board)
    new_board[pos[1]][pos[0]] = turn[0].lower()
    if highlight_last:
        new_board[pos[1]][pos[0]] = turn[0].upper()

    return new_board

def remove_captured_pieces(board, y, x):
    # print("Removing at")
    # print(str(x) + "," + str(y))
    new_board = copy.deepcopy(board)
    new_board[y][x] = '.'

    return new_board


board = []
BOARD_SIZE = 19
for i in range(3, 22):
    board_row = file_lines[i].strip()
    board_row = [x for x in board_row]
    board.append(board_row)


print("Board: ")
print_board(board)

move_position = get_next_move(
    board, turn, time_remaining, num_white_captured, num_black_captured
)
print("Decide to move to ")
print(move_position)
print(map_x_y_to_board_coordinates(move_position))

print("Board after move: ")
print_board(add_piece_at_location(board, move_position, main_turn, highlight_last=True))