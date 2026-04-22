# mcts: selection -> expansion -> simulation -> backpropagation


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

        # the rest tbd for the recursive steps i sppose

    def next_state(self, move):
        pass


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

    def rollout(self):
        # based on rollout policy -> tbd
        pass

    def backpropagate(self):
        pass

    def best_child(self):
        pass

    # non-class based rollout policy and tree policy or do those go in here to dictate how rollout, etc, function
