from constants import *
from pieces import *


def empty_field(field_value):
    return field_value == EMPTY_FIELD


def get_piece_color(piece):

    if (piece in BLACK_PIECES):
        return BLACK_COLOR

    return WHITE_COLOR


def get_opponent_color(color):

    if (color == WHITE_COLOR):
        return BLACK_COLOR

    return WHITE_COLOR


def is_on_the_board(x, y):

    if (x > 7 or x < 0 or y > 7 or y < 0):
        return False

    return True


def get_legal_moves_on_lines(piece, board):

    moves = []
    x_counter = 1
    y_counter = 1

    while (piece.x + x_counter <= 7):
        if (not board.fields[piece.y][piece.x + x_counter] == EMPTY_FIELD):
            if (get_piece_color(board.fields[piece.y][piece.x + x_counter]) == piece.color):
                break
            else:
                moves.append(board.evaluate_move(
                    piece.piece, piece.x, piece.y, [0, x_counter]))
                break
        else:
            moves.append(board.evaluate_move(
                piece.piece, piece.x, piece.y, [0, x_counter]))
        x_counter += 1

    x_counter = -1

    while (piece.x + x_counter >= 0):
        if (not board.fields[piece.y][piece.x + x_counter] == EMPTY_FIELD):
            if (get_piece_color(board.fields[piece.y][piece.x + x_counter]) == piece.color):
                break
            else:
                moves.append(board.evaluate_move(
                    piece.piece, piece.x, piece.y, [0, x_counter]))
                break
        else:
            moves.append(board.evaluate_move(
                piece.piece, piece.x, piece.y, [0, x_counter]))
        x_counter -= 1

    while (piece.y + y_counter <= 7):
        if (not board.fields[piece.y + y_counter][piece.x] == EMPTY_FIELD):
            if (get_piece_color(board.fields[piece.y + y_counter][piece.x]) == piece.color):
                break
            else:
                moves.append(board.evaluate_move(
                    piece.piece, piece.x, piece.y, [y_counter, 0]))
                break
        else:
            moves.append(board.evaluate_move(
                piece.piece, piece.x, piece.y, [y_counter, 0]))
        y_counter += 1

    y_counter = -1

    while (piece.y + y_counter >= 0):
        if (not board.fields[piece.y + y_counter][piece.x] == EMPTY_FIELD):
            if (get_piece_color(board.fields[piece.y + y_counter][piece.x]) == piece.color):
                break
            else:
                moves.append(board.evaluate_move(
                    piece.piece, piece.x, piece.y, [y_counter, 0]))
                break
        else:
            moves.append(board.evaluate_move(
                piece.piece, piece.x, piece.y, [y_counter, 0]))
        y_counter -= 1

    return moves


