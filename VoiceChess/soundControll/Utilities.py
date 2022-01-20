import os
import random
import string
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np

AUDIO_DATASET_PATH = 'C:\\Users\\LUKA\\Desktop\\ChessSoundDataset\\'
folderi = ['1', '2', '3', '4', '5', '6', '7', '8', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
users = ['Luka', 'Njegos', 'Keti', 'Jovana', 'Djordje', 'Basic', 'Nikola']
pojacajUsers = ['Luka', 'Nikola', 'Keti', 'Jovana']


# users = ['Nikola']


def report():
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


def plot_time_series(data):
    plt.figure(figsize=(14, 8))
    plt.title('Raw wave ')
    plt.ylabel('Amplitude')
    plt.plot(np.linspace(0, 1, len(data)), data)
    plt.show()
