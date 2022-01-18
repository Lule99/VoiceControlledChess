from PySide2.QtMultimedia import QSound


class Sound:
    def __init__(self):
        self.sound_file = "./move.wav"

    def play(self):
        QSound.play(self.sound_file)