def get_legal_moves_on_diagonales(piece, board):

    moves = []
    counter_x = 1
    counter_y = 1
    # dole desno
    while (piece.x + counter_x < 8 and piece.y + counter_y < 8):
        if (not board.fields[piece.y + counter_y][piece.x + counter_x] == EMPTY_FIELD):
            if (get_piece_color(board.fields[piece.y + counter_y][piece.x + counter_x]) == piece.color):
                break
            else:
                moves.append(board.evaluate_move(
                    piece.piece, piece.x, piece.y, [counter_y, counter_x]))
                break
        else:
            moves.append(board.evaluate_move(
                piece.piece, piece.x, piece.y, [counter_y, counter_x]))
        counter_x += 1
        counter_y += 1

    counter_x = -1
    counter_y = 1
    # dole levo
    while (piece.x + counter_x >= 0 and piece.y + counter_y < 8):
        if (not board.fields[piece.y + counter_y][piece.x + counter_x] == EMPTY_FIELD):
            if (get_piece_color(board.fields[piece.y + counter_y][piece.x + counter_x]) == piece.color):
                break
            else:
                moves.append(board.evaluate_move(
                    piece.piece, piece.x, piece.y, [counter_y, counter_x]))
                break
        else:
            moves.append(board.evaluate_move(
                piece.piece, piece.x, piece.y, [counter_y, counter_x]))
        counter_x -= 1
        counter_y += 1

    counter_x = 1
    counter_y = -1
    # dole levo
    while (piece.x + counter_x < 8 and piece.y + counter_y >= 0):
        if (not board.fields[piece.y + counter_y][piece.x + counter_x] == EMPTY_FIELD):
            if (get_piece_color(board.fields[piece.y + counter_y][piece.x + counter_x]) == piece.color):
                break
            else:
                moves.append(board.evaluate_move(
                    piece.piece, piece.x, piece.y, [counter_y, counter_x]))
                break
        else:
            moves.append(board.evaluate_move(
                piece.piece, piece.x, piece.y, [counter_y, counter_x]))
        counter_x += 1
        counter_y -= 1

    counter_x = -1
    counter_y = -1
    # dole levo
    while (piece.x + counter_x >= 0 and piece.y + counter_y >= 0):
        if (not board.fields[piece.y + counter_y][piece.x + counter_x] == EMPTY_FIELD):
            if (get_piece_color(board.fields[piece.y + counter_y][piece.x + counter_x]) == piece.color):
                break
            else:
                moves.append(board.evaluate_move(
                    piece.piece, piece.x, piece.y, [counter_y, counter_x]))
                break
        else:
            moves.append(board.evaluate_move(
                piece.piece, piece.x, piece.y, [counter_y, counter_x]))
        counter_x -= 1
        counter_y -= 1

    return moves


def get_user_inputs_for_game_start():

    while (True):
        try:
            print("Choose dificult:\n")
            print("\t1. Easy\n")
            print("\t2. Medium\n")
            print("\t3. Hard\n")
            value = int(input("Your choice: "))
            if (value == 1):
                choosed_level = 1
                break
            elif (value == 2):
                choosed_level = 3
                break
            elif (value == 3):
                choosed_level = 4
                break
            else:
                print("Input is invalid, try again..\n")
        except:
            print("Input is invalid, try again..\n")

    while (True):
        try:
            print("Choose color:\n")
            print("\t1. Black\n")
            print("\t2. White\n")
            value = int(input("Your choice: "))
            if (value == 1):
                color = BLACK_COLOR
                break
            elif (value == 2):
                color = WHITE_COLOR
                break
            else:
                print("Input is invalid, try again..\n")
        except:
            print("Input is invalid, try again..\n")

    return[choosed_level, color]


def get_player_move(board):

    while (True):
        try:
            print("Your turn, type your move (for example 'A2 A4'):\n")
            next_move = input(">> ")
            if (not check_if_format_is_valid(next_move)):
                print("Command format is invalid, try again..\n")
            else:
                new_board_state = check_if_move_is_valid(next_move, board)
                if (new_board_state == []):
                    print("That move is invalid, try again..\n")
                else:
                    print_player_move(next_move)
                    return new_board_state
        except:
            print("Move command is invalid, try again..\n")


def print_player_move(next_move):

    print("------------------------------------------------")
    move = next_move.split(" ")
    print("Player move: " + move[0] + " --> " + move[1])
    print("------------------------------------------------")


def check_if_format_is_valid(next_move):

    try:
        field_from, field_to = next_move.split(" ")
        if not (field_from[0] == "A" or field_from[0] == "B" or field_from[0] == "C" or field_from[0] == "D"
                or field_from[0] == "E" or field_from[0] == "F" or field_from[0] == "G" or field_from[0] == "H"):
            return False
        if not (field_to[0] == "A" or field_to[0] == "B" or field_to[0] == "C" or field_to[0] == "D"
                or field_to[0] == "E" or field_to[0] == "F" or field_to[0] == "G" or field_to[0] == "H"):
            return False
        if (int(field_from[1]) > 8 or int(field_from[1]) < 1):
            return False
        if (int(field_to[1]) > 8 or int(field_to[1]) < 1):
            return False
        return True
    except:
        return False


