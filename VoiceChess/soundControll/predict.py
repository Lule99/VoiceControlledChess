import cv2
import keras
import os

from pydub import AudioSegment

from Utilities import dump_to_mel, img_size, mp3_to_wav
from augmentations import pojacaj

klase_cifre = ['1', '2', '3', '4', '5', '6', '7', '8']
klase_slova = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

keti1  = "testData\\testKeti1.wav"
luka1  = "testData\\testLuka1.wav"
lukaA  = "testData\\testLukaA.wav"
lukaA1 = "testData\\testLukaA1.wav"
test   = "testData\\test.wav"

def prepare_input_sound(file_path):
    export_path = "testData\\mels"

    if "testData" not in os.listdir():
        os.makedirs(export_path)

    dump_to_mel("test.wav", file_path, export_path)

    file_path = os.path.join(export_path,"test.jpg")
    print(file_path)

    img_arr = cv2.imread(file_path)
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    # plt.imshow(img_arr)
    # plt.show()
    img_arr = cv2.resize(img_arr, (img_size, img_size))
    img_arr = img_arr / 255.0

    return img_arr.reshape(-1, img_size, img_size, 3)


def load_model(model_type):
    if model_type == "c":
        return keras.models.load_model("model_cifre.model")
    else:
        return keras.models.load_model("model_slova.model")

def to_wav():
    mp3_to_wav("C:\\Users\\LUKA\\Desktop\\b1.mp3")
    #mp3_to_wav("C:\\Users\\LUKA\\Desktop\\e.mp3")

def predict():
    model = load_model("c")
    prediction = model.predict([prepare_input_sound(test)])

    result = {}

    for cls in klase_cifre:
        result[cls] = prediction[0][klase_cifre.index(cls)]*100

    print(prediction)
    print(30*"*")
    print(result)

    print("*\n*\n*\nWinner: ", max(result, key=result.get))





if __name__ == "__main__":
    #to_wav()
    predict()