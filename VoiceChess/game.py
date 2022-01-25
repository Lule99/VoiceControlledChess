import sys
from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox
from keras.models import load_model

from algorithm2 import *
from board_view import BoardView
from my_threads import Worker
from soundControll.recorder import *
import tensorflow as tf
from sound import Sound


class Game(QMainWindow):
    def __init__(self, settings):
        QMainWindow.__init__(self)
        self.settings = settings
        self.board = BoardView(settings)

        self._init_ui()

        self.threadpool = QtCore.QThreadPool()
        self.play()

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.board)

        self.setCentralWidget(self.board)
        self.setFixedSize(850, 865)
        self.icon = QtGui.QIcon("./Slicice/icon.png")
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Voice chess")

    def play(self):
        worker = Worker(self.logic)
        worker.signals.progress.connect(self.move)
        self.threadpool.start(worker)

    def logic(self, progress_callback):

        if (self.settings[1] == 0):
            choosed_level = 1
        elif (self.settings[1] == 1):
            choosed_level = 3
        else:
            choosed_level = 4

        if (self.settings[0] == 0):
            choosed_color = WHITE_COLOR
        else:
            choosed_color = BLACK_COLOR

        board = Board(choosed_color == BLACK_COLOR)
        idle_moves_counter = 0

        model = load_model('model.h5')

        recognizer = speech_recognition.Recognizer()

        counter = 0
        selekcija = ""
        odrediste = ""

        tf.compat.v1.disable_eager_execution()

        if choosed_color == WHITE_COLOR:
            while (counter < 2):
                try:
                    with speech_recognition.Microphone(sample_rate=22050) as mic:

                        recognizer.adjust_for_ambient_noise(mic, duration=0.6)
                        recognizer.pause_threshold = 0.8  # default 0.8
                        recognizer.non_speaking_duration = 0.25
                        print("Odredi polje[Izgovor Slovo_Cifra]:")
                        audio = recognizer.listen(mic, phrase_time_limit=7)
                        print("Obrada zvuka...")
                        start = datetime.datetime.now()

                        s = io.BytesIO(audio.get_wav_data())
                        segment = AudioSegment.from_raw(s, sample_width=audio.sample_width, frame_rate=audio.sample_rate, channels=1)
                        s.close()
                        audio: AudioSegment = pojacaj(segment)

                        words = silence.split_on_silence(audio, min_silence_len=100, silence_thresh=-16, keep_silence=400)

                        if len(words) == 2:
                            audio.export("soundControll/sample.wav")
                            words[0].export("soundControll/slovo.wav")
                            words[1].export("soundControll/broj.wav")

                        else:
                            count = 0
                            # for audF in words:
                            #     audF.export(count.__str__() + ".wav")
                            #     count += 1
                            print("Broj izdvojenih reci: ", len(words))
                            raise Exception("Greska u obradi zvuka")

                        # wave_plot()
                        slovo: AudioSegment = words[0]
                        cifra: AudioSegment = words[1]

                        final_slovo = prepare_for_cnn_old_way("slovo.wav")
                        final_cifra = prepare_for_cnn_old_way("broj.wav")

                        slovo = predict_letter(final_slovo)
                        broj = predict_number(final_cifra)

                        if counter == 0:
                            selekcija = slovo+broj
                        if counter == 1:
                            odrediste = slovo+broj
                        
                        counter += 1

                        if counter == 2:
                            new_board = move(selekcija+" "+odrediste, board)

                            if new_board == []:
                                counter = 0
                                continue
                            else:
                                board = new_board

                            progress_callback.emit(board)
                            Heuristic.write_player_move(board)
                            idle_moves_counter += 1

                except Exception as e:
                    print(e)
                    continue

            counter = 0

        while (True):
            if(self.settings[2] == 0):
                pieces_remaining = count_pieces(board)
                if (check_if_only_pawns_remaining(board)):
                    board = Heuristic.get_computer_move(
                        board, choosed_level + 2)
                else:
                    board = Heuristic.get_computer_move(board, choosed_level)
            else:
                pieces_remaining = count_pieces(board)
                if (choosed_color == WHITE_COLOR):
                    board = Algorithm2.simulation(
                        Node(board), model, BLACK_COLOR)
                else:
                    board = Algorithm2.simulation(
                        Node(board), model, WHITE_COLOR)

            if (Heuristic.check_if_it_is_tie()):
                poruka = QMessageBox
                odg = poruka.question(self, "", "Igra zavrsena, nereseno je!", poruka.Ok)
                if odg == poruka.Ok:
                    sys.exit()
                break
            if (board == -100000):
                poruka = QMessageBox
                odg = poruka.question(self, "", "Sah-mat, pobedili ste!", poruka.Ok)
                if odg == poruka.Ok:
                    sys.exit()
                break
            elif (board == 0):
                poruka = QMessageBox
                odg = poruka.question(self, "", "Igra zavrsena, nereseno je!", poruka.Ok)
                if odg == poruka.Ok:
                    sys.exit()
                break
            else:
                if (pieces_remaining == count_pieces(board)):
                    idle_moves_counter += 1
                    if (idle_moves_counter == 50):
                        poruka = QMessageBox
                        odg = poruka.question(self, "", "Igra zavrsena, nereseno je!", poruka.Ok)
                        if odg == poruka.Ok:
                            sys.exit()
                        break
                else:
                    idle_moves_counter = 0

                progress_callback.emit(board)

            possible_moves = board.get_possible_moves(choosed_color)
            if (len(possible_moves) == 0):
                if (board.check_if_it_is_check(choosed_color)):
                    poruka = QMessageBox
                    odg = poruka.question(self, "", "Igra zavrsena, izgubili ste!", poruka.Ok)
                    if odg == poruka.Ok:
                        sys.exit()
                    break
                else:
                    poruka = QMessageBox
                    odg = poruka.question(self, "", "Igra zavrsena, nereseno je!", poruka.Ok)
                    if odg == poruka.Ok:
                        sys.exit()
                    break
            else:
                if (board.check_if_it_is_check(choosed_color)):
                    poruka = QMessageBox
                    poruka.question(self, "", "Sah!", poruka.Ok)
                pieces_remaining = count_pieces(board)
                
                while (counter < 2):
                    try:
                        with speech_recognition.Microphone(sample_rate=22050) as mic:
                            recognizer.adjust_for_ambient_noise(mic, duration=0.6)
                            recognizer.pause_threshold = 0.8  # default 0.8
                            recognizer.non_speaking_duration = 0.25
                            if counter == 0:
                                input("Nastavi:\n>>")
                            print("Odredi polje[Izgovor Slovo_Cifra]:")
                            audio = recognizer.listen(mic, phrase_time_limit=7)
                            print("Obrada zvuka...")
                            start = datetime.datetime.now()

                            s = io.BytesIO(audio.get_wav_data())
                            segment = AudioSegment.from_raw(s, sample_width=audio.sample_width, frame_rate=audio.sample_rate, channels=1)
                            s.close()
                            audio: AudioSegment = pojacaj(segment)

                            words = silence.split_on_silence(audio, min_silence_len=150, silence_thresh=-16, keep_silence=400)

                            if len(words) == 2:
                                audio.export("soundControll/sample.wav")
                                words[0].export("soundControll/slovo.wav")
                                words[1].export("soundControll/broj.wav")

                            else:
                                count = 0
                                # for audF in words:
                                #     audF.export(count.__str__() + ".wav")
                                #     count += 1
                                print("Broj izdvojenih reci: ", len(words))
                                raise Exception("Greska u obradi zvuka")

                            # wave_plot()
                            slovo: AudioSegment = words[0]
                            cifra: AudioSegment = words[1]

                            final_slovo = prepare_for_cnn_old_way("slovo.wav")
                            final_cifra = prepare_for_cnn_old_way("broj.wav")

                            slovo = predict_letter(final_slovo)
                            broj = predict_number(final_cifra)

                            if counter == 0:
                                selekcija = slovo+broj
                            if counter == 1:
                                odrediste = slovo+broj
                            
                            counter += 1

                            if counter == 2:
                                new_board = move(selekcija + " " + odrediste, board)

                                if new_board == []:
                                    counter = 0
                                    continue
                                else:
                                    board = new_board

                                progress_callback.emit(board)
                                Heuristic.write_player_move(board)
                                idle_moves_counter += 1
                                
                    except Exception as e:
                        print(e)
                        continue

                counter = 0

                if (pieces_remaining == count_pieces(board)):
                    idle_moves_counter += 1
                    if (idle_moves_counter == 50):
                        poruka = QMessageBox
                        odg = poruka.question(self, "", "Igra zavrsena, nereseno je!", poruka.Ok)
                        if odg == poruka.Ok:
                            sys.exit()
                        break
                else:
                    idle_moves_counter = 0

                Heuristic.write_player_move(board)
                progress_callback.emit(board)

                if (Heuristic.check_if_it_is_tie()):
                    poruka = QMessageBox
                    odg = poruka.question(self, "", "Igra zavrsena zbog ponavljanja, nereseno je!", poruka.Ok)
                    if odg == poruka.Ok:
                        sys.exit()
                    break

    def move(self, board):
        self.board.move(board.fields)

