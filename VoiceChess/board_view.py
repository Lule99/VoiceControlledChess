from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QTableWidget, QLabel

from sound import Sound


class BoardView(QTableWidget):
    def __init__(self, settings) -> None:
        QTableWidget.__init__(self)
        self.setColumnCount(8)
        self.setRowCount(8)
        self.sound = Sound()
        self.settings = settings

        self.board = []
        self.horizontal_labels = []
        self.vertical_labels = []
        if settings[0] == 1:
            self.board = [
                ["R", "N", "B", "Q", "K", "B", "N", "R"],
                ["P", "P", "P", "P", "P", "P", "P", "P"],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                ["p", "p", "p", "p", "p", "p", "p", "p"],
                ["r", "n", "b", "q", "k", "b", "n", "r"]
            ]
            self.horizontal_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
            self.vertical_labels = ["8", "7", "6", "5", "4", "3", "2", "1"]
            # self.horizontal_labels = ["H", "G", "F", "E", "D", "C", "B", "A"]
            # self.vertical_labels = ["1", "2", "3", "4", "5", "6", "7", "8"]
        else:
            self.board = [
                ["r", "n", "b", "q", "k", "b", "n", "r"],
                ["p", "p", "p", "p", "p", "p", "p", "p"],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                ["P", "P", "P", "P", "P", "P", "P", "P"],
                ["R", "N", "B", "Q", "K", "B", "N", "R"]
            ]
            self.horizontal_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
            self.vertical_labels = ["8", "7", "6", "5", "4", "3", "2", "1"]

        self.draw(self.board)

    def draw(self, new_board_state):
        self.board = new_board_state
        for i in range(8):
            for j in range(8):
                field_color = "black"
                if ((i % 2 == 0) and (j % 2 == 0)) or ((i % 2 != 0) and (j % 2 != 0)):
                    field_color = "white"

                label = QLabel()
                pixmap = QtGui.QPixmap(
                    ("./Slicice/"+self.get_piece(field_color, self.board[i][j]))).scaled(100, 100, transformMode=QtCore.Qt.SmoothTransformation)
                label.setPixmap(pixmap)
                self.setCellWidget(i, j, label)

        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setStyleSheet(
            "padding: 0; font-weight: bold; font-size: 20px;")
        self.verticalHeader().setDefaultSectionSize(100)
        self.verticalHeader().setStyleSheet(
            "padding: 0;font-weight: bold; font-size: 20px;")
        self.setShowGrid(False)
        self.setHorizontalHeaderLabels(self.horizontal_labels)
        self.setVerticalHeaderLabels(self.vertical_labels)

    def get_piece(self, color, label):
        if label == ".":
            return color
        if label.islower():
            return color + "_" + label + label
        else:
            return color + "_" + label

    def move(self, board):
        self.draw(board)
        self.sound.play()

