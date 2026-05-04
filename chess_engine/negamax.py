import math
import random

import chess

import chess_engine.player as player

from chess_engine.evaluations import Evaluator


def negamax(
    evaluator: Evaluator,
    board: chess.Board,
    depth: int,
    alpha: float,
    beta: float,
) -> tuple[float, chess.Move | None, int]:
    if depth == 0 or board.is_game_over():
        return (evaluator.evaluate(board), None, depth)

    moves = list(board.generate_legal_moves())

    random.shuffle(moves)

    value = -math.inf
    bestMove = None
    bestDepth = 0

    for move in moves:
        board.push(move)
        negamax_result = negamax(evaluator, board, depth - 1, -beta, -alpha)
        moveValue = -negamax_result[0]
        board.pop()

        if (
            not bestMove
            or moveValue > value
            or (moveValue == value and negamax_result[2] > bestDepth)
        ):
            value = moveValue
            bestMove = move
            bestDepth = negamax_result[2]

        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return (value, bestMove, bestDepth)


class NegamaxPlayer(player.Player):
    def __init__(self, evaluator: Evaluator, depth: int):
        super().__init__()

        self.evaluator = evaluator

        assert depth > 0
        self.depth = depth

    def decide_move(self, board: chess.Board) -> chess.Move | None:
        result = negamax(self.evaluator, board, self.depth, -math.inf, math.inf)
        return result[1]
