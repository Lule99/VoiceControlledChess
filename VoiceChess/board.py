from pieces import *


class Board(object):

    def __init__(self, player_is_black):

        if (player_is_black):
            self.fields = Board.get_initial_board(BLACK_COLOR)
            self.computer_color = WHITE_COLOR
        else:
            self.fields = Board.get_initial_board(WHITE_COLOR)
            self.computer_color = BLACK_COLOR

        self.computer_king_position = [0, 4]
        self.computer_king_moved = False
        self.user_king_position = [7, 4]
        self.user_king_moved = False
        self.last_move = EMPTY_STRING

    @staticmethod
    def get_initial_board(player_color):

        if (player_color == BLACK_COLOR):
            return PLAYER_BLACK_INITIAL_BOARD

        return PLAYER_WHITE_INITIAL_BOARD

    def __eq__(self, other):

        if (not isinstance(other, Board)):
            return False

        if (self.computer_color !=other.computer_color):
            return False

        for i in range(0, 8):
            for k in range(0, 8):
                if (self.fields[i][k] != other.fields[i][k]):
                    return False

        return True

    def get_deep_copy(self):

        new_board = Board(self.computer_color == WHITE_COLOR)
        new_board.computer_king_moved = self.computer_king_moved
        new_board.user_king_moved = self.user_king_moved
        new_board.computer_king_position = [self.computer_king_position[0], self.computer_king_position[1]]
        new_board.user_king_position = [self.user_king_position[0], self.user_king_position[1]]
        new_board.last_move = self.last_move
        new_board.fields = []

        for i in range(0, 8):
            new_row = []

            for k in range(0, 8):
                new_row.append(self.fields[i][k])

            new_board.fields.append(new_row)

        return new_board

    def get_possible_moves(self, color_on_the_turn):

        moves = []
        legal_moves = []

        for i in range(0,8):
            for k in range (0,8):
                if ((not empty_field(self.fields[i][k])) and get_piece_color(self.fields[i][k]) == color_on_the_turn):
                    piece = Piece(self.fields[i][k], k, i, self.get_deep_copy())
                    moves += piece.get_legal_moves()

        for move in moves:
            if not move.check_if_it_is_check(color_on_the_turn):
                legal_moves.append(move)

        return legal_moves

    def check_for_castling(self, king):

        castling_moves = []

        if (self.computer_color == get_piece_color(king) and self.computer_king_moved == False):
            castling_moves += self.left_castling(king)
            castling_moves += self.right_castling(king)
        elif (self.computer_color == get_opponent_color(get_piece_color(king)) and self.user_king_moved == False):
            castling_moves += self.left_castling(king)
            castling_moves += self.right_castling(king)

        return castling_moves

    def left_castling(self, king):

        moves = []

        if (self.fields[king.y][king.x - 1] == EMPTY_FIELD and self.fields[king.y][king.x - 2] == EMPTY_FIELD and
            self.fields[king.y][king.x - 3] == EMPTY_FIELD and (not self.fields[king.y][king.x - 4] == EMPTY_FIELD) and
            self.fields[king.y][king.x - 4] in ROOK and get_piece_color(self.fields[king.y][king.x - 4]) == king.color):

            if (king.no_opponent_king_around(self, [0,-2])):

                new_board = self.get_deep_copy()
                new_king = king.get_deep_copy()
                new_king.x = king.x - 2

                new_board.fields[king.y][king.x - 2] = new_king.piece

                if (get_piece_color(self.fields[king.y][king.x - 4]) == BLACK_COLOR):
                    new_board.fields[king.y][king.x - 1] = BLACK_ROOK
                else:
                    new_board.fields[king.y][king.x - 1] = WHITE_ROOK

                new_board.fields[king.y][king.x] = EMPTY_FIELD
                new_board.fields[king.y][king.x - 4] = EMPTY_FIELD
                if (king.color == self.computer_color):
                    new_board.computer_king_position = [new_king.y, new_king.x]
                    new_board.computer_king_moved = True
                    new_board.last_move = generate_string_for_move(king.x, king.y, [0,-2])
                else:
                    new_board.user_king_position = [new_king.y, new_king.x]
                    new_board.user_king_moved = True
                    new_board.last_move = generate_string_for_move(king.x, king.y, [0,-2])
                moves.append(new_board)

        return moves

    def right_castling(self, king):

        moves = []

        if (self.fields[king.y][king.x + 1] == EMPTY_FIELD and self.fields[king.y][king.x + 2] == EMPTY_FIELD and (not self.fields[king.y][king.x + 3] == EMPTY_FIELD) and
            self.fields[king.y][king.x + 3] in ROOK and get_piece_color(self.fields[king.y][king.x + 3]) == king.color):
            if (king.no_opponent_king_around(self, [0, 2])):
                new_board = self.get_deep_copy()
                new_king = king.get_deep_copy()
                new_king.x = king.x + 2

                new_board.fields[king.y][king.x + 2] = new_king.piece

                if (get_piece_color(self.fields[king.y][king.x +3]) == BLACK_COLOR):
                    new_board.fields[king.y][king.x + 1] = BLACK_ROOK
                else:
                    new_board.fields[king.y][king.x + 1] = WHITE_ROOK

                new_board.fields[king.y][king.x] = EMPTY_FIELD
                new_board.fields[king.y][king.x + 3] = EMPTY_FIELD
                if (king.color == self.computer_color):
                    new_board.computer_king_position = [new_king.y, new_king.x]
                    new_board.computer_king_moved = True
                    new_board.last_move = generate_string_for_move(king.x, king.y, [0,2])
                else:
                    new_board.user_king_position = [new_king.y, new_king.x]
                    new_board.user_king_moved = True
                    new_board.last_move = generate_string_for_move(king.x, king.y, [0,2])
                moves.append(new_board)

        return moves

    def check_if_it_is_check(self, color_on_the_turn):

        if (self.check_lines(color_on_the_turn)):
            return True
        elif (self.check_diagonales(color_on_the_turn)):
            return True
        elif (self.check_knights(color_on_the_turn)):
            return True
        elif (self.check_pawns(color_on_the_turn)):
            return True

        return False

    def check_lines(self, color_on_the_turn):

        if (color_on_the_turn == self.computer_color):
            king_position = self.computer_king_position
        else:
            king_position = self.user_king_position

        x_position_down = king_position[1] - 1
        x_position_up = king_position[1] + 1
        y_position_down = king_position[0] - 1
        y_position_up = king_position[0] + 1

        while (x_position_down >= 0):
            if (not self.fields[king_position[0]][x_position_down] == EMPTY_FIELD):
                if (get_piece_color(self.fields[king_position[0]][x_position_down]) == get_opponent_color(color_on_the_turn) and
                        (self.fields[king_position[0]][x_position_down] in QUEEN or self.fields[
                            king_position[0]][x_position_down] in ROOK)):
                    return True
                break
            x_position_down -= 1

        while (x_position_up < 8):
            if (not self.fields[king_position[0]][x_position_up] == EMPTY_FIELD):
                if (get_piece_color(self.fields[king_position[0]][x_position_up]) == get_opponent_color(color_on_the_turn) and
                        (self.fields[king_position[0]][x_position_up] in QUEEN or self.fields[
                            king_position[0]][x_position_up] in ROOK)):
                    return True
                break
            x_position_up += 1

        while (y_position_down >= 0):
            if (not self.fields[y_position_down][king_position[1]] == EMPTY_FIELD):
                if (get_piece_color(self.fields[y_position_down][king_position[1]]) == get_opponent_color(color_on_the_turn) and
                        (self.fields[y_position_down][king_position[1]] in QUEEN or self.fields[
                            y_position_down][king_position[1]] in ROOK)):
                    return True
                break
            y_position_down -= 1

        while (y_position_up < 8):
            if (not self.fields[y_position_up][king_position[1]] == EMPTY_FIELD):
                if (get_piece_color(self.fields[y_position_up][king_position[1]]) == get_opponent_color(color_on_the_turn) and
                        (self.fields[y_position_up][king_position[1]] in QUEEN or self.fields[
                            y_position_up][king_position[1]] in ROOK)):
                    return True
                break
            y_position_up += 1

        return False

    def check_diagonales(self, color_on_the_turn):

        if (color_on_the_turn == self.computer_color):
            king_position = self.computer_king_position
        else:
            king_position = self.user_king_position

        counter_x = 1
        counter_y = 1
        #dole desno
        while (king_position[1] + counter_x < 8 and king_position[0] + counter_y < 8):
            if (not self.fields[king_position[0] + counter_y][king_position[1] + counter_x] == EMPTY_FIELD):
                if (get_piece_color(self.fields[king_position[0] + counter_y][king_position[1] + counter_x]) == get_opponent_color(color_on_the_turn) and
                        (self.fields[king_position[0] + counter_y][king_position[1] + counter_x] in QUEEN or self.fields[king_position[0] + counter_y][king_position[1] + counter_x] in BISHOP)):
                    return True
                break
            counter_x += 1
            counter_y += 1

        counter_x = 1
        counter_y = 1
        #dole levo
        while (king_position[1] - counter_x >= 0 and king_position[0] + counter_y < 8):
            if (not self.fields[king_position[0] + counter_y][king_position[1] - counter_x] == EMPTY_FIELD):
                if (get_piece_color(self.fields[king_position[0] + counter_y][king_position[1] - counter_x]) == get_opponent_color(color_on_the_turn) and
                        (self.fields[king_position[0] + counter_y][king_position[1] - counter_x] in QUEEN or self.fields[king_position[0] + counter_y][king_position[1] - counter_x] in BISHOP)):
                    return True
                break
            counter_x += 1
            counter_y += 1

        counter_x = 1
        counter_y = 1
        #gore desno
        while (king_position[1] + counter_x < 8 and king_position[0] - counter_y >= 0):
            if (not self.fields[king_position[0] - counter_y][king_position[1] + counter_x] == EMPTY_FIELD):
                if (get_piece_color(self.fields[king_position[0] - counter_y][king_position[1] + counter_x]) == get_opponent_color(color_on_the_turn) and
                        (self.fields[king_position[0] - counter_y][king_position[1] + counter_x] in QUEEN or self.fields[king_position[0] - counter_y][king_position[1] + counter_x] in BISHOP)):
                    return True
                break
            counter_x += 1
            counter_y += 1

        counter_x = 1
        counter_y = 1
        #gore levo
        while (king_position[1] - counter_x >= 0 and king_position[0] - counter_y >= 0):
            if (not self.fields[king_position[0] - counter_y][king_position[1] - counter_x] == EMPTY_FIELD):
                if (get_piece_color(self.fields[king_position[0] - counter_y][king_position[1] - counter_x]) == get_opponent_color(color_on_the_turn) and
                        (self.fields[king_position[0] - counter_y][king_position[1] - counter_x] in QUEEN or self.fields[king_position[0] - counter_y][king_position[1] - counter_x] in BISHOP)):
                    return True
                break
            counter_x += 1
            counter_y += 1

        return False

    def check_knights(self, color_on_the_turn):

        if (color_on_the_turn == self.computer_color):
            king_position = self.computer_king_position
        else:
            king_position = self.user_king_position

        if (is_on_the_board(king_position[0] + 2, king_position[1] + 1) and (not self.fields[king_position[0] + 2][king_position[1] + 1] == EMPTY_FIELD) and self.fields[king_position[0] + 2][king_position[1] + 1] in KNIGHT and get_piece_color(self.fields[king_position[0] + 2][king_position[1] + 1]) == get_opponent_color(color_on_the_turn)):
            return True
        elif (is_on_the_board(king_position[0] + 2, king_position[1] - 1) and (not self.fields[king_position[0] + 2][king_position[1] - 1] == EMPTY_FIELD) and self.fields[king_position[0] + 2][king_position[1] - 1] in KNIGHT and get_piece_color(self.fields[king_position[0] + 2][king_position[1] - 1]) == get_opponent_color(color_on_the_turn)):
            return True
        elif (is_on_the_board(king_position[0] + 1, king_position[1] + 2) and (not self.fields[king_position[0] + 1][king_position[1] + 2] == EMPTY_FIELD) and self.fields[king_position[0] + 1][king_position[1] + 2] in KNIGHT and get_piece_color(self.fields[king_position[0] + 1][king_position[1] + 2]) == get_opponent_color(color_on_the_turn)):
            return True
        elif (is_on_the_board(king_position[0] + 1, king_position[1] - 2) and (not self.fields[king_position[0] + 1][king_position[1] - 2] == EMPTY_FIELD) and self.fields[king_position[0] + 1][king_position[1] - 2] in KNIGHT and get_piece_color(self.fields[king_position[0] + 1][king_position[1] - 2]) == get_opponent_color(color_on_the_turn)):
            return True
        elif (is_on_the_board(king_position[0] - 1, king_position[1] + 2) and (not self.fields[king_position[0] - 1][king_position[1] + 2] == EMPTY_FIELD) and self.fields[king_position[0] - 1][king_position[1] + 2] in KNIGHT and get_piece_color(self.fields[king_position[0] - 1][king_position[1] + 2]) == get_opponent_color(color_on_the_turn)):
            return True
        elif (is_on_the_board(king_position[0] - 1, king_position[1] - 2) and (not self.fields[king_position[0] - 1][king_position[1] - 2] == EMPTY_FIELD) and self.fields[king_position[0] - 1][king_position[1] - 2] in KNIGHT and get_piece_color(self.fields[king_position[0] - 1][king_position[1] - 2]) == get_opponent_color(color_on_the_turn)):
            return True
        elif (is_on_the_board(king_position[0] - 2, king_position[1] + 1) and (not self.fields[king_position[0] - 2][king_position[1] + 1] == EMPTY_FIELD) and self.fields[king_position[0] - 2][king_position[1] + 1] in KNIGHT and get_piece_color(self.fields[king_position[0] - 2][king_position[1] + 1]) == get_opponent_color(color_on_the_turn)):
            return True
        elif (is_on_the_board(king_position[0] - 2, king_position[1] - 1) and (not self.fields[king_position[0] - 2][king_position[1] - 1] == EMPTY_FIELD) and self.fields[king_position[0] - 2][king_position[1] - 1] in KNIGHT and get_piece_color(self.fields[king_position[0] - 2][king_position[1] - 1]) == get_opponent_color(color_on_the_turn)):
            return True

        return False

    def check_pawns(self, color_on_the_turn):

        if (color_on_the_turn == self.computer_color):
            king_position = self.computer_king_position
            if ((is_on_the_board(king_position[1] + 1, king_position[0] + 1) and not self.fields[king_position[0] + 1][king_position[1] + 1] == EMPTY_FIELD) and
                    self.fields[king_position[0] + 1][king_position[1] + 1] in PAWN and get_piece_color(self.fields[king_position[0] + 1][king_position[1] + 1]) == get_opponent_color(color_on_the_turn)):
                return True
            elif ((is_on_the_board(king_position[1] - 1, king_position[0] + 1) and not self.fields[king_position[0] + 1][king_position[1] - 1] == EMPTY_FIELD) and
                  self.fields[king_position[0] + 1][king_position[1] - 1] in PAWN and get_piece_color(self.fields[king_position[0] + 1][king_position[1] - 1]) == get_opponent_color(color_on_the_turn)):
                return True
        else:
            king_position = self.user_king_position
            if ((is_on_the_board(king_position[1] + 1, king_position[0] - 1) and not self.fields[king_position[0] - 1][king_position[1] + 1] == EMPTY_FIELD) and
                    self.fields[king_position[0] - 1][king_position[1] + 1] in PAWN and get_piece_color(self.fields[king_position[0] - 1][king_position[1] + 1]) == get_opponent_color(color_on_the_turn)):
                return True
            elif ((is_on_the_board(king_position[1] - 1, king_position[0] - 1) and not self.fields[king_position[0] - 1][king_position[1] - 1] == EMPTY_FIELD) and
                  self.fields[king_position[0] - 1][king_position[1] - 1] in PAWN and get_piece_color(self.fields[king_position[0] - 1][king_position[1] - 1]) == get_opponent_color(color_on_the_turn)):
                return True

        return False

    def evaluate_move(self, piece, piece_x, piece_y, move):

        new_board = self.get_deep_copy()
        new_board.fields[piece_y][piece_x] = EMPTY_FIELD
        new_x_position = piece_x + move[1]
        new_y_position = piece_y + move[0]
        new_piece = piece + ""
        new_board.fields[new_y_position][new_x_position] = new_piece
        new_board.last_move = generate_string_for_move(piece_x, piece_y, move)

        if (new_piece in KING):
            if (get_piece_color(new_piece) == self.computer_color):
                new_board.computer_king_position = [new_y_position, new_x_position]
                new_board.computer_king_moved = True
            else:
                new_board.user_king_position = [new_y_position, new_x_position]
                new_board.user_king_moved = True
        elif (new_piece in PAWN):
            if (new_y_position == 0 and get_piece_color(new_piece) == get_opponent_color(new_board.computer_color)):

                if (self.computer_color == BLACK_COLOR):
                    pawn_become_queen = WHITE_QUEEN
                else:
                    pawn_become_queen = BLACK_QUEEN

                new_board.fields[new_y_position][new_x_position] = pawn_become_queen
            elif (new_y_position == 7 and get_piece_color(new_piece) == new_board.computer_color):

                if (self.computer_color == BLACK_COLOR):
                    pawn_become_queen = WHITE_QUEEN
                else:
                    pawn_become_queen = BLACK_QUEEN

                new_board.fields[new_piece.y][new_piece.x] = pawn_become_queen
            # check for el passant
            elif (self.fields[new_y_position][new_x_position] == EMPTY_FIELD and move[1] != 0):
                new_board.fields[piece_y][new_x_position] = EMPTY_FIELD

        return new_board