from dataclasses import dataclass
import math
import random

from chess import Board, Move

from chess_engine.evaluations import Evaluator
from chess_engine.player import Player


@dataclass
class Node:
    board: Board
    parent: Node | None
    last_move: Move | None
    children: list[Node]
    unexplored_moves: list[Move]
    visit_count: int
    total_reward: float

    @classmethod
    def new(self, board: Board):
        return Node(
            board=board,
            parent=None,
            last_move=None,
            children=[],
            unexplored_moves=list(board.legal_moves),
            visit_count=0,
            total_reward=0,
        )

    def explore_move(self, move: Move) -> Node:
        new_board = self.board.copy()
        new_board.push(move)

        child = Node(
            board=new_board,
            parent=self,
            last_move=move,
            children=[],
            unexplored_moves=list(new_board.legal_moves),
            visit_count=0,
            total_reward=0,
        )

        self.unexplored_moves.remove(move)
        self.children.append(child)

        return child

    def observe_reward(self, reward: float):
        self.total_reward += reward
        self.visit_count += 1


def ucb1(parent: Node, child: Node, c: float) -> float:
    return (child.total_reward / child.visit_count) + c * math.sqrt(
        2 * math.log(parent.visit_count) / child.visit_count
    )


class MCTSPlayer(Player):
    def __init__(
        self,
        evaluator: Evaluator,
        rollout_count: int,
        rollout_max_depth: int | None = None,
    ):
        super().__init__()

        self.evaluator: Evaluator = evaluator

        self.rollout_count: int = rollout_count

        if rollout_max_depth is None:
            self.rollout_max_depth: float = math.inf
        else:
            assert rollout_max_depth >= 0
            self.rollout_max_depth: float = rollout_max_depth

    def decide_move(self, board: Board) -> Move | None:
        # TODO: Preserve part of the tree across calls?
        root = Node.new(board)
        for _ in range(self.rollout_count):
            node = self.tree_policy(root)
            reward = self.rollout(node.board.copy())
            self.back_propagate(node, reward)
        return self.best_child(root).last_move

    def tree_policy(self, node: Node) -> Node:
        while node.unexplored_moves or node.children:
            if node.unexplored_moves:
                return self.expand_node(node)
            else:
                node = self.best_child(node)
        return node

    def expand_node(self, node: Node) -> Node:
        # TODO: How to select an action?
        move = random.choice(node.unexplored_moves)
        return node.explore_move(move)

    def best_child(self, parent: Node) -> Node:
        # TODO: Factor out the child heuristic as a parameter.
        def heuristic(child: Node) -> float:
            # We use the constant suggested in Browne et al. "A Survey of MCTS Methods"
            c = 1 / math.sqrt(2)
            return ucb1(parent, child, c)

        # TODO: How to break ties?
        return max(parent.children, key=heuristic)

    def rollout(self, board: Board) -> float:
        # TODO: Factor out rollout policy as a parameter.
        my_color = board.turn

        depth = 0
        while (moves := list(board.legal_moves)) and depth < self.rollout_max_depth:
            move = random.choice(moves)
            board.push(move)
            depth += 1

        evaluation = self.evaluator.evaluate(board)

        if board.turn != my_color:
            evaluation *= -1

        return evaluation

    def back_propagate(self, node: Node, reward: float):
        node: Node | None = node
        while node is not None:
            node.observe_reward(reward)
            reward = -reward
            node = node.parent
