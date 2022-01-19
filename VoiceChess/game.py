from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from board_view import BoardView
from my_threads import Worker
from recording import VoiceRecorder
from computerLogic import *


class Game(QMainWindow):
    def __init__(self, settings):
        QMainWindow.__init__(self)
        self.settings = settings
        self.board = BoardView(settings)
        self.voice_recorder = VoiceRecorder()

        self._init_ui()

        self.threadpool = QtCore.QThreadPool()
        self.play()

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.board)

        record_btn = QPushButton("Snimanje")
        record_btn.clicked.connect(self.recording)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        layout.addWidget(self.board)

        right_part = QWidget()
        v_layout = QVBoxLayout()
        v_layout.addWidget(record_btn)
        right_part.setLayout(v_layout)
        layout.addWidget(right_part)

        self.setCentralWidget(main_widget)
        self.setFixedSize(970, 865)
        self.icon = QtGui.QIcon("./Slicice/icon.png")
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Voice chess")

    def play(self):
        worker = Worker(self.logic)
        worker.signals.progress.connect(self.move)
        self.threadpool.start(worker)

    def logic(self, progress_callback):

        if (self.settings[1] == 0):
            choosed_level = 1
        elif (self.settings[1] == 1):
            choosed_level = 3
        else:
            choosed_level = 4

        if (self.settings[0] == 0):
            choosed_color = WHITE_COLOR
        else:
            choosed_color = BLACK_COLOR
                
        board = Board(choosed_color == 1)
        idle_moves_counter = 0

        if (choosed_color == WHITE_COLOR):
            board = get_player_move(board)
            progress_callback.emit(board)

            Heuristic.write_player_move(board)
            idle_moves_counter += 1

        while (True):
            pieces_remaining = count_pieces(board)
            if (check_if_only_pawns_remaining(board)):
                board = Heuristic.get_computer_move(board, choosed_level + 2) #ovde ces pozvati montecarlo ili minimax
            else:
                board = Heuristic.get_computer_move(board, choosed_level) #ovde ces pozvati montecarlo ili minimax
            if (Heuristic.check_if_it_is_tie()):
                print("Game ended tie because of third repeat of some situation..")
                break
            if (board == -100000):
                print("Checkmate! Congratulations, you won!")
                break
            elif (board == 0):
                print("Stalemate! Tie game..")
                break
            else:
                if (pieces_remaining == count_pieces(board)):
                    idle_moves_counter += 1
                    if (idle_moves_counter == 50):
                        print("Game ended tie because 50 moves are made without capturing any pieces..")
                        break
                else:
                    idle_moves_counter = 0

                progress_callback.emit(board)

            possible_moves = board.get_possible_moves(choosed_color)
            if (len(possible_moves) == 0):
                if (board.check_if_it_is_check(choosed_color)):
                    print("Checkmate! You lost..")
                    break
                else:
                    print("Stalemate! Tie game..")
                    break
            else:
                if (board.check_if_it_is_check(choosed_color)):
                    print("Check!\n")
                pieces_remaining = count_pieces(board)
                board = get_player_move(board)
                if (pieces_remaining == count_pieces(board)):
                    idle_moves_counter += 1
                    if (idle_moves_counter == 50):
                        print("Game ended tie because 50 moves are made without capturing any pieces..")
                        break
                else:
                    idle_moves_counter = 0

                Heuristic.write_player_move(board)
                progress_callback.emit(board)

                if (Heuristic.check_if_it_is_tie()):
                    print("Game ended tie because of third repeat of some situation..")
                    break

    def move(self, board):
        self.board.move(board.fields)

    def recording(self):
        voice_record = self.voice_recorder.recording()
        self.voice_recorder.save(voice_record)
