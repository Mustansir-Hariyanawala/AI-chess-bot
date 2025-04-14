import random
import random as rnd
from Moves import Move
from ChessEngine import GameState


piece_score = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
checkmate = 1000
stalemate = 0
dept = 3
def random_moves(valid_moves: list[Move]):
    return valid_moves[rnd.randint(0, (len(valid_moves) - 1))]

"""
Helper method to make first recursive call"""
def find_best_move_minmax(game_state: GameState, valid_moves):
    global next_move
    next_move = None
    find_move_minmax(game_state, valid_moves, game_state.whiteToMove, dept)
    return next_move

def find_negamax(game_state, valid_moves, depth, turn_multiplier):
    global next_move
    if depth == 0:
        return score_material(game_state.board)


def find_move_minmax(game_state: GameState, valid_moves: list[Move], white_to_move: bool, depth = dept):
    global next_move
    if depth == 0:
        return score_material(game_state)

    if white_to_move:
        max_score = -checkmate
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = find_move_minmax(game_state, next_moves, False, depth - 1)
            if score > max_score:
                max_score = score
                if depth == dept:
                    next_move = move
            game_state.undo_move()
        return max_score

    else:
        min_score = checkmate
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = find_move_minmax(game_state, next_moves, True, depth - 1)
            if score < min_score:
                min_score = score
                if depth == dept:
                    next_move = move
            game_state.undo_move()
        return min_score


def score_material(game_state: GameState, score_board = False):
    if score_board:
        multiplier = -1 if game_state.whiteToMove else 1
        if game_state.check_mate:
            return multiplier * checkmate
        elif game_state.stale_mate:
            return stalemate

    score = 0
    for row in game_state.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]

    return score
