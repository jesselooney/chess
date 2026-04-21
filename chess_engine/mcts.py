import chess

from chess import Board
from chess import Move

# mcts: selection -> expansion -> simulation -> backpropagation

class State():

    def __init__(self, value=0, moves = []):
        self.value = value
        self.moves=moves
        # something to keep track of whether it is this agents turn or not?

    def is_terminal(self):
        if len(self.moves) == 0:
            return True
        return False

    def reward(self):
        # tbd

    def next_state(self, move):
        # tbd

# keep track of visited nodes so we don't loop infinitely
class Node():

    def __init__(self, state, parent=None):
        self.visited = False # or does the visited-ness tracker go in states?
        self.reward = 0.0
        self.state = state
        self.children = []
        self.parent = parent
    
    def add_child(self, child_state):
        child = Node(child_State, self)
        self.children.append(child)

    def update(self, reward):
        self.reward += reward

    def is_expanded(self):
        # tbd

def tree_policy():
    # tbd