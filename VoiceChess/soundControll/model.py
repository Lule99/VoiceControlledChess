from keras import *
from keras.models import *
from keras.layers import *
from Utilities import *



def run(to_load, useCuda):
    gpu_check_CUDA(useCuda)
    X, X_test, y, y_test = load(to_load)


    model = model_one(X)
    model.summary()
    model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    # model.fit(X, y, batch_size=64, epochs=10, validation_split=0.15, callbacks=[tensorboard])      mapiranje na logs za prikaz
    model.fit(X, y, batch_size=16, epochs=3, validation_split=0.15)

    print("Model successfully trained!")
    print("Running tests...")
    score = model.evaluate(X_test, y_test, verbose=1)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    model.save("model_"+to_load+".model")


def model_one(X):
    model = Sequential()
    model.add(Conv2D(16, (3, 3), input_shape=X.shape[1:],
                     data_format='channels_last'))  # [:1] iskljuciti broj elemenata np arr-a...
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Conv2D(128, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Flatten())
    model.add(Dense(256))  # alternativno 128 Ok
    model.add(Activation('relu'))
    # model.add(Dropout(0.15))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(8))
    model.add(Activation('sigmoid'))

    return model




