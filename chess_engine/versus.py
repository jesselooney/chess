from argparse import ArgumentParser
from collections import defaultdict
from collections.abc import Mapping
from time import perf_counter

import chess
from chess import Board, Color

import chess_engine.evaluations as evaluations
from chess_engine.mcts import MCTSPlayer
from chess_engine.negamax import NegamaxPlayer
import chess_engine.player as player
from chess_engine.player import Player


PLAYERS = {
    "random": player.RandomPlayer(),
    "nega-pieces-1": NegamaxPlayer(evaluations.PiecewiseEvaluator(), 1),
    "nega-center-1": NegamaxPlayer(evaluations.FavorCenterEvaluator(), 1),
    "nega-aggro-1": NegamaxPlayer(evaluations.FavorAggressionEvaluator(), 1),
    "nega-attack-1": NegamaxPlayer(evaluations.FavorAttackEvaluator(), 1),
    "nega-pieces-2": NegamaxPlayer(evaluations.PiecewiseEvaluator(), 2),
    "nega-center-2": NegamaxPlayer(evaluations.FavorCenterEvaluator(), 2),
    "nega-aggro-2": NegamaxPlayer(evaluations.FavorAggressionEvaluator(), 2),
    "nega-attack-2": NegamaxPlayer(evaluations.FavorAttackEvaluator(), 2),
    "nega-pieces-3": NegamaxPlayer(evaluations.PiecewiseEvaluator(), 3),
    "nega-center-3": NegamaxPlayer(evaluations.FavorCenterEvaluator(), 3),
    "nega-aggro-3": NegamaxPlayer(evaluations.FavorAggressionEvaluator(), 3),
    "nega-attack-3": NegamaxPlayer(evaluations.FavorAttackEvaluator(), 3),
    "mcts-center-full-1000-random": MCTSPlayer(
        evaluations.PiecewiseEvaluator(), player.RandomPlayer(), 1000
    ),
    "mcts-center-10-10000-random": MCTSPlayer(
        evaluations.FavorCenterEvaluator(), player.RandomPlayer(), 10000, 10
    ),
    "mcts-center-05-10000-random": MCTSPlayer(
        evaluations.FavorCenterEvaluator(), player.RandomPlayer(), 10000, 5
    ),
    "mcts-center-10-10000-epsilon-75-nega-pieces-1": MCTSPlayer(
        evaluations.FavorCenterEvaluator(),
        player.EpsilonGreedyPlayer(
            NegamaxPlayer(evaluations.PiecewiseEvaluator(), 1), 0.75
        ),
        10000,
        10,
    ),
    "mcts-center-10-10000-epsilon-95-nega-pieces-1": MCTSPlayer(
        evaluations.FavorCenterEvaluator(),
        player.EpsilonGreedyPlayer(
            NegamaxPlayer(evaluations.PiecewiseEvaluator(), 1), 0.95
        ),
        10000,
        10,
    ),
    "mcts-center-05-10000-epsilon-75-nega-pieces-1": MCTSPlayer(
        evaluations.FavorCenterEvaluator(),
        player.EpsilonGreedyPlayer(
            NegamaxPlayer(evaluations.PiecewiseEvaluator(), 1), 0.75
        ),
        10000,
        5,
    ),
    "mcts-center-05-10000-epsilon-95-nega-pieces-1": MCTSPlayer(
        evaluations.FavorCenterEvaluator(),
        player.EpsilonGreedyPlayer(
            NegamaxPlayer(evaluations.PiecewiseEvaluator(), 1), 0.95
        ),
        10000,
        5,
    ),
}


def winner_to_str(winner: Color | None):
    return {
        chess.WHITE: "white",
        chess.BLACK: "black",
        None: "null",
    }[winner]


def play_game(players: Mapping[Color, Player]):
    move_count = 0
    move_counts = defaultdict(int)
    clocks = defaultdict(float)

    board = Board()

    print("-" * 15)
    print(board)
    print("-" * 15)

    while (outcome := board.outcome(claim_draw=True)) is None:
        if move_count >= 100:
            # Call the game a draw.
            return (move_counts, clocks, None, "hard_move_limit")

        current_player: Player = players[board.turn]

        start = perf_counter()
        move = current_player.decide_move(board)
        end = perf_counter()

        move_count += 1
        move_counts[board.turn] += 1
        clocks[board.turn] += end - start

        if move is None or not board.is_legal(move):
            print(f"illegal move attempted: {move}")
            # The other player wins immediately.
            return (move_counts, clocks, not board.turn, "illegal_move")

        board.push(move)

        print(str(move).center(15, "-"))
        print(board)
        print("-" * 15)

    return (move_counts, clocks, outcome.winner, outcome.termination.name.lower())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("white")
    parser.add_argument("black")

    args = parser.parse_args()

    white_player = args.white
    black_player = args.black

    players = {
        chess.WHITE: PLAYERS[white_player],
        chess.BLACK: PLAYERS[black_player],
    }

    move_counts, clocks, winner, reason = play_game(players)

    winner_str = winner_to_str(winner)

    white_moves = move_counts[chess.WHITE]
    black_moves = move_counts[chess.BLACK]

    white_clock = clocks[chess.WHITE]
    black_clock = clocks[chess.BLACK]

    print(
        f"white={white_player},black={black_player},winner={winner_str},reason={reason},white_moves={white_moves},black_moves={black_moves},white_clock={white_clock},black_clock={black_clock}"
    )