def check_if_move_is_valid(next_move, board):

    field_from, field_to = next_move.split(" ")
    coordinates_from = [convertor_from_char_to_position(
        field_from[0]), 8 - int(field_from[1])]
    coordinates_to = [convertor_from_char_to_position(
        field_to[0]), 8 - int(field_to[1])]
    move = [coordinates_to[1] - coordinates_from[1],
            coordinates_to[0] - coordinates_from[0]]
    if (is_it_castling(coordinates_from, move, board)):
        new_board_state = evaluate_castling(coordinates_from, move, board)
    else:
        new_board_state = board.evaluate_move(
            board.fields[coordinates_from[1]][coordinates_from[0]], coordinates_from[0], coordinates_from[1], move)

    return check_if_thats_possible_move(board, new_board_state)


def is_it_castling(coordinates_from, move, board):

    if (board.fields[coordinates_from[1]][coordinates_from[0]] in KING and abs(move[1]) == 2):
        return True

    return False


def evaluate_castling(coordinates_from, move, board):

    new_board = board.get_deep_copy()
    x = coordinates_from[0]
    y = coordinates_from[1]
    piece = board.fields[y][x]

    if (move[1] > 0):

        rook = new_board.fields[y][x + 3]

        new_board.fields[y][x + 2] = piece
        new_board.fields[y][x + 1] = rook
        new_board.fields[y][x] = EMPTY_FIELD
        new_board.fields[y][x + 3] = EMPTY_FIELD

        if (get_piece_color(piece) == board.computer_color):
            new_board.computer_king_position = [y, x + 2]
            new_board.computer_king_moved = True
        else:
            new_board.user_king_position = [y, x + 2]
            new_board.user_king_moved = True

    else:

        rook = new_board.fields[y][x - 4]

        new_board.fields[y][x - 2] = piece
        new_board.fields[y][x - 1] = rook
        new_board.fields[y][x] = EMPTY_FIELD
        new_board.fields[y][x - 4] = EMPTY_FIELD

        if (get_piece_color(piece) == board.computer_color):
            new_board.computer_king_position = [y, x - 2]
            new_board.computer_king_moved = True
        else:
            new_board.user_king_position = [y, x - 2]
            new_board.user_king_moved = True

    return new_board


def check_if_thats_possible_move(board, new_board_state):

    possible_board_states = board.get_possible_moves(
        get_opponent_color(board.computer_color))
    for board_state in possible_board_states:
        if (board_state == new_board_state):
            return new_board_state

    return []


def convertor_from_char_to_position(char):

    if (char == "A"):
        return 0
    elif (char == "B"):
        return 1
    elif (char == "C"):
        return 2
    elif (char == "D"):
        return 3
    elif (char == "E"):
        return 4
    elif (char == "F"):
        return 5
    elif (char == "G"):
        return 6
    else:
        return 7


def convertor_from_position_to_char(char):

    if (char == 0):
        return "A"
    elif (char == 1):
        return "B"
    elif (char == 2):
        return "C"
    elif (char == 3):
        return "D"
    elif (char == 4):
        return "E"
    elif (char == 5):
        return "F"
    elif (char == 6):
        return "G"
    else:
        return "H"


def generate_string_for_move(x, y, move):
    return convertor_from_position_to_char(x) + str(8 - y) + " " + convertor_from_position_to_char(x + move[1]) + str(8 - (y + move[0]))


def count_pieces(board):

    counter = 0
    for i in range(0, 8):
        for k in range(0, 8):
            if (board.fields[i][k] != EMPTY_FIELD):
                counter += 1

    return counter


def check_if_only_pawns_remaining(board):

    for i in range(0, 8):
        for k in range(0, 8):
            if (board.fields[i][k] != EMPTY_FIELD and board.fields[i][k] not in PAWN and board.fields[i][k] not in KING):
                return False

    return True
