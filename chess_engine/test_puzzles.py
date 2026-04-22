import csv
from typing import Generator, Dict
from pathlib import Path

from chess import Board, Move

from chess_engine.evaluations import piecewise_evaluation
from chess_engine.negamax import NegamaxPlayer
from chess_engine.player import Player


def stream_csv_as_dicts(
    file_path: Path,
) -> Generator[Dict[str, str], None, None]:
    with file_path.open(mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for row in reader:
            yield dict(row)


def test_puzzle(player: Player, board: Board, moves: list[Move]) -> list[Move] | None:
    observed_moves = []
    pairs = zip(moves[::2], moves[1::2])
    for move, correct_response in pairs:
        board.push(move)
        observed_moves.append(move)

        observed_response = player.decide_move(board)

        if observed_response is None:
            return observed_moves

        board.push(observed_response)
        observed_moves.append(observed_response)

        if observed_response != correct_response and not board.is_checkmate():
            return observed_moves


def test_puzzles(player, puzzles_path: Path):
    correct_count = 0
    incorrect_count = 0
    for puzzle in stream_csv_as_dicts(puzzles_path):
        identifier = puzzle["PuzzleId"]
        fen = puzzle["FEN"]
        moves_str = puzzle["Moves"]

        board = Board(fen)
        moves = [Move.from_uci(uci_str) for uci_str in moves_str.split(" ")]

        observed_moves = test_puzzle(player, board, moves)

        if observed_moves is None:
            correct_count += 1
        else:
            incorrect_count += 1

            observed_moves_str = " ".join(move.uci() for move in observed_moves)
            print(f"""
            Failed puzzle {identifier}
                position: {fen}
                expected: {moves_str}
                observed: {observed_moves_str}
            """)

    print(f"correct: {correct_count}; incorrect: {incorrect_count}")


if __name__ == "__main__":
    player = NegamaxPlayer(piecewise_evaluation, 5)
    puzzles_path = Path("puzzles100.csv")
    test_puzzles(player, puzzles_path)
