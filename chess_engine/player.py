import sys

from abc import ABC
from abc import abstractmethod

import chess
from chess import Board
from chess import Move

import random
import math

from chess_engine.evaluations import Evaluator


class Player(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def decide_move(self, board: Board) -> Move | None:
        pass


class UserPlayer(Player):
    def decide_move(self, board: Board) -> Move:
        while True:
            try:
                command = input("> ")
            except KeyboardInterrupt:
                sys.exit(0)

            try:
                move = board.parse_san(command)
                break
            except chess.InvalidMoveError:
                print("Error: Invalid SAN string.")
            except chess.IllegalMoveError:
                print("Error: Illegal move.")
            except chess.AmbiguousMoveError:
                print("Error: Ambiguous move.")
        return move


class RandomPlayer(Player):
    def decide_move(self, board: Board) -> Move:
        possible_moves = list(board.generate_legal_moves())
        return random.choice(possible_moves)


class EpsilonGreedyPlayer(Player):
    def __init__(self, policy: Player, epsilon: float):
        super().__init__()

        self.policy: Player = policy

        # A number in the range [0, 1] indicating the probability of making a
        # random move.
        self.epsilon: float = epsilon

    def decide_move(self, board: Board) -> Move:
        if random.random() < self.epsilon:
            # Make a random move.
            return random.choice(list(board.legal_moves))
        else:
            # Follow the policy.
            return self.policy.decide_move(board)


class SimplePlayer(Player):
    def __init__(self, evaluator: Evaluator):
        super().__init__()

        self.evaluator = evaluator

    def decide_move(self, board: Board) -> Move:
        possible_moves = list(board.generate_legal_moves())
        random.shuffle(possible_moves)
        best_value = -math.inf
        best_move = None
        for move in possible_moves:
            board.push(move)
            value = -self.evaluator.evaluate(board)
            board.pop()
            if (not best_move) or (value > best_value):
                best_value = value
                best_move = move
        return best_move


class AlphaBetaPlayer(Player):
    def __init__(self, evaluator: Evaluator, depth: int):
        super().__init__()

        self.evaluator = evaluator

        assert depth > 0
        self.depth = depth

    def min_max_value(
        self,
        piece_values: dict[chess.PieceType, int],
        board: Board,
        my_color: chess.Color,
        depth: int,
        alpha: int,
        beta: int,
    ) -> tuple[int, Move]:
        if depth == 0:
            return (self.evaluator.evaluate(board), None)
        legalMoves = list(board.generate_legal_moves())
        best_move = None
        best_value = 0
        for move in legalMoves:
            succ_board = board.copy()
            succ_board.push(move)
            next_depth = depth - 1
            succ_value = self.min_max_value(
                piece_values, succ_board, my_color, next_depth, alpha, beta
            )[0]
            if succ_board.turn == chess.WHITE:
                if (not best_move) or succ_value > best_value:
                    best_move = move
                    best_value = succ_value
                    if not alpha:
                        alpha = best_value
                    else:
                        alpha = max(alpha, best_value)
                if beta and best_value > beta:
                    return (best_value, best_move)
            else:
                if (not best_move) or succ_value < best_value:
                    best_move = move
                    best_value = succ_value
                    if not beta:
                        beta = best_value
                    else:
                        beta = min(beta, best_value)
                if alpha and best_value < alpha:
                    return (best_value, best_move)
        if not best_move:
            return (self.evaluator.evaluate(board), None)
        return (best_value, best_move)

    def decide_move(self, board: Board) -> Move:
        piece_values: dict[chess.PieceType, int] = {
            chess.PAWN: 1,
            chess.BISHOP: 3,
            chess.KNIGHT: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 100,
        }
        return self.min_max_value(
            piece_values, board, board.turn, self.depth, None, None
        )[1]
