from homework import find

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
            return True
        if (
            col <= 14
            and board[row][col + 1] == opponent
            and board[row][col + 2] == opponent
            and board[row][col + 3] == player
        ):
            return True

    # Vertical captures
    if row >= 2 and row <= 16:
        if (
            board[row - 1][col] == opponent
            and board[row - 2][col] == opponent
            and board[row - 3][col] == player
        ):
            return True
        if (
            row <= 14
            and board[row + 1][col] == opponent
            and board[row + 2][col] == opponent
            and board[row + 3][col] == player
        ):
            return True

    # Check diagonal captures (NW-SE)
    if row >= 3 and row <= 15 and col >= 3 and col <= 15:
        if (
            board[row - 1][col - 1] == opponent
            and board[row - 2][col - 2] == opponent
            and board[row - 3][col - 3] == player
        ):
            return True
        if (
            row <= 14
            and col <= 14
            and board[row + 1][col + 1] == opponent
            and board[row + 2][col + 2] == opponent
            and board[row + 3][col + 3] == player
        ):
            return True

    # Check diagonal captures (SW-NE)
    if row >= 3 and row <= 15 and col >= 3 and col <= 15:
        if (
            board[row - 1][col + 1] == opponent
            and board[row - 2][col + 2] == opponent
            and board[row - 3][col + 3] == player
        ):
            return True
        if (
            row <= 14
            and col >= 2
            and board[row + 1][col - 1] == opponent
            and board[row + 2][col - 2] == opponent
            and board[row + 3][col - 3] == player
        ):
            return True

    return False


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
                and board[row][col - 4] == player
                and board[row][col - 5] == "."
            ):
                pente_count += 1
            if (
                col <= 14
                and board[row][col + 1] == player
                and board[row][col + 2] == player
                and board[row][col + 3] == player
                and board[row][col + 4] == player
                and board[row][col + 5] == "."
            ):
                pente_count += 1

        # Vertical captures
        if row >= 2 and row <= 16:
            if (
                board[row - 1][col] == player
                and board[row - 2][col] == player
                and board[row - 3][col] == player
                and board[row - 4][col] == player
                and board[row - 5][col] == "."
            ):
                pente_count += 1
            if (
                row <= 14
                and board[row + 1][col] == player
                and board[row + 2][col] == player
                and board[row + 3][col] == player
                and board[row + 4][col] == player
                and board[row + 5][col] == "."
            ):
                pente_count += 1

        # Check diagonal captures (NW-SE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col - 1] == player
                and board[row - 2][col - 2] == player
                and board[row - 3][col - 3] == player
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
                and board[row + 4][col + 4] == player
                and board[row + 5][col + 5] == "."
            ):
                pente_count += 1

        # Check diagonal captures (SW-NE)
        if row >= 3 and row <= 15 and col >= 3 and col <= 15:
            if (
                board[row - 1][col + 1] == player
                and board[row - 2][col + 2] == player
                and board[row - 3][col + 3] == player
                and board[row - 4][col + 4] == player
                and board[row - 5][col + 5] == "."
            ):
                pente_count += 1
            if (
                row <= 14
                and col >= 2
                and board[row + 1][col - 1] == player
                and board[row + 2][col - 2] == player
                and board[row + 3][col - 3] == player
                and board[row + 4][col - 4] == player
                and board[row + 5][col - 5] == "."
            ):
                pente_count += 1

    # print("triads count: ")
    # print(triads_count)
    return quads_count


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