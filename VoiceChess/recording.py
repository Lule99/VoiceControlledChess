import sounddevice
from scipy.io.wavfile import write


class VoiceRecorder:
    def __init__(self, seconds: int = 2,
                 samplerate: int = 44100,
                 channels: int = 2) -> None:
        self.seconds = seconds
        self.samplerate = samplerate
        self.channels = channels

    def recording(self):
        record_voice = sounddevice.rec(
            int(self.seconds * self.samplerate), samplerate=self.samplerate, channels=self.channels)
        sounddevice.wait()
        return record_voice

    def save(self, record_voice, path: str = "out.wav") -> None:
        write(path, self.samplerate, record_voice)
