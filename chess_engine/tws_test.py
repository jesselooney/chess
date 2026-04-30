import chess

import chess_engine.player as player
import chess_engine.negamax as negamax
import chess_engine.evaluations as evaluations

from collections import Counter

print(
    "Welcome to terminal chess. Use standard algebraic notation (SAN) to control the board. Use Ctrl+D to exit the REPL."
)


players = {
    chess.WHITE: negamax.NegamaxPlayer(evaluations.FavorAggressionEvaluator(), 2),
    chess.BLACK: negamax.NegamaxPlayer(evaluations.FavorCenterEvaluator(), 2),
}

scores = Counter()


def play_game(players: dict[chess.Color, player.Player]) -> chess.Outcome:
    board = chess.Board()

    outcome = None

    while True:
        print("-" * 15)
        print(board)
        white_eval = players[chess.WHITE].evaluator.evaluate(board)
        black_eval = players[chess.BLACK].evaluator.evaluate(board)
        if board.turn == chess.BLACK:
            white_eval *= -1
            black_eval *= -1
        print("WHITE: " + str(white_eval))
        print("BLACK: " + str(black_eval))
        print("-" * 15)

        current_player: player.Player = players[board.turn]

        move = current_player.decide_move(board)

        try:
            board.push(move)
        except chess.InvalidMoveError:
            print("Error: Invalid SAN string.")
        except chess.IllegalMoveError:
            print("Error: Illegal move.")
        except chess.AmbiguousMoveError:
            print("Error: Ambiguous move.")
        outcome = board.outcome()
        if outcome is not None:
            break
    print(outcome)

    print("-" * 15)
    print(board)
    print("-" * 15)

    return outcome


for x in range(100):
    outcome = play_game(players)
    scores[outcome.winner] += 1

print(scores)
