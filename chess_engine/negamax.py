import math
from typing import Callable

import chess

import chess_engine.player as player


def negamax(evaluation: Callable[[chess.Board], float], board: chess.Board, depth: int, alpha: float, beta: float) -> tuple[float, chess.Move]:
    if depth == 0 or board.is_game_over():
        return (evaluation(board), None)
    
    moves = board.legal_moves

    value = -math.inf
    bestMove = None

    for move in moves:
        board.push(move)
        moveValue = -negamax(evaluation, board, depth - 1, -beta, -alpha)[0]
        board.pop()

        if moveValue > value:
            value = moveValue
            bestMove = move

        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return (value, bestMove)


class NegamaxPlayer(player.Player):
    def __init__(self, evaluation: Callable[[chess.Board], float], depth: int):
        super().__init__()

        self.evaluation = evaluation

        assert depth > 0
        self.depth = depth

    def decide_move(self, board: chess.Board) -> chess.Move:
        return negamax(self.evaluation, board, self.depth, -math.inf, math.inf)[1]

