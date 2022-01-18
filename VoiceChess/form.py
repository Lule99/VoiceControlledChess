from PySide2 import QtWidgets


class SettingsForm(QtWidgets.QDialog):
    def __init__(self) -> None:
        super(SettingsForm, self).__init__()

        self.settings = [0, 0, 0]

        self.w = QtWidgets.QWidget()
        self.h1 = QtWidgets.QHBoxLayout()
        self.h2 = QtWidgets.QHBoxLayout()
        self.h3 = QtWidgets.QHBoxLayout()
        self.h4 = QtWidgets.QHBoxLayout()

        self.btn = QtWidgets.QPushButton("Potvrdi")
        self.h4.addWidget(self.btn)

        self.v = QtWidgets.QVBoxLayout()

        self.white = QtWidgets.QRadioButton("Beli")
        self.white.click()
        self.black = QtWidgets.QRadioButton("Crni")

        self.h1.addWidget(self.white)
        self.h1.addWidget(self.black)

        self.easy = QtWidgets.QRadioButton("Lako")
        self.easy.click()
        self.medium = QtWidgets.QRadioButton("Srednje")
        self.hard = QtWidgets.QRadioButton("Tesko")

        self.h2.addWidget(self.easy)
        self.h2.addWidget(self.medium)
        self.h2.addWidget(self.hard)

        self.minimax = QtWidgets.QRadioButton("Minimax")
        self.minimax.click()
        self.mcts = QtWidgets.QRadioButton("MCTS")

        self.h3.addWidget(self.minimax)
        self.h3.addWidget(self.mcts)

        self.color = QtWidgets.QGroupBox("Izaberite boju")
        self.color.setLayout(self.h1)

        self.level = QtWidgets.QGroupBox("Izaberite tezinu")
        self.level.setLayout(self.h2)

        self.alg = QtWidgets.QGroupBox("Algoritam")
        self.alg.setLayout(self.h3)

        self.v.addWidget(self.color)
        self.v.addWidget(self.level)
        self.v.addWidget(self.alg)
        self.v.addWidget(self.btn)
        self.setLayout(self.v)
        self.show()

        self.btn.clicked.connect(self.submit)

    def submit(self):

        if self.black.isChecked():
            self.settings[0] = 1

        if self.medium.isChecked():
            self.settings[1] = 1
        elif self.hard.isChecked():
            self.settings[1] = 2

        if self.mcts.isChecked():
            self.settings[2] = 1
        self.close()
        self.accept()
