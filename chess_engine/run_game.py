import math

import chess

from chess_engine.evaluations import piecewise_evaluation
from chess_engine.negamax import NegamaxPlayer
import chess_engine.player as player


def play_game(board: chess.Board, players: list[player.Player]) -> chess.Outcome:
    current_player = 0
    while not board.is_game_over():
        print("-" * 15)
        print(board)
        print("-" * 15)

        move = players[current_player].decide_move(board)
        print(move)
        board.push(move)
        current_player = (current_player + 1) % len(players)

    return board.outcome()


if __name__ == "__main__":
    board = chess.Board()

    user = player.UserPlayer()
    random = player.RandomPlayer()
    alphaBeta = player.AlphaBetaPlayer(4)
    negamax = NegamaxPlayer(piecewise_evaluation, 4)

    outcome = play_game(board, [user, negamax])

    print(outcome)

