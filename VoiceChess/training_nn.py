import numpy as np
import os

from keras.applications import xception
import keras
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.layers import *

def get_binary(outputs):
    ret_val = np.zeros((len(outputs), 3))
    cnt = 0
    for output in outputs:
        if output == -1:
            ret_val[cnt][0] = 1
        elif output == 0:
            ret_val[cnt][1] = 1
        else:
            ret_val[cnt][2] = 1
        
        cnt += 1

    return ret_val

def my_model():
    my_model = keras.models.Sequential([
        Flatten(input_shape=(768, )),
        Dense(512, activation="relu"),
        Dropout(0.2),
        Dense(256, activation="relu"),
        Dropout(0.2),
        Dense(50, activation="relu"),
        Dropout(0.2),
        Dense(3, activation='softmax')])
    return my_model


data = np.load('./Data/processed_data.npz')
inputs = data['arr_0']
outputs = data['arr_1']
outputs_binary = get_binary(outputs)

num_validation = 0.30
x_train, x_validation, y_train, y_validation = train_test_split(inputs, outputs_binary,
                                                                test_size=num_validation, random_state=3)

x_test = x_validation[len(x_validation) * 2 // 3:]
y_test = y_validation[len(y_validation) * 2 // 3:]
x_validation = x_validation[:len(x_validation) * 2 // 3]
y_validation = y_validation[:len(y_validation) * 2 // 3]

model = my_model()
model.summary()

model.compile(loss=keras.losses.categorical_crossentropy, optimizer='adam', metrics=['accuracy'])

es_callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)

history = model.fit(x_train, y_train, epochs=20, verbose=1, callbacks=[es_callback],
                    validation_data=(x_validation, y_validation))

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

model.save("model.h5")
print("Saved model to disk")