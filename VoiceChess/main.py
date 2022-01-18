import sys
from PySide2.QtWidgets import QApplication
from form import SettingsForm
from game import Game


if __name__ == "__main__":
    app = QApplication(sys.argv)

    form = SettingsForm()
    form.setWindowTitle("Podesavanja")

    if form.exec_():
        game = Game(form.settings)
        game.show()

    sys.exit(app.exec_())
