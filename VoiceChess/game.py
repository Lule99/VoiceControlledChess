import speech_recognition
from pydub import AudioSegment, silence
from soundControll.recorder import *

from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from board_view import BoardView
from my_threads import Worker
from recording import VoiceRecorder
from computerLogic import *
from algorithm2 import *
from keras.models import load_model


class Game(QMainWindow):
    def __init__(self, settings):
        QMainWindow.__init__(self)
        self.settings = settings
        self.board = BoardView(settings)
        self.voice_recorder = VoiceRecorder()

        self._init_ui()

        self.threadpool = QtCore.QThreadPool()
        self.play()

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.board)

        record_btn = QPushButton("Snimanje")
        record_btn.clicked.connect(self.recording)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        layout.addWidget(self.board)

        right_part = QWidget()
        v_layout = QVBoxLayout()
        v_layout.addWidget(record_btn)
        right_part.setLayout(v_layout)
        layout.addWidget(right_part)

        self.setCentralWidget(main_widget)
        self.setFixedSize(970, 865)
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

        if choosed_color == WHITE_COLOR:
            while (counter < 2):
                try:
                    with speech_recognition.Microphone(sample_rate=22050) as mic:

                        recognizer.adjust_for_ambient_noise(mic, duration=0.6)
                        recognizer.pause_threshold = 0.8  # default 0.8
                        recognizer.non_speaking_duration = 0.25
                        print("Pricaj")
                        audio = recognizer.listen(mic)
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
                            print(len(words))
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
                            board = move(selekcija+" "+odrediste)
                            if board == []:
                                counter = 0
                                continue

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
                print("Game ended tie because of third repeat of some situation..")
                break
            if (board == -100000):
                print("Checkmate! Congratulations, you won!")
                break
            elif (board == 0):
                print("Stalemate! Tie game..")
                break
            else:
                if (pieces_remaining == count_pieces(board)):
                    idle_moves_counter += 1
                    if (idle_moves_counter == 50):
                        print(
                            "Game ended tie because 50 moves are made without capturing any pieces..")
                        break
                else:
                    idle_moves_counter = 0

                progress_callback.emit(board)

            possible_moves = board.get_possible_moves(choosed_color)
            if (len(possible_moves) == 0):
                if (board.check_if_it_is_check(choosed_color)):
                    print("Checkmate! You lost..")
                    break
                else:
                    print("Stalemate! Tie game..")
                    break
            else:
                if (board.check_if_it_is_check(choosed_color)):
                    print("Check!\n")
                pieces_remaining = count_pieces(board)
                
                while (counter < 2):
                    try:
                        with speech_recognition.Microphone(sample_rate=22050) as mic:
                            recognizer.adjust_for_ambient_noise(mic, duration=0.6)
                            recognizer.pause_threshold = 0.8  # default 0.8
                            recognizer.non_speaking_duration = 0.25
                            print("Pricaj")
                            audio = recognizer.listen(mic)
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
                                print(len(words))
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
                                board = move(selekcija+" "+odrediste)
                                if board == []:
                                    counter = 0
                                    continue

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
                        print(
                            "Game ended tie because 50 moves are made without capturing any pieces..")
                        break
                else:
                    idle_moves_counter = 0

                Heuristic.write_player_move(board)
                progress_callback.emit(board)

                if (Heuristic.check_if_it_is_tie()):
                    print("Game ended tie because of third repeat of some situation..")
                    break

    def move(self, board):
        self.board.move(board.fields)

    def recording(self):
        voice_record = self.voice_recorder.recording()
        self.voice_recorder.save(voice_record)
