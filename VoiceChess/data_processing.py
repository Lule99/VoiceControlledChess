import chess.pgn
import chess.engine
import numpy as np
import service


def load_data():
    inputs, outputs = [], []

    results = {'1/2-1/2': 0, '0-1': -1, '1-0': 1}
    counter = {'1/2-1/2': 0, '0-1': 0, '1-0': 0}

    pgn = open("./Data/lichess_db_standard_rated_2014-07.pgn")

    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        if counter['1/2-1/2'] >= 7000 and counter['0-1'] >= 7000 and counter['1-0'] >= 7000:
            break

        result = game.headers['Result']
        if result not in results:
            continue

        counter[result] += 1
        if counter[result] >= 7000:
            continue

        result = results[result]

        board = game.board()
        for i, move in enumerate(game.mainline_moves()):
            board.push(move)
            serialized_board = service.convert_board_to_matrix(board)
            inputs.append(serialized_board)
            outputs.append(result)

    np.savez('./Data/processed_data.npz', inputs, outputs)


load_data()
