import datetime
import io
import os

import tensorflow as tf
import cv2
import librosa.display
import matplotlib.figure
import numpy as np
import speech_recognition
from matplotlib import pyplot as plt
from pydub import AudioSegment, silence
from speech_recognition import AudioData
from VoiceChess.soundControll.Utilities import img_size, dump_to_mel
from VoiceChess.soundControll.augmentations import pojacaj
from VoiceChess.soundControll.predict import predict_letter, predict_number


def my_record():
    """
    Snima i prepoznaje ulazni zvuk.
    Telo ove funkcije ugradjeno je i predstavlja glavnu petlju game.py
    :return:
    """
    recognizer = speech_recognition.Recognizer()

    tf.compat.v1.disable_eager_execution()

    while True:
        try:
            with speech_recognition.Microphone(sample_rate=22050) as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.6)
                recognizer.pause_threshold = 0.8  # default 0.8
                recognizer.non_speaking_duration = 0.25
                print("Pricaj")
                t = datetime.datetime.now()
                audio: AudioData = recognizer.listen(mic, phrase_time_limit=10)           # timeout=15, phrase_time_limit=3.5 ne vredi ako je dynamic_energy_threshold, jer sve tretira kao input...
                print("Obrada zvuka...")
                start = datetime.datetime.now()

                s = io.BytesIO(audio.get_wav_data())
                segment = AudioSegment.from_raw(s, sample_width=audio.sample_width, frame_rate=audio.sample_rate,
                                                channels=1)
                s.close()
                audio: AudioSegment = pojacaj(segment)

                # words = silence.split_on_silence(audio, min_silence_len=150, silence_thresh=-16, keep_silence=400)
                words = silence.split_on_silence(audio, min_silence_len=100, silence_thresh=-16, keep_silence=400)

                if len(words) == 2:
                    audio.export("sample.wav")
                    words[0].export("slovo.wav")
                    words[1].export("broj.wav")

                else:
                    count = 0
                    # Izvoz lose separatisanih reci:
                    for audF in words:
                        audF.export(count.__str__()+".wav")
                        count += 1
                    print("Broj izdvojanih reci: ", len(words))
                    print("time: ", datetime.datetime.now()-t)
                    raise Exception("Greska u obradi zvuka")

                # Za koristenje prepare_for_cnn() direktno bez snimanja na disk:

                # slovo: AudioSegment = words[0]
                # cifra: AudioSegment = words[1]

                # final_slovo = prepare_for_cnn(slovo)
                # final_cifra = prepare_for_cnn(cifra)

                # Sa snimanjem na disk:

                final_slovo = prepare_for_cnn_old_way("slovo.wav")
                final_cifra = prepare_for_cnn_old_way("broj.wav")

                slovo = predict_letter(final_slovo)
                broj = predict_number(final_cifra)

                print("Vreme: ", datetime.datetime.now() - start)
                print("Predikcija: ", slovo + broj)

                if input("0 za dalje:\n>>") != "0":
                    break

        except Exception as e:
            print(e)
            continue


def prepare_for_cnn(audio):
    """
    Procesiranje ulaznog audio fajla za ulaz u CNN. Bez cuvanja audia, spectograma itd na disk...
    Ulaz --> model direktno.

    :param audio: .wav file
    :return:
    """
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

    return final_img


def prepare_for_cnn_old_way(file_path):
    """
    Procesiranje ulaznog audio fajla za ulaz u CNN.

    :param file_path:  .wav file putanja
    :return:
    """
    export_path = "testData/mels"

    if "testData" not in os.listdir():
        os.makedirs(export_path)

    dump_to_mel("test_" + file_path, "" + file_path, export_path)

    file_path = os.path.join(export_path, "test_" + file_path[:-4] + ".jpg")

    img_arr = cv2.imread(file_path)
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    img_arr = cv2.resize(img_arr, (img_size, img_size))
    img_arr = img_arr / 255.0

    return img_arr.reshape(-1, img_size, img_size, 3)


def wave_plot():
    """
    Interna funkcija. Ne koristi se u produkciji.
    Koristeno za uvid u grafik snimljenog i segmentiranog snimka.

    :return:
    """
    data, sr = librosa.load(
        "C:\\Users\\LUKA\\PycharmProjects\\VoiceControlledChess\\VoiceChess\\soundControll\\sample.wav")
    plt.figure(figsize=[10, 5])
    librosa.display.waveplot(data, sr=sr)
    plt.xlabel("Vreme[s]")
    plt.ylabel("Amplituda")
    plt.show()
    data, sr = librosa.load(
        "C:\\Users\\LUKA\\PycharmProjects\\VoiceControlledChess\\VoiceChess\\soundControll\\slovo.wav")
    plt.figure(figsize=[10, 5])
    librosa.display.waveplot(data, sr=sr)
    plt.xlabel("Vreme[s]")
    plt.ylabel("Amplituda")
    plt.show()
    data, sr = librosa.load(
        "C:\\Users\\LUKA\\PycharmProjects\\VoiceControlledChess\\VoiceChess\\soundControll\\broj.wav")
    plt.figure(figsize=[10, 5])
    librosa.display.waveplot(data, sr=sr)
    plt.xlabel("Vreme[s]")
    plt.ylabel("Amplituda")
    plt.show()


if __name__ == "__main__":
    my_record()
