from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from board import Board
from my_threads import Worker
from recording import VoiceRecorder


class Game(QMainWindow):
    def __init__(self, settings):
        QMainWindow.__init__(self)
        self.board = Board(settings)
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
        x = input("Unesite potez u obliku a2 a3...(x za kraj)>>")
        while x != "x":
            progress_callback.emit(x)
            x = input("Unesite potez u obliku a2 a3...(x za kraj)>>")

    def move(self, console_input):
        self.board.test_move(console_input)
        self.board.draw()

    def recording(self):
        voice_record = self.voice_recorder.recording()
        self.voice_recorder.save(voice_record)
