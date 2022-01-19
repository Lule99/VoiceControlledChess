from service import *

#Piece parent class
class Piece(object):

    def __init__(self, piece, x_position, y_position, board):#BICE OBRISANO

        self.piece = piece
        self.color = get_piece_color(piece)
        self.x = x_position
        self.y = y_position
        self.board = board

    def __str__(self):#bice obrisano
        return self.piece

    def get_legal_moves(self):

        if (self.piece in KING):
            king = King(self.piece, self.x, self.y, self.board)
            return king.get_legal_moves()

        elif (self.piece in QUEEN):
            queen = Queen(self.piece, self.x, self.y, self.board)
            return queen.get_legal_moves()

        elif (self.piece in BISHOP):
            bishop = Bishop(self.piece, self.x, self.y, self.board)
            return bishop.get_legal_moves()

        elif (self.piece in KNIGHT):
            knight = Knight(self.piece, self.x, self.y, self.board)
            return knight.get_legal_moves()

        elif (self.piece in ROOK):
            rook = Rook(self.piece, self.x, self.y, self.board)
            return rook.get_legal_moves()

        else:
            pawn = Pawn(self.piece, self.x, self.y, self.board)
            return pawn.get_legal_moves()


class King(Piece):

    def __init__(self, piece, x_position, y_position, board):
        super(King, self).__init__(piece, x_position, y_position, board)
        self.value = 10000

    def get_legal_moves(self):

        possible_moves = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]
        legal_moves = []

        for move in possible_moves:
            if (is_on_the_board(self.y + move[0], self.x + move[1]) and (self.board.fields[self.y + move[0]][self.x + move[1]] == EMPTY_FIELD or get_piece_color(self.board.fields[self.y + move[0]][self.x + move[1]]) == get_opponent_color(self.color))):
                if (self.no_opponent_king_around(self.board, move)):
                    legal_moves.append(self.board.evaluate_move(self.piece, self.x, self.y, move))

        legal_moves += self.board.check_for_castling(self)
        return legal_moves

    def no_opponent_king_around(self, board, move):

        new_position = [self.y + move[0], self.x + move[1]]

        if (self.color == board.computer_color):
            if (abs(board.user_king_position[0] - new_position[0]) >= 2 or abs(board.user_king_position[1] - new_position[1]) >= 2):
                return True

            return False
        else:
            if (abs(board.computer_king_position[0] - new_position[0]) >= 2 or abs(board.computer_king_position[1] - new_position[1]) >= 2):
                return True

            return False

    def get_deep_copy(self):
        return King(self.piece, self.x, self.y, self.board)

class Queen(Piece):

    def __init__(self, piece, x_position, y_position, board):
        super(Queen, self).__init__(piece, x_position, y_position, board)
        self.value = 900

    def get_legal_moves(self):
        legal_moves = get_legal_moves_on_lines(self, self.board) + get_legal_moves_on_diagonales(self, self.board)
        return legal_moves

    def get_deep_copy(self):
        return Queen(self.piece, self.x, self.y, self.board)


class Rook(Piece):

    def __init__(self, piece, x_position, y_position, board):
        super(Rook, self).__init__(piece, x_position, y_position, board)
        self.value = 500

    def get_legal_moves(self):
        legal_moves = get_legal_moves_on_lines(self, self.board)
        return legal_moves

    def get_deep_copy(self):
        return Rook(self.piece, self.x, self.y, self.board)


class Knight(Piece):

    def __init__(self, piece, x_position, y_position, board):
        super(Knight, self).__init__(piece, x_position, y_position, board)
        self.value = 300

    def get_legal_moves(self):

        possible_moves = [[-2, -1], [-2, 1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]]
        legal_moves = []

        for move in possible_moves:
            if (is_on_the_board(self.y + move[0], self.x + move[1]) and
                    (self.board.fields[self.y + move[0]][self.x + move[1]] == EMPTY_FIELD or
                    get_piece_color(self.board.fields[self.y + move[0]][self.x + move[1]]) == get_opponent_color(self.color))):
                legal_moves.append(self.board.evaluate_move(self.piece, self.x, self.y, move))

        return legal_moves

    def get_deep_copy(self):
        return Knight(self.piece, self.x, self.y, self.board)


