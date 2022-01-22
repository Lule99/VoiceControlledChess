from datetime import datetime

import librosa.display

import model
from Utilities import *
from augmentations import *


def main():

    # begin = datetime.now()
    # print("----------------------------------------------------\nPocetak: ", begin)
    # to_wav()
    # augment()
    # to_mel()
    # report()
    # end = datetime.now()
    # print("----------------------------------------------------\nKraj: ", end)
    # print("*\n*\n*\n*** Trajanje: ", end - begin)
    # print("\nTRENING\n")
    # begin = datetime.now()
    # model.run("slova", False)
    # end = datetime.now()
    # print("----------------------------------------------------\nKraj: ", end)
    # print("*\n*\n*\n*** Trajanje: ", end - begin)
    # begin = datetime.now()
    # print("\nTRENING\n")
    # model.run("cifre", True)
    # end = datetime.now()
    # print("*\n*\n*\n*** Trajanje: ", end - begin)
    pass


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
