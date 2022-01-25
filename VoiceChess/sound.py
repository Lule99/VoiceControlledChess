from PySide2.QtMultimedia import QSound


class Sound:
    def __init__(self, path):
        self.sound_file = path

    def play(self):
        QSound.play(self.sound_file)