class Bishop(Piece):

    def __init__(self, piece, x_position, y_position, board):
        super(Bishop, self).__init__(piece, x_position, y_position, board)
        self.value = 300

    def get_legal_moves(self):

        legal_moves = get_legal_moves_on_diagonales(self, self.board)
        return legal_moves

    def get_deep_copy(self):
        return Bishop(self.piece, self.x, self.y, self.board)


class Pawn(Piece):

    def __init__(self, piece, x_position, y_position, board):
        super(Pawn, self).__init__(piece, x_position, y_position, board)
        self.value = 100

    def get_legal_moves(self):

        if (self.color == self.board.computer_color):
            possible_moves = [[1,0], [1,1], [1,-1]]
            if (self.y == 1 and self.board.fields[self.y + 1][self.x] == EMPTY_FIELD):
                possible_moves.append([2,0])
        else:
            possible_moves = [[-1,0], [-1,1], [-1,-1]]
            if (self.y == 6 and self.board.fields[self.y - 1][self.x] == EMPTY_FIELD):
                possible_moves.append([-2,0])

        legal_moves = []

        for move in possible_moves:
            if (move[1] == 0):
                if(is_on_the_board(self.y + move[0], self.x + move[1]) and self.board.fields[self.y + move[0]][self.x + move[1]] == EMPTY_FIELD):
                    legal_moves.append(self.board.evaluate_move(self.piece, self.x, self.y, move))
            else:
                if (is_on_the_board(self.y + move[0], self.x + move[1]) and (not self.board.fields[self.y + move[0]][self.x + move[1]] == EMPTY_FIELD) and get_piece_color(self.board.fields[self.y + move[0]][self.x + move[1]]) == get_opponent_color(self.color)):
                    legal_moves.append(self.board.evaluate_move(self.piece, self.x, self.y, move))

        legal_moves += self.get_el_passant_moves(self.board)

        return legal_moves

    def get_el_passant_moves(self, board):

        if (self.color == board.computer_color):
            moves = [[1, -1], [1,1]]

            for move in moves:
                if (is_on_the_board(self.y + move[0], self.x + move[1]) and board.fields[self.y + move[0]][self.x + move[1]] == EMPTY_FIELD):
                    if ((not board.fields[self.y][self.x + move[1]] == EMPTY_FIELD) and board.fields[self.y][self.x + move[1]] in PAWN and
                            get_piece_color(board.fields[self.y][self.x + move[1]]) == get_opponent_color(board.computer_color) and self.y == 4):
                        move_for_el_passant = convertor_from_position_to_char(self.x + move[1]) + str(2) + " " + convertor_from_position_to_char(self.x + move[1]) + str(4)
                        if (board.last_move == move_for_el_passant):
                            return [board.evaluate_move(self.piece, self.x, self.y, move)]
        else:
            moves = [[-1, -1], [-1, 1]]
            for move in moves:
                if (is_on_the_board(self.y + move[0], self.x + move[1]) and board.fields[self.y + move[0]][self.x + move[1]] == EMPTY_FIELD):
                    if ((not board.fields[self.y][self.x + move[1]] == EMPTY_FIELD) and board.fields[self.y][
                        self.x + move[1]] in PAWN and
                            get_piece_color(board.fields[self.y][self.x + move[1]]) == board.computer_color and self.y == 3):
                        move_for_el_passant = convertor_from_position_to_char(self.x + move[1]) + str(
                            7) + " " + convertor_from_position_to_char(self.x + move[1]) + str(5)
                        if (board.last_move == move_for_el_passant):
                            return [board.evaluate_move(self.piece, self.x, self.y, move)]

        return []

    def get_deep_copy(self):
        return Pawn(self.piece, self.x, self.y, self.board)
