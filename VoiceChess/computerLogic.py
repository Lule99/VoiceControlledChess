from board import *
from math import inf


class Heuristic(object):

    king_positions = [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20],
    ]

    queen_positions = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    rook_positions = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ]

    knight_positions = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 15, 20, 20, 15, 0, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    bishop_positions = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    pawn_positions = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    possible_first_moves = []

    last_computer_moves = [[], [], [], [], []]
    last_user_moves = [[], [], [], [], []]

    @staticmethod
    def is_game_over(board):
        if (Heuristic.check_if_it_is_tie()):
            return True
        return abs(Heuristic.calculate(board)) > 5000

    @staticmethod
    def calculate(board):

        score = 0
        for i in range(0, 8):
            for k in range(0, 8):
                if (not board.fields[i][k] == EMPTY_FIELD):
                    if (get_piece_color(board.fields[i][k]) == board.computer_color):
                        score += Heuristic.calculate_piece_value(
                            board.fields[i][k]) + Heuristic.get_position_value(board.fields[i][k], 7 - i, k)
                    else:
                        score -= Heuristic.calculate_piece_value(
                            board.fields[i][k]) + Heuristic.get_position_value(board.fields[i][k], i, k)

        return score

    @staticmethod
    def calculate_piece_value(piece):

        if (piece in KING):
            return 10000

        elif (piece in QUEEN):
            return 900

        elif (piece in ROOK):
            return 500

        elif (piece in BISHOP):
            return 300

        elif (piece in KNIGHT):
            return 300

        else:
            return 100

    @staticmethod
    def get_position_value(piece, y, x):

        if (piece in KING):
            return Heuristic.king_positions[y][x]
        elif (piece in QUEEN):
            return Heuristic.queen_positions[y][x]
        elif (piece in ROOK):
            return Heuristic.rook_positions[y][x]
        elif (piece in KNIGHT):
            return Heuristic.knight_positions[y][x]
        elif (piece in BISHOP):
            return Heuristic.bishop_positions[y][x]
        else:
            return Heuristic.pawn_positions[y][x]

    @staticmethod
    def minimax(board, depth, color_on_turn, alpha, beta, goal_depth, first_move, first_user_move):

        if (depth == goal_depth):
            return Heuristic.calculate(board)

        if (board.computer_color == color_on_turn):
            best_value = -100000
            moves = board.get_possible_moves(color_on_turn)
            if (len(moves) == 0):
                if (not board.check_if_it_is_check(color_on_turn)):
                    return 0
                else:
                    return best_value

            if (first_move == -1):

                move_to_make = -1
                Heuristic.possible_first_moves = moves
                for i in range(0, len(moves)):
                    if (Heuristic.check_for_possible_tie_computer(moves[i])):
                        value = 0
                    else:
                        value = Heuristic.minimax(moves[i], depth + 1, get_opponent_color(
                            color_on_turn), alpha, beta, goal_depth, i, first_user_move)
                    if (best_value < value):
                        best_value = value
                        move_to_make = i
                    alpha = max(alpha, best_value)
                    if (beta <= alpha):
                        break
                Heuristic.write_computer_move(
                    Heuristic.possible_first_moves[move_to_make])

                return Heuristic.possible_first_moves[move_to_make]
            else:
                for i in range(0, len(moves)):
                    value = Heuristic.minimax(moves[i], depth + 1, get_opponent_color(
                        color_on_turn), alpha, beta, goal_depth, first_move, first_user_move)
                    best_value = max(value, best_value)
                    alpha = max(alpha, best_value)
                    if (beta <= alpha):
                        break

                return best_value

        else:
            best_value = 100000
            moves = board.get_possible_moves(color_on_turn)
            if (len(moves) == 0):
                if (not board.check_if_it_is_check(color_on_turn)):
                    return 0
                else:
                    # ako je sah mat, skaliraj ga
                    best_value = best_value * (goal_depth + 1 - depth)

            for i in range(0, len(moves)):
                if (first_user_move == -1 and Heuristic.check_for_possible_tie_user(moves[i])):
                    value = 0
                else:
                    value = Heuristic.minimax(moves[i], depth + 1, get_opponent_color(
                        color_on_turn), alpha, beta, goal_depth, first_move, 0)
                best_value = min(value, best_value)
                beta = min(beta, best_value)
                if (beta <= alpha):
                    break

            return best_value

    @staticmethod
    def optimized_minimax(board, depth, color_on_turn, alpha, beta, first_move, first_user_move, possible_moves, goal_depth=4):

        if (depth == goal_depth):
            return Heuristic.calculate(board)

        if (board.computer_color == color_on_turn):
            best_value = -100000
            #moves = Heuristic.get_best_moves_according_to_heuristic(board.get_possible_moves(color_on_turn), True)
            moves = board.get_possible_moves(color_on_turn)
            if (len(moves) == 0):
                if (not board.check_if_it_is_check(color_on_turn)):
                    return 0
                else:
                    return best_value

            if (first_move == -1):

                move_to_make = -1
                moves = possible_moves
                Heuristic.possible_first_moves = moves
                for i in range(0, len(moves)):
                    if (Heuristic.check_for_possible_tie_computer(moves[i])):
                        value = 0
                    else:
                        value = Heuristic.optimized_minimax(moves[i], depth + 1, get_opponent_color(
                            color_on_turn), alpha, beta, i, first_user_move, [])
                    if (best_value < value):
                        best_value = value
                        move_to_make = i
                    alpha = max(alpha, best_value)
                    if (beta <= alpha):
                        break
                Heuristic.write_computer_move(
                    Heuristic.possible_first_moves[move_to_make])

                return Heuristic.possible_first_moves[move_to_make]
                #return best_value
            else:
                for i in range(0, len(moves)):
                    value = Heuristic.optimized_minimax(moves[i], depth + 1, get_opponent_color(
                        color_on_turn), alpha, beta, first_move, first_user_move, [])
                    best_value = max(value, best_value)
                    alpha = max(alpha, best_value)
                    if (beta <= alpha):
                        break

                return best_value

        else:
            best_value = 100000
            #moves = Heuristic.get_best_moves_according_to_heuristic(board.get_possible_moves(color_on_turn), False)
            moves = board.get_possible_moves(color_on_turn)
            if (len(moves) == 0):
                if (not board.check_if_it_is_check(color_on_turn)):
                    return 0
                else:
                    # ako je sah mat, skaliraj ga
                    best_value = best_value * (goal_depth + 1 - depth)

            for i in range(0, len(moves)):
                if (first_user_move == -1 and Heuristic.check_for_possible_tie_user(moves[i])):
                    value = 0
                else:
                    value = Heuristic.optimized_minimax(moves[i], depth + 1, get_opponent_color(
                        color_on_turn), alpha, beta, first_move, 0, [])
                best_value = min(value, best_value)
                beta = min(beta, best_value)
                if (beta <= alpha):
                    break

            return best_value

    @staticmethod
    def get_best_moves_according_to_heuristic(possible_moves, searching_for_max, number_of_moves):

        if (len(possible_moves) < number_of_moves):
            number_of_moves = len(possible_moves)

        return Heuristic.Nmaxelements(possible_moves, number_of_moves, searching_for_max)

    @staticmethod
    def Nmaxelements(list, N, biggest):
        final_list = []

        if (biggest):
            for i in range(0, N):
                max1 = -inf
                index = -1

                for j in range(len(list)):
                    value = Heuristic.calculate(list[j])
                    if value > max1:
                        max1 = value
                        index = j

                final_list.append(list[index])
                del list[index]
        else:
            for i in range(0, N):
                max1 = inf
                index = -1

                for j in range(len(list)):
                    value = Heuristic.calculate(list[j])
                    if value < max1:
                        max1 = value
                        index = j

                final_list.append(list[index])
                del list[index]

        return final_list

    @staticmethod
    def check_for_possible_tie_computer(board):

        if (Heuristic.last_computer_moves[1] == board and Heuristic.last_computer_moves[3] == board):
            return True

        return False

    @staticmethod
    def check_for_possible_tie_user(board):

        if (Heuristic.last_user_moves[1] == board and Heuristic.last_user_moves[3] == board):
            return True

        return False

    @staticmethod
    def write_computer_move(board):

        Heuristic.last_computer_moves[0] = Heuristic.last_computer_moves[1]
        Heuristic.last_computer_moves[1] = Heuristic.last_computer_moves[2]
        Heuristic.last_computer_moves[2] = Heuristic.last_computer_moves[3]
        Heuristic.last_computer_moves[3] = Heuristic.last_computer_moves[4]
        Heuristic.last_computer_moves[4] = board.get_deep_copy()

    @staticmethod
    def write_player_move(board):

        Heuristic.last_user_moves[0] = Heuristic.last_user_moves[1]
        Heuristic.last_user_moves[1] = Heuristic.last_user_moves[2]
        Heuristic.last_user_moves[2] = Heuristic.last_user_moves[3]
        Heuristic.last_user_moves[3] = Heuristic.last_user_moves[4]
        Heuristic.last_user_moves[4] = board.get_deep_copy()

    @staticmethod
    def get_computer_move(board, choosed_level):

        new_board_state = Heuristic.minimax(
            board, 0, board.computer_color, -1000000, 1000000, choosed_level, -1, -1)
        if (isinstance(new_board_state, Board)):
            print("------------------------------------------------")
            move = new_board_state.last_move.split(" ")
            print("Computer move: " + move[0] + " --> " + move[1])
            print("------------------------------------------------")

        return new_board_state

    @staticmethod
    def check_if_it_is_tie():
        if (Heuristic.last_computer_moves[0] != [] and Heuristic.last_computer_moves[0] == Heuristic.last_computer_moves[2] and Heuristic.last_computer_moves[0] == Heuristic.last_computer_moves[4]):
            return True
        elif (Heuristic.last_user_moves[0] != [] and Heuristic.last_user_moves[0] == Heuristic.last_user_moves[2] and Heuristic.last_user_moves[0] == Heuristic.last_user_moves[4]):
            return True

        return False
