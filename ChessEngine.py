"""
This class is responsible for storing all the information about the current state of a chess game. It will be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""
class GameState:
    """
    Used to create functionable chessboard
    """
    def __init__(self):
        self.board = [
            ["bR", "bN", 'bB', 'bQ', 'BK', "bB", 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ["wR", "wN", 'wB', 'wQ', 'wK', "wB", 'wN', 'wR']
        ]
        self.whiteToMove = True
        self.moveLog = []