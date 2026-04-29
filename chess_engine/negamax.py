import math
import random
from typing import Callable

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

    moves = board.legal_moves

    value = -math.inf
    bestMove = None

    for move in moves:
        board.push(move)
        negamax_result = negamax(evaluator, board, depth - 1, -beta, -alpha)
        moveValue = -negamax_result[0]
        board.pop()

        if not bestMove:
            value = moveValue
            bestMove = move
        elif moveValue > value:
            value = moveValue
            bestMove = move
        elif moveValue == value and negamax_result[2] >= depth:
            value = moveValue
            bestMove = move
        elif moveValue == value and random.random() > 0.5:
            value = moveValue
            bestMove = move

        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return (value, bestMove, depth)


class NegamaxPlayer(player.Player):
    def __init__(self, evaluator: Evaluator, depth: int):
        super().__init__()

        self.evaluator = evaluator

        assert depth > 0
        self.depth = depth

    def decide_move(self, board: chess.Board) -> chess.Move | None:
        result = negamax(self.evaluator, board, self.depth, -math.inf, math.inf)
        print("Best score: " + str(result[0]))
        return result[1]
