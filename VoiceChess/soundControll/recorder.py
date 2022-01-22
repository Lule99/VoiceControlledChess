import io

import cv2
import librosa.display
import matplotlib.figure
import numpy as np
import sounddevice
import speech_recognition
from matplotlib import pyplot as plt
from pydub import AudioSegment, silence
from scipy.io.wavfile import write
from Utilities import img_size
from augmentations import pojacaj
from predict import predict_num, predict_letter


class VoiceRecorder:
    def __init__(self, seconds: int = 3,
                 samplerate: int = 22050,
                 channels: int = 2) -> None:
        self.seconds = seconds
        self.samplerate = samplerate
        self.channels = channels

    def recording(self):
        bla = input("Zapocni snimanje[press any key]...")
        record_voice = sounddevice.rec(
            int(self.seconds * self.samplerate), samplerate=self.samplerate, channels=self.channels)
        print("Recording started:")
        sounddevice.wait()
        return record_voice

    def save(self, record_voice, path: str = "out.wav") -> None:
        write(path, self.samplerate, record_voice)


def main():
    rec = VoiceRecorder()
    rec.save(rec.recording())



def my_record():

    recognizer = speech_recognition.Recognizer()


    while True:
        try:
            with speech_recognition.Microphone(sample_rate=22050) as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.01)
                print("Pricaj")
                audio = recognizer.listen(mic)


                s = io.BytesIO(audio.get_wav_data())
                segment = AudioSegment.from_raw(s,  sample_width=audio.sample_width, frame_rate=audio.sample_rate, channels=1)
                s.close()
                audio: AudioSegment = pojacaj(segment)

                words = silence.split_on_silence(audio, min_silence_len=100, silence_thresh=-16)

                if len(words) == 2:
                    audio.export("sample.wav")
                    words[0].export("slovo.wav")
                    words[1].export("broj.wav")

                else:
                    print("Greska u obradi zvuka")
                    break

                #wave_plot()
                slovo:AudioSegment = words[0]
                cifra:AudioSegment = words[1]

                #konvert za librosu
                data = np.array(slovo.get_array_of_samples()) .astype(np.float32)
                sr = 22050

                fig = plt.figure(figsize=[1, 1], dpi=500)
                ax = fig.add_subplot(111)
                ax.axes.get_xaxis().set_visible(False)
                ax.axes.get_yaxis().set_visible(False)
                ax.set_frame_on(False)

                s = librosa.feature.melspectrogram(y=data, sr=sr)
                librosa.display.specshow(librosa.power_to_db(s, ref=np.max),
                                         x_axis='time', y_axis='mel', fmin=50,fmax=280)

                figure: matplotlib.figure.Figure = plt.gcf()
                figure.set_dpi(500)
                plt.savefig("mel", dpi=500)
                figure.canvas.draw()

                b = figure.axes[0].get_window_extent()
                img = np.array(figure.canvas.buffer_rgba())
                img = img[int(b.y0):int(b.y1), int(b.x0):int(b.x1), :]
                plt.close("all")
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
                img = cv2.resize(img, (img_size, img_size))
                img = img/255.0
                final_img = img.reshape(-1, img_size, img_size, 3)

                predict_letter(final_img)



                if input("0 za dalje:") != "0":
                    break




        except Exception as e:
            print("greska")
            print(e)


def wave_plot():
    data, sr = librosa.load(
        "C:\\Users\\LUKA\\PycharmProjects\\VoiceControlledChess\\VoiceChess\\soundControll\\sample.wav")
    fig = plt.figure(figsize=[10, 5])
    librosa.display.waveplot(data, sr=sr)
    plt.xlabel("Vreme[s]")
    plt.ylabel("Amplituda")
    plt.show()
    data, sr = librosa.load(
        "C:\\Users\\LUKA\\PycharmProjects\\VoiceControlledChess\\VoiceChess\\soundControll\\slovo.wav")
    fig = plt.figure(figsize=[10, 5])
    librosa.display.waveplot(data, sr=sr)
    plt.xlabel("Vreme[s]")
    plt.ylabel("Amplituda")
    plt.show()
    data, sr = librosa.load(
        "C:\\Users\\LUKA\\PycharmProjects\\VoiceControlledChess\\VoiceChess\\soundControll\\broj.wav")
    fig = plt.figure(figsize=[10, 5])
    librosa.display.waveplot(data, sr=sr)
    plt.xlabel("Vreme[s]")
    plt.ylabel("Amplituda")
    plt.show()

if __name__ == "__main__":
    my_record()