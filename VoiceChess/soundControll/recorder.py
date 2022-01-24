import datetime
import io
import os
import time

import cv2
import librosa.display
import matplotlib.figure
import numpy as np
import sounddevice
import speech_recognition
from matplotlib import pyplot as plt
from pydub import AudioSegment, silence
from scipy.io.wavfile import write
from Utilities import img_size, dump_to_mel
from augmentations import pojacaj
from predict import predict_letter, predict_number


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

                recognizer.adjust_for_ambient_noise(mic, duration=0.6)
                recognizer.pause_threshold = 0.8        #default 0.8
                recognizer.non_speaking_duration = 0.25
                print("Pricaj")
                audio = recognizer.listen(mic)
                print("Obrada zvuka...")
                start = datetime.datetime.now()



                s = io.BytesIO(audio.get_wav_data())
                segment = AudioSegment.from_raw(s,  sample_width=audio.sample_width, frame_rate=audio.sample_rate, channels=1)
                s.close()
                audio: AudioSegment = pojacaj(segment)

                words = silence.split_on_silence(audio, min_silence_len=150, silence_thresh=-16, keep_silence=400)

                if len(words) == 2:
                    audio.export("sample.wav")
                    words[0].export("slovo.wav")
                    words[1].export("broj.wav")

                else:
                    count = 0
                    for audF in words:
                        audF.export(count.__str__()+".wav")
                        count+=1
                    print(len(words))
                    raise Exception("Greska u obradi zvuka")

                #wave_plot()
                slovo:AudioSegment = words[0]
                cifra:AudioSegment = words[1]

                final_slovo = prepare_for_cnn(slovo)
                final_cifra = prepare_for_cnn(cifra)

                # final_slovo = prepare_for_cnn_old_way("slovo.wav")
                # final_cifra = prepare_for_cnn_old_way("broj.wav")

                predict_letter(final_slovo)
                predict_number(final_cifra)

                print("Vreme: ", datetime.datetime.now() - start)



                if input("0 za dalje:") != "0":
                    break




        except Exception as e:
            print(e)
            continue


def prepare_for_cnn(audio):
    # konvert za librosu
    data = np.array(audio.get_array_of_samples()).astype(np.float32)
    sr = 22050

    fig = plt.figure(figsize=[1, 1], dpi=500)
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    s = librosa.feature.melspectrogram(y=data, sr=sr)
    librosa.display.specshow(librosa.power_to_db(s, ref=np.max),
                             x_axis='time', y_axis='mel', fmin=50, fmax=280)

    figure: matplotlib.figure.Figure = plt.gcf()
    figure.set_dpi(500)
    # plt.savefig("mel", dpi=500)
    figure.canvas.draw()

    b = figure.axes[0].get_window_extent()
    img = np.array(figure.canvas.buffer_rgba())
    img = img[int(b.y0):int(b.y1), int(b.x0):int(b.x1), :]
    plt.close()
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    img = cv2.resize(img, (img_size, img_size))
    img = img / 255.0
    final_img = img.reshape(-1, img_size, img_size, 3)
    cv2.imwrite()

    return final_img

def prepare_for_cnn_old_way(file_path):
    export_path = "testData\\mels"

    if "testData" not in os.listdir():
        os.makedirs(export_path)

    dump_to_mel("test_"+file_path, file_path, export_path)

    file_path = os.path.join(export_path, "test_"+file_path[:-4]+".jpg")

    img_arr = cv2.imread(file_path)
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    img_arr = cv2.resize(img_arr, (img_size, img_size))
    img_arr = img_arr / 255.0

    return img_arr.reshape(-1, img_size, img_size, 3)



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