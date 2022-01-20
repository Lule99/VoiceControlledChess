import numpy as np
import librosa
import soundfile as sf

"""
Dodavanje pozadinskog suma radi povecanja robusnosti konv mreze...
Na naziv fajla konkatenira se i stepen dodatog suma wn_rate!
"""
def add_white_noise(data, sr, input_path, wn_rate):
#    plot_time_series(data)
    wn = np.random.randn(len(data))
    data_wn = data + wn_rate * wn
#    plot_time_series(data_wn)
    sf.write(input_path[:-4]+"__white_noise_rate="+wn_rate.__str__()+".wav", data_wn, sr)


"""
Augmentacija visine tona. Konkatenira stepen korekcije visine tona [pitch_factor] na naziv ulaznog fajla.
"""
def cchange_pitch(data, sr, pitch_factor, wav_path):
    data_aug = librosa.effects.pitch_shift(data, sr, pitch_factor)
    sf.write(wav_path[:-4]+"__Change_Pitch_factor="+pitch_factor.__str__()+".wav", data_aug, sr)


"""
Augmentacija brzine. Konkatenira stepen ubrzanja [speed_factor] na naziv ulaznog fajla.
"""
def speed_augment(data, sr, speed_factor, wav_path,):
    data_aug = librosa.effects.time_stretch(data, speed_factor)
    sf.write(wav_path[:-4]+"__Speed__factor="+speed_factor.__str__()+".wav",data_aug, sr)


"""
Za tihe snimke, losijeg kvaliteta, pojacavanje za 30 db fiksno.
"""
def pojacaj(wavFile):
    return wavFile.apply_gain(30)
