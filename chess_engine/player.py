from abc import ABC
from abc import abstractmethod

import chess
from chess import Board
from chess import Move

import random

class Player(ABC):
    def __init__(self, color : chess.Color):
        super().__init__()
        self.color : chess.Color = color
    
    def calculate_value(self, board : Board, map : dict[chess.PieceType,int]) -> int:
        total_value : int = 0
        for piece in board.piece_map().values():
            val = map.get(piece.piece_type, 0)
            
            if piece.color == self.color:
                total_value += val
            else:
                total_value -= val
        return total_value

    @abstractmethod
    def decide_move(self, board : Board) -> Move:
        pass

class RandomPlayer(Player):
    def decide_move(self, board : Board) -> Move:
        possible_moves = list(board.generate_legal_moves())
        return random.choice(possible_moves)

class SimplePlayer(Player):

    def decide_move(self, board : Board) -> Move:
        map : dict[chess.PieceType,int] = {
            chess.PAWN:1,
            chess.BISHOP:3,
            chess.KNIGHT:3,
            chess.ROOK:5,
            chess.QUEEN:9,
            chess.KING:100,
        }
        possible_moves = list(board.generate_legal_moves())
        best_value = None
        best_moves = []
        for move in possible_moves:
            board.push(move)
            value = self.calculate_value(board, map)
            if (not best_value) or (value > best_value):
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)
            board.pop()
        print(best_value)
        return random.choice(best_moves)

class AlphaBetaPlayer(Player):

    def __init__(self, color : chess.Color, depth : int):
        super().__init__(color)
        self.depth = depth
    
    def min_max_value(self, map, board : Board, depth, alpha, beta):
        if depth == 0:
            return (self.calculate_value(board, map), None)
        legalMoves = list(board.generate_legal_moves())
        best_move = None
        best_value = 0
        for move in legalMoves:
            succ_board = board.copy()
            succ_board.push(move)
            next_depth = depth - 1
            succ_value = self.min_max_value(map, succ_board, next_depth, alpha, beta)[0]
            if succ_board.turn == self.color:
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
            return (self.calculate_value(board, map), None)
        return (best_value, best_move)

    def decide_move(self, board : Board) -> Move:
        map : dict[chess.PieceType,int] = {
            chess.PAWN:1,
            chess.BISHOP:3,
            chess.KNIGHT:3,
            chess.ROOK:5,
            chess.QUEEN:9,
            chess.KING:100,
        }
        return self.min_max_value(map, board, self.depth, None, None)[1]