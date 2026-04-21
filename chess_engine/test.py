import sys

import chess

from player import RandomPlayer

print(
    "Welcome to terminal chess. Use standard algebraic notation (SAN) to control the board. Use Ctrl+D to exit the REPL."
)

board = chess.Board()

randomPlayer = RandomPlayer()

while True:
    print("-" * 15)
    print(board)
    print("-" * 15)

    move = randomPlayer.decide_move(board)
    try:
        board.push(move)
    except chess.InvalidMoveError:
        print("Error: Invalid SAN string.")
    except chess.IllegalMoveError:
        print("Error: Illegal move.")
    except chess.AmbiguousMoveError:
        print("Error: Ambiguous move.")
    outcome = board.outcome()
    if outcome != None:
        break
print(outcome)