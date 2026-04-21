import sys

import chess

print(
    "Welcome to terminal chess. Use standard algebraic notation (SAN) to control the board. Use Ctrl+D to exit the REPL."
)

board = chess.Board()

while True:
    print("-" * 15)
    print(board)
    print("-" * 15)

    try:
        command = input("> ")
    except KeyboardInterrupt:
        print()
        continue
    except EOFError:
        sys.exit(0)

    if command == "u":
        try:
            board.pop()
        except IndexError:
            pass
    else:
        move_san = command
        try:
            board.push_san(move_san)
        except chess.InvalidMoveError:
            print("Error: Invalid SAN string.")
        except chess.IllegalMoveError:
            print("Error: Illegal move.")
        except chess.AmbiguousMoveError:
            print("Error: Ambiguous move.")
