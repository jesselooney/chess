from abc import ABC
from abc import abstractmethod

from chess import Board
from chess import Move

import random

class Player(ABC):
    @abstractmethod
    def decide_move(self, board : Board) -> Move:
        pass

class RandomPlayer(Player):
    def decide_move(self, board : Board) -> Move:
        possible_moves = list(board.generate_legal_moves())
        return random.choice(possible_moves)