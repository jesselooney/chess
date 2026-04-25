# mcts: selection -> expansion -> simulation -> backpropagation
import random
import chess
from chess import Board, Move

piece_values: dict[chess.PieceType, int] = {
    chess.PAWN: 1,
    chess.BISHOP: 3,
    chess.KNIGHT: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 100,
}

class State:
    def __init__(self, value, board, player):
        self.value = value
        self.moves = board.legal_moves
        self.board = board
        self.player = player  # this is whether we are black or white
        # something to keep track of whether it is this agents turn or not?

    def is_terminal(self):
        if self.board.is_checkmate():
            return True
        if self.board.is_stalemate():
            return True
        if len(self.moves) == 0:
            return True
        return False

    def reward(self):
        if self.board.is_stalemate():
            return 50
        if self.board.is_checkmate():
            if self.board.outcome().winner == self.player:
                return 100
            else:
                return 0
            # determine which player won the game? agent or opponent...
        else:
            total_value: int = 0
            for piece in self.board.piece_map().values():
                val = piece_values.get(piece.piece_type, 0)

                if piece.color == self.player:
                    total_value += val
                else:
                    total_value -= val
            return total_value
        # the rest tbd for the recursive steps i sppose

    def next_state(self, move):
        # do we have to only do next state when it is our turn? i think that is handled by the tree imo...
        next = State(self.value, self.board.push(move), self.player)
        return next


# keep track of visited nodes so we don't loop infinitely
class Node:
    def __init__(self, state, parent=None):
        self.visited = False  # or does the visited-ness tracker go in states?
        self.reward = 0.0
        self.state = state
        self.children = []
        self.parent = parent
        self.untried_actions = (
            self.state.moves
        )  # need to copy this because we will be adding/removing?

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)

    def update(self, reward):
        self.reward += reward

    def is_expanded(self):
        if len(self.untried_actions) == 0:
            return True
        return False
    
    def expand(self):
        pass

    def rollout(self):
        # random rollout policy for now
        current_state = self.state
        while not current_state.is_terminal():
            current_state = current_state.next_state(random.choice(current_state.moves))
        return current_state.reward()

    def backpropagate(self):
        pass

    def best_child(self):
        best_score = 0.0
        best_child = []
        for child in self.children:
            score = child.reward / child.visited  # or some other scoring function?
            if score == best_score:
                best_child.append(child)
            if score > best_score:
                best_score = score
                best_child = [child]
        return random.choice(best_child)
    # using bestness polcy or random rollout policy?? not entirely sure how these two interact
    # i think we need to have the rollouts simulated here or perhaps when we expand

    # non-class based rollout policy and tree policy or do those go in here to dictate how rollout, etc, function
