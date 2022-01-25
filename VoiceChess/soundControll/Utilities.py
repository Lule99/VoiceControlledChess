import os
import pickle
import random
import string
from pathlib import Path

import cv2
import librosa
import librosa.display
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from pydub import AudioSegment
from sklearn import model_selection as skms

from VoiceChess.soundControll.augmentations import pojacaj

"""
*   Podaci i putanja potrebni koristeni za procesiranje, augmentaciju i pripremu za i treniranje modela...
"""
# putanja do originalnih audio snimaka
AUDIO_DATASET_PATH = 'C:\\Users\\LUKA\\Desktop\\ChessSoundDataset\\'

# nazivi foldera originalnim audio sa uzorcima
users = ['Luka', 'Njegos', 'Keti', 'Jovana', 'Djordje', 'Basic', 'Nikola']

# struktura datoteke sa snimljenim audio fajlovima
folderi = ['1', '2', '3', '4', '5', '6', '7', '8', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# korisnici sa slabim intenzitetom audio fajlova, potrebno pojacati 30db [Augmentations.pojacaj()]
pojacajUsers = ['Luka', 'Nikola', 'Keti', 'Jovana']

# ~~~Klase
cifre = folderi[:8]
slova = folderi[8:]

# ~~~Data
img_size = 128  # Svaki mel_spectogram bice skaliran na 128x128
traning_data = []


def mp3_to_wav(path):
    """
    Originalni audio snimci u mp3 formatu, potrebno konvertovati u wav..
    :param path:
    :return:
    """
    wav_file = AudioSegment.from_mp3(path)
    wav_file = pojacaj(wav_file)
    wav_file.export(path[:-4] + ".wav")


def report():
    """
    Uvid u dataset nakon obrade podataka (balansiranost, broj uzoraka i sl...)
    :return:
    """
    dataset = {}
    for folder in folderi:
        count = len(os.listdir(get_mel_target_path(folder)))
        dataset[folder] = count

    mean = sum(dataset.values()) / len(dataset.keys())

    print(15 * '*' + "\nIzvestaj o datasetu:\n" + 15 * '*')
    print("\tMaximalno u klasi: " + max(dataset.values()).__str__())
    print("\tMinimalno u klasi: " + min(dataset.values()).__str__())
    print("\tProsecak broj po klasi: " + mean.__str__())
    print(15 * '*')
    for data in dataset.keys():
        total = dataset[data].__str__()
        diff = (dataset[data] - mean).__str__()
        rel = (dataset[data] / mean).__str__()

        total_str = total + " " if len(total) == 3 else total
        abs_str = diff if len(diff) == 6 else diff + (6 - len(diff)) * " "

        print("\tKlasa {0}:\t{1}\tuzoraka\t\t| Odstupa od proseka [Count-mean]:\t ABS: {2}\tREL: {3} % [mean]".format(
            data, total_str, abs_str, rel[:5]))
    print(15 * '*')


def randomize_name():
    """
    Svaki audiofajl dobija nasumicno ime
    :return:
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


def make_export_folder_if_not_exists(user):
    if not os.path.exists(AUDIO_DATASET_PATH + "GEN_WAV_" + user):
        for folder_name in folderi:
            new_waw = AUDIO_DATASET_PATH + "GEN_WAV_" + user + '\\' + folder_name
            Path(new_waw).mkdir(parents=True, exist_ok=True)


def make_mel_export_folder():
    if not os.path.exists(AUDIO_DATASET_PATH + "MELS"):
        for folder_name in folderi:
            new_mel = AUDIO_DATASET_PATH + "MELS\\" + folder_name
            Path(new_mel).mkdir(parents=True, exist_ok=True)


def get_mel_target_path(folder_name):
    return AUDIO_DATASET_PATH + "MELS\\" + folder_name


def dump_to_mel(file_name, import_path, dump_to_path):
    """
    Funkcija ulazni audio fajl transformise u mel spektogram...

    :param file_name:    naziv fajla koji se obradjuje
    :param import_path:  putanja na kojoj se nalazi ulazni audio fajl
    :param dump_to_path: folder gde ce se cuvati izlazni mel spectogram
    :return:
    """
    data, sr = librosa.load(import_path)

    fig = plt.figure(figsize=[1, 1])
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    s = librosa.feature.melspectrogram(y=data, sr=sr)
    librosa.display.specshow(librosa.power_to_db(s, ref=np.max), x_axis='time', y_axis='mel', fmin=50, fmax=280)

    # mel_path = dump_to_path + '\\' + file_name[:-4] + '.jpg'
    mel_path = dump_to_path + '/' + file_name[:-4] + '.jpg'
    plt.savefig(mel_path, dpi=500, bbox_inches='tight', pad_inches=0)

    plt.close()


def plot_time_series(data):
    """
    Uvid u snimljeni audio [ frekvencija/amplituda ]
    :param data:
    :return:
    """
    plt.figure(figsize=(14, 8))
    plt.title('Raw wave ')
    plt.ylabel('Amplitude')
    plt.plot(np.linspace(0, 1, len(data)), data)
    plt.show()


# ~~~~~~~~~~~~~~~~~~MODEL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def process_mels(mel_type_iterable):
    """
    1.  Svaki mel spektogram iz odgovarajuce klase se ucitava u BGR formatu (zbog OpenCv)
    2.  Vrsi se resize na Utilities.img_size, trenutno 128px maximalna memorija hardware-a
    3.  Normalizacija
    4.  Dodavanje u Utilities.traning_data - koji ce kasnije biti izmesan i podeljen na trening, test i validacioni skup...

    :param mel_type_iterable: Utilities.slova ili Utilities.cifre, da bi odvojeno tekla obrada podataka za cnn za slova i cnn za brojeve...
    :return:
    """
    print("Pravljenje trening podataka...")

    broken_mels = 0
    for cls in mel_type_iterable:
        path = get_mel_target_path(cls)
        class_num = mel_type_iterable.index(cls)
        for mel in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, mel))
                img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
                # plt.imshow(img_arr)
                # plt.show()
                img_arr = cv2.resize(img_arr, (img_size, img_size))
                img_arr = img_arr / 255.0
                # plt.imshow(img_arr)
                # plt.show()
                traning_data.append((img_arr, class_num))
            except Exception as e:
                broken_mels += 1

        print("Klasa [", cls, "] obradjena...")
    if broken_mels > 0:
        print("Neuspešno učitani mel-ovi: ", broken_mels)

    if (mel_type_iterable == cifre):
        save_np_data(make_numpy_arr(), "cifre")
    else:
        save_np_data(make_numpy_arr(), "slova")


def make_numpy_arr():
    """
    Po obradi mel_spec [vidi Utilities.process_mels()], trening podaci se nasumicni mesaju i dodaju u X[], a odgovarajuce labele u Y[]
    Reshape za prilagodjavanje ulaza u keras... tri kanala, slika u boji...
    :return:
    """
    print("Velicina trening seta: ", len(traning_data))
    # promesaj trening set...
    random.shuffle(traning_data)

    X = []
    y = []

    for img, label in traning_data:
        X.append(img)
        y.append(label)

    # u np array...
    X = np.array(X).reshape(-1, img_size, img_size, 3)
    y = np.array(y)

    return X, y


def save_np_data(tuple, to_save):
    """
    Izvoz pripremnjelni trening podataka iz [ Utilities.make_numpy_arr() ]
    :param tuple:  X,y podaci iz make_numpy_arr()
    :param to_save: cifre ili slova
    :return:
    """
    if not (to_save == "cifre" or to_save == "slova"):
        raise Exception("Los parametar za save!\n\t \"cifre/slova\" only")

    print("Saving ...")
    x_path = "X" + to_save + ".pickle"
    y_path = "y" + to_save + ".pickle"
    x, y = tuple
    out = open(x_path, "wb")
    pickle.dump(x, out, protocol=4)
    out.close()
    out = open(y_path, "wb")
    pickle.dump(y, out)
    out.close()
    print("Data saved")


def load_np_data(to_load):
    """

    :param to_load: cifre/slova , vidi Utilities.save_np_data()
    :return:
    """
    if not (to_load == "cifre" or to_load == "slova"):
        raise Exception("Los parametar za ucitavanje!\n\t \"cifre\"/\"slova\"")

    x_path = "X" + to_load + ".pickle"
    y_path = "y" + to_load + ".pickle"

    if x_path not in os.listdir() or y_path not in os.listdir():
        print(20 * "~", "\nObradjeni trening podaci ne postoje! Sledi procesiranje podataka...\n", 20 * "~")
        if to_load == "cifre":
            process_mels(cifre)
        else:
            process_mels(slova)

    print("Ucitavanje trening podataka...")
    load_x = open(x_path, "rb")
    x_res = pickle.load(load_x)
    load_x.close()
    load_y = open(y_path, "rb")
    y_res = pickle.load(load_y)
    load_y.close()
    print("Podaci ucitani...")
    print("Broj ucitanih instanci: ", len(x_res))
    return x_res, y_res


def load(to_load):
    """

    :param to_load: "cifre" / "slova"
    :return:
    """
    X, y = load_np_data(to_load)
    X, X_test, y, y_test = skms.train_test_split(X, y, test_size=0.1, random_state=42)

    return X, X_test, y, y_test


def gpu_check_CUDA(useCuda):
    """
    Aktivacija CUDA za brze treniranje
    :param useCuda: boolean T/F
    :return:
    """
    if useCuda:
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        print("Broj detektovanih GPU: ", len(physical_devices))
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
