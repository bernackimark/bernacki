from .slots_classes import Piece, Shape

default_pieces = [
    Piece(0, '*A*'), Piece(1, '*B*'), Piece(2, '*C*'), Piece(3, '*D*'),
    Piece(4, '*E*'), Piece(5, '*F*'), Piece(6, '*G*', 2), Piece(7, '***', 1, True),
    Piece(8, '*H*'), Piece(9, '*I*'),
]

default_shapes = [
    Shape('Three Reel Straight', [0, 0, 0], 2),
    Shape('Four Reel Straight', [0, 0, 0, 0], 4),
    Shape('Five Reel Straight', [0, 0, 0, 0, 0], 10),
    Shape('Lowercase W', [0, 1, 0, 1, 0]),
    Shape('Pyramid', [2, 1, 0, 1, 2]),
    Shape('Falling Profits', [2, 1, 0, 1, 2]),
    Shape('Uppercase W', [0, 2, 0, 2, 0]),
    Shape('Rising Profits', [2, 1, 1, 1, 0]),
    Shape('Middle Finger', [2, 2, 0, 2, 2]),
    Shape('Crown', [1, 2, 0, 2, 1]),
    Shape('Robot Face', [0, 2, 2, 2, 0]),
    Shape('Reverse REI Logo', [0, 1, 0, 1, 2]),
    Shape('Uppercase M', [2, 0, 2, 0, 2]),
    Shape('Space Invaders', [1, 0, 0, 0, 1]),
]
