import datetime
from augmentations import *
from Utilities import *
import librosa
import librosa.display
import numpy as np
from matplotlib import pyplot as plt
from pydub import AudioSegment


def main():
    begin = datetime.datetime.now()
    print("----------------------------------------------------\nPocetak: ", begin)
    to_wav()
    augment()
    to_mel()
    report()
    end = datetime.datetime.now()
    print("----------------------------------------------------\nKraj: ", end)
    print("*\n*\n*\n*** Trajanje: ", end - begin)


def to_wav():
    for user in users:
        make_export_folder_if_not_exists(user)
        print("Folder: " + user)
        for folder_name in folderi:
            print('\t\tObrada: ' + folder_name)
            folder_path = AUDIO_DATASET_PATH + user + "\\" + folder_name + "\\"
            for file in os.listdir(folder_path):
                import_dest = folder_path + file
                export_dest = AUDIO_DATASET_PATH + "GEN_WAV_" + user + '\\' + folder_name + '\\' + folder_name + "___" + randomize_name() + ".wav"
                wav_file = AudioSegment.from_mp3(import_dest)

                if user in pojacajUsers:
                    wav_file = pojacaj(wav_file)

                wav_file.export(export_dest)


def dump_to_mel(file_name, import_path, dump_to_path):
    data, sr = librosa.load(import_path)

    fig = plt.figure(figsize=[1, 1])
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    s = librosa.feature.melspectrogram(y=data, sr=sr)
    librosa.display.specshow(librosa.power_to_db(s, ref=np.max), x_axis='time', y_axis='mel', fmin=50, fmax=280)

    mel_path = dump_to_path + '\\' + file_name[:-4] + '.jpg'
    plt.savefig(mel_path, dpi=500, bbox_inches='tight', pad_inches=0)

    plt.close()


def to_mel():
    print('Generisanje mel spektrograma:\n')

    make_mel_export_folder()

    for user in users:
        print("Folder: " + user)
        for folder in folderi:
            print('\t\tObrada: ' + folder)
            current_wav_folder = AUDIO_DATASET_PATH + 'GEN_WAV_' + user + "\\" + folder
            dump_to_path = get_mel_target_path(folder)
            for wav_file in os.listdir(current_wav_folder):
                wav_path = current_wav_folder + "\\" + wav_file
                dump_to_mel(wav_file, wav_path, dump_to_path)


def augment():
    print('Augmentacija:\n')

    for user in users:
        print("Folder: " + user)
        for folder in folderi:
            print('\t\tObrada: ' + folder)
            current_wav_folder = AUDIO_DATASET_PATH + 'GEN_WAV_' + user + "\\" + folder
            for wav_file in os.listdir(current_wav_folder):
                wav_path = current_wav_folder + "\\" + wav_file
                data, sr = librosa.load(wav_path)
                add_white_noise(data, sr, wav_path, 0.005)
                add_white_noise(data, sr, wav_path, 0.01)
                add_white_noise(data, sr, wav_path, 0.025)
                cchange_pitch(data, sr, -1.5, wav_path)
                cchange_pitch(data, sr, -2.5, wav_path)
                cchange_pitch(data, sr, 1.5, wav_path)
                cchange_pitch(data, sr, 2.5, wav_path)
                speed_augment(data, sr, 0.75, wav_path)
                speed_augment(data, sr, 1.5, wav_path)
                speed_augment(data, sr, 1.75, wav_path)


if __name__ == "__main__":
    main()
