import math

import chess
from chess import Outcome
from chess import Board

from abc import ABC
from abc import abstractmethod

import chess_engine.chess_util as chess_util

def piece_evaluation(board: Board) -> float:
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

def center_evaluation(board : chess.Board) -> float:
    value = 0
    for square in board.piece_map().keys():
        piece : chess.Piece = board.piece_map()[square]
        centerDistance : float = math.dist(chess_util.square_to_coordinates(square), (4.5,4.5))
        distanceBonus : float = 1.0 / centerDistance
        if piece.color == board.turn:
            value += distanceBonus
        else:
            value -= distanceBonus

    return value

def aggression_evaluation(board : chess.Board) -> float:
    value = 0
    for square in board.piece_map().keys():
        piece : chess.Piece = board.piece_map()[square]
        # determine goal for file based on player color
        distance : float = abs(chess.square_rank(square) - (7.5 if piece.color == chess.WHITE else 0.5) )
        distanceBonus : float = 1.0 / distance
        if piece.color == board.turn:
            value += distanceBonus
        else:
            value -= distanceBonus

    return value

class Evaluator(ABC):

    def evaluate_outcome(self, outcome: Outcome) -> float:
        if outcome.winner is None:
            # The game is a draw.
            return 0

        # The current player must be the loser, which is infinitely bad.
        return -math.inf

    @abstractmethod
    def evaluate(self, board: Board) -> float:
        pass

class PiecewiseEvaluator(Evaluator):

    def evaluate(self, board: Board) -> float:
        outcome = board.outcome()
        if outcome is not None:
            return self.evaluate_outcome(outcome)

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

class FavorCenterEvaluator(Evaluator):

    def evaluate(self, board : chess.Board) -> float:
        outcome = board.outcome()
        if outcome is not None:
            return self.evaluate_outcome(outcome)

        return piece_evaluation(board) + 0.1 * center_evaluation(board)

class FavorAggressionEvaluator(Evaluator):

    def evaluate(self, board : chess.Board) -> float:
        outcome = board.outcome()
        if outcome is not None:
            return self.evaluate_outcome(outcome)

        return piece_evaluation(board) + 0.1 * aggression_evaluation(board)

class FavorAggression(Evaluator):
    def evaluate(self, board: chess.Board) -> float:
        outcome = board.outcome()
        if outcome is not None:
            return self.evaluate_outcome(outcome)

        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }

        value = 0
        for square in board.piece_map().keys():
            piece : chess.Piece = board.piece_map()[square]
            pieceValue = piece_values.get(piece.piece_type, 0)
            # determine goal for file based on player color
            distance : float = math.dist(chess_util.square_to_coordinates(square), (4.5, 7.5) if piece.color == chess.WHITE else (4.5, 0.5))
            distanceMultiplier : float = 1.0 + (0.1 / distance)
            pieceValue += distanceMultiplier
            if piece.color == board.turn:
                value += pieceValue
            else:
                value -= pieceValue

        return value