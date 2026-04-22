import math

import chess


def outcome_evaluation(outcome: chess.Outcome) -> float:
    if outcome.winner is None:
        # The game is a draw.
        return 0

    # The current player must be the loser, which is infinitely bad.
    return -math.inf


def piecewise_evaluation(board: chess.Board) -> float:
    outcome = board.outcome()
    if outcome is not None:
        return outcome_evaluation(outcome)

    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }

    value = 0
    for piece in board.piece_map().values():
        pieceValue = piece_values.get(piece.piece_type, 0)
        if piece.color == board.turn:
            value += pieceValue
        else:
            value -= pieceValue

    return value
