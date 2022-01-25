import os

import cv2
import keras

from VoiceChess.soundControll.Utilities import dump_to_mel, img_size

klase_cifre = ['1', '2', '3', '4', '5', '6', '7', '8']
klase_slova = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


def prepare_input_sound(file_path):
    """
    Interno testiranje! ne koristi se u produkciji.
    Funkcija priprema ulazne podatke za model...
    :param file_path:
    :return:
    """
    export_path = "testData\\mels"

    if "testData" not in os.listdir():
        os.makedirs(export_path)

    dump_to_mel("test.wav", file_path, export_path)

    file_path = os.path.join(export_path, "test.jpg")
    print(file_path)

    img_arr = cv2.imread(file_path)
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    # plt.imshow(img_arr)
    # plt.show()
    img_arr = cv2.resize(img_arr, (img_size, img_size))
    img_arr = img_arr / 255.0

    return img_arr.reshape(-1, img_size, img_size, 3)


def load_model(model_type):
    """
    Ucitavanje modela cifre/slova
    :param model_type: c/s
    :return:
    """
    if model_type == "c":
        return keras.models.load_model("soundControll/model_cifre.model")
        # return keras.models.load_model("model_cifre.model")
    else:
        return keras.models.load_model("soundControll/model_slova.model")
        # return keras.models.load_model("model_slova.model")


def predict():
    """
    Funkcija korstena za interno testiranje modela kako cifri tako i slova...
    :return:
    """
    model = load_model("c")
    prediction = model.predict([prepare_input_sound("VoiceChess/soundControll/testData/test.wav")])

    result = {}

    for cls in klase_cifre:
        result[cls] = prediction[0][klase_cifre.index(cls)] * 100

    #print(prediction)
    print(30 * "*")
    print(result)

    print("*\n*\n*\nWinner: ", max(result, key=result.get))


def predict_number(img):
    """
    Predikcija cifre
    :param img:
    :return:
    """
    model = load_model("c")
    prediction = model.predict(img)

    result = {}

    for cls in klase_cifre:
        result[cls] = prediction[0][klase_cifre.index(cls)] * 100

    #print(prediction)
    print(30 * "*")
    print(result)

    ret_val = max(result, key=result.get)

    print("*\n*\n*\nWinner: ", ret_val)
    return ret_val


def predict_letter(img):
    """
    Predikcija slova
    :param img:
    :return:
    """
    model = load_model("s")
    prediction = model.predict(img)

    result = {}

    for cls in klase_slova:
        result[cls] = prediction[0][klase_slova.index(cls)] * 100

    print(prediction)
    print(30 * "*")
    print(result)

    ret_val = max(result, key=result.get)

    print("*\n*\n*\nWinner: ", ret_val)

    return ret_val


if __name__ == "__main__":
    predict()
