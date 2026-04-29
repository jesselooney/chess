import math

import chess

def square_to_coordinates(square : chess.Square) -> tuple[int, int]:
    # Coordinate is (file, rank)
    return (chess.square_file(square), chess.square_rank(square))