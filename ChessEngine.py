"""
This class is responsible for storing all the information about the current state of a chess game. It will be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""
from decorator import append


class GameState:
    """
    Used to create functionable chessboard
    """
    def __init__(self):
        self.board = [
            ["bR", "bN", 'bB', 'bQ', 'bK', "bB", 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ["wR", "wN", 'wB', 'wQ', 'wK', "wB", 'wN', 'wR']
        ]

        self.move_function = {'p': self.get_pawn_moves,
                              'R': self.get_rook_moves,
                              'B': self.get_bishop_moves,
                              'N': self.get_knight_moves,
                              'Q': self.get_queen_moves,
                              'K': self.get_king_moves
                              }
        self.whiteToMove = True
        self.moveLog = []
        self.square_range = range(8)
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)
        self.is_in_check = False
        self.pins = []
        self.checks = []
        self.possible_enpassant = () #coordinate of en passant possible

        #castling
        self.white_castle_king_side = True
        self.white_castle_queen_side = True
        self.black_castle_king_side = True
        self.black_castle_queen_side = True
        self.castle_log = [CastleRights(self.white_castle_king_side, self.black_castle_king_side,
                                         self.white_castle_queen_side, self.black_castle_queen_side)]

    #takes moves as parameter and executes it (this will not work for castling, pawn promotion and en passant
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_move
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap player's turn
        if move.piece_move == 'wK':
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.piece_move == 'bK':
            self.black_king_loc = (move.end_row, move.end_col)
        #pawn promotion
        if move.pawn_promoted:
            promoted_piece = input("Promote to Q, R, B and N:")
            self.board[move.end_row][move.end_col] = move.piece_move[0] + promoted_piece
        #enpassant
        #update enpassant_possible variable
        if move.piece_move[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.possible_enpassant = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.possible_enpassant = ()

        if move.enpassant_move:
            self.board[move.start_col][move.end_col] = '--'


        #castling
        self.update_castle_rights(move)
        self.castle_log.append(CastleRights(self.white_castle_king_side, self.black_castle_king_side,
                                            self.white_castle_queen_side, self.black_castle_queen_side))

        if move.castle:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = \
                    self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = '--'
            else:
                self.board[move.end_row][move.end_col + 1] = \
                    self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = '--'

    def update_castle_rights(self, move):
        if move.piece_move == 'wk':
            self.white_castle_king_side = False
            self.white_castle_queen_side = False
        elif move.piece_move == 'bk':
            self.black_castle_king_side = False
            self.black_castle_queen_side = False
        elif move.piece_move == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:
                    self.white_castle_queen_side = False
                elif move.start_col == 7:
                    self.white_castle_king_side = False
        elif move.piece_move == 'bR':
            if move.start_row == 0:  # Black rooks start on row 0
                if move.start_col == 0:
                    self.black_castle_queen_side = False
                elif move.start_col == 7:
                    self.black_castle_king_side = False

    def undo_move(self):
        if len(self.moveLog) == 0:
            return
        move = self.moveLog.pop() #retrieving recent move
        self.board[move.start_row][move.start_col] = move.piece_move #place to be undoed
        self.board[move.end_row][move.end_col] = move.piece_captured #place captured pawn again
        self.whiteToMove = not self.whiteToMove #reswap player's turn
        if move.piece_move == 'wK':
            self.white_king_loc = (move.start_row, move.start_col)
        elif move.piece_move == 'bK':
            self.black_king_loc = (move.start_row, move.start_col)

        if move.enpassant_move:
            self.board[move.end_row][move.end_col] = '--'
            self.board[move.start_row][move.end_col] = move.piece_captured
            self.possible_enpassant = (move.end_row, move.end_col)
        #undo 2 square pawn advance

        if move.piece_move[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.possible_enpassant = ()

        self.castle_log.pop()
        castle_rights = self.castle_log[-1]
        self.white_castle_king_side = castle_rights.wks
        self.black_castle_king_side = castle_rights.bks
        self.white_castle_queen_side = castle_rights.wqs
        self.black_castle_queen_side = castle_rights.bqs

        if move.castle:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                self.board[move.end_row][move.end_col - 1] = '--'
            else:
                self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = '--'
    '''
    All moves considering checks
    '''
    def get_valid_moves(self):
        # temp_enpassant_possible = self.possible_enpassant

        moves = []
        #2.) for each move, check for pins, checks and if currently it's in check
        self.pins, self.checks, self.is_in_check = self.check_for_pins_and_checks()
        king_loc = self.white_king_loc if self.whiteToMove else self.black_king_loc
        king_row = king_loc[0]
        king_col = king_loc[1]
        #3.) if the king is in check,
        if self.is_in_check:
            if len(self.checks) == 1:
                moves = self.get_all_possible_move()
                check = self.checks[0]
                check_row = check[0]
                check_columns = check[1]
                piece_checking = self.board[check_row][check_columns]
                valid_square = []
                if piece_checking[1] == 'N':
                    valid_square.append((check_row, check_columns))
                else:
                    for i in range(1, 8):
                        valid_square.append((king_row + check[2] * i,
                                         king_col + check[3] * i))
                        if valid_square[0][0] == check_row and valid_square[0][1] == check_columns:
                            break
                #get rid of any moves that don't
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].piece_move[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_square:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_move()

        # self.possible_enpassant = temp_enpassant_possible
        return moves



    def check_for_pins_and_checks(self):
        pins = []
        check =[]
        is_in_check = False
        opponent = 'b' if self.whiteToMove else 'w'
        turn = 'w' if self.whiteToMove else 'b'
        row = self.white_king_loc[0] if self.whiteToMove \
            else self.black_king_loc[0]
        column = self.white_king_loc[1] if self.whiteToMove \
            else self.black_king_loc[1]
        pre_compute = ((0, -1), (-1, 0), (0, 1), (1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1))
        for j in range(len(pre_compute)):
            compute = pre_compute[j]
            possible_pin = ()
            for i in range(1, 8):
                r = row + compute[0] * i
                c = column + compute[1] * i
                if 0 <= r < 8 and 0 <= c < 8:
                    end_piece = self.board[r][c]
                    if end_piece[0] == turn:
                        if possible_pin == ():
                            possible_pin = (r, c, compute[0], compute[1])
                        else:
                            break
                    elif end_piece[0] == opponent:
                        types = end_piece[1]
                        """
                        5 possibilities here in this complex condition
                        1.) vertically and horizontally king exists
                        2.) diagonally bishop exists
                        3.) 1 square diagonally pawn exists
                        4.) in any 8 directions queen exists
                        5.) in any direction 1 square gap king exists
                        """
                        if(0 <= j <= 3 and types == 'R') or \
                            (4 <= j <= 7 and types == 'B') or \
                            (i == 1 and types == 'p' and ((opponent == 'w' and 6 <= j <= 7) or
                                                          (opponent == 'b' and 4 <= j <= 5))) or \
                            (types == 'Q') or \
                            (i == 1 and types == 'K'):
                            if possible_pin == (): # king is in check
                                is_in_check = True
                                check.append((r, c, compute[0], compute[1]))
                                break
                            else: #opponent pinning
                                pins.append(possible_pin)
                                break
                        else:#neither pinning nor checking
                            break
                else:#off board
                    break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            r = row + m[0]
            c = column + m[1]
            if 0 <= r < 8 and 0 <= c < 8:
                end_piece = self.board[r][c]
                if end_piece[0] == opponent and end_piece[1] == 'N':
                    is_in_check = True
                    check.append((r, c, m[0], m[1]))
        return pins, check, is_in_check




    """
    All moves without considering checks
    """

    def get_all_possible_move(self):
        moves = []
        for rows in self.square_range: #number of rows
            for cols in self.square_range:#number of columns
                turn = self.board[rows][cols][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[rows][cols][1]
                    self.move_function[piece](rows, cols, moves)
        return moves


    def get_pawn_moves(self, row, column, moves):
        piece_pinned = False
        pin_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piece_pinned = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove: #white to move
            move_amount = -1
            start_row = 6
            back_row = 0
            opponent = 'b'
        else:
            move_amount = 1
            start_row = 1
            back_row = 7
            opponent = 'w'

        pawn_promotion = False

        if self.board[row + move_amount][column] == '--':
            if not piece_pinned or pin_dir == (move_amount, 0):
                if row + move_amount == back_row:
                    pawn_promotion = True
                moves.append(Move((row, column), (row + move_amount, column),
                                  self.board, pawn_promoted=pawn_promotion))
            if row == start_row and self.board[row + 2 * move_amount][column] == '--':
                moves.append(Move((row, column), (row + 2 * move_amount, column), self.board))

        if column - 1 >= 0:
            if not piece_pinned or pin_dir == (move_amount, -1):
                if self.board[row + move_amount][column - 1][0] == opponent:
                    if row + move_amount == back_row:
                        pawn_promotion = True
                    moves.append(Move((row, column), (row + move_amount, column - 1),
                                      self.board, pawn_promoted=pawn_promotion))
                if (row + move_amount, column - 1) == self.possible_enpassant:
                        moves.append(Move((row, column), (row + move_amount, column - 1),
                                      self.board, enpassant_possible=True))

        if column + 1 <= 7:  # Ensure within board bounds
            if not piece_pinned or pin_dir == (move_amount, 1):
                if self.board[row + move_amount][column + 1][0] == opponent:
                    if row + move_amount == back_row:
                        pawn_promotion = True
                    moves.append(Move((row, column), (row + move_amount, column + 1),
                                      self.board, pawn_promoted=pawn_promotion))
                if (row + move_amount, column + 1) == self.possible_enpassant:
                    moves.append(Move((row, column), (row + move_amount, column + 1),
                                      self.board, enpassant_possible=True))

    def get_rook_moves(self, row, column, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][column][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        opponent = 'b' if self.whiteToMove else 'w'
        pre_compute = ((-1, 0), (0, -1), (0, 1), (1, 0))
        for compute in pre_compute:
            for i in range(1, 8):
                r = row + compute[0] * i
                c = column + compute[1] * i
                if 0 <= r < 8 and 0 <= c < 8:
                    if not piece_pinned or pin_direction == compute or \
                        pin_direction == (-compute[0], -compute[1]):
                        end_piece = self.board[r][c]
                        if end_piece[0] == '-':
                            moves.append(Move((row, column), (r, c), self.board))
                        elif end_piece[0] == opponent:
                            moves.append(Move((row, column), (r, c), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_bishop_moves(self, row, column, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][column][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        opponent = 'b' if self.whiteToMove else 'w'
        pre_compute = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for compute in pre_compute:
            for i in range(1, 8):
                r = row + compute[0] * i
                c = column + compute[1] * i
                if 0 <= r < 8 and 0 <= c < 8:
                    if not piece_pinned or pin_direction == compute or \
                            pin_direction == (-compute[0], -compute[1]):
                        end_piece = self.board[r][c]
                        if end_piece[0] == '-':
                            moves.append(Move((row, column), (r, c), self.board))
                        elif end_piece[0] == opponent:
                            moves.append(Move((row, column), (r, c), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_knight_moves(self, row, column, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        turn = 'w' if self.whiteToMove else 'b'   
        pre_compute = ((-2, -1), (-1, -2), (-1, 2), (2, -1), (1, -2), (-2, 1), (1, 2), (2, 1))
        for pre in pre_compute:
            new_row = row + pre[0]
            new_col = column + pre[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
              if self.board[new_row][new_col][0] != turn:
                  if not piece_pinned:
                      moves.append(Move((row, column), (new_row, new_col), self.board))

    def get_queen_moves(self, row, column, moves):
        self.get_bishop_moves(row, column, moves)
        self.get_rook_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):

        opponent = 'b' if self.whiteToMove else 'w'
        turn = 'w' if self.whiteToMove else 'b'
        pre_compute = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for pre in pre_compute:
            new_row = row + pre[0]
            new_col = column + pre[1]
            #print(new_row, new_col)
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col][0] != turn:
                    if turn == 'w':
                        self.white_king_loc = (new_row, new_col)
                    else:
                        self.black_king_loc = (new_row, new_col)
                    pins, check, is_in_check = self.check_for_pins_and_checks()
                    if not is_in_check:
                        moves.append(Move((row, column), (new_row, new_col), self.board))
                    if turn == 'w':
                        self.white_king_loc = (row, column)
                    else:
                        self.black_king_loc = (row, column)
        self.get_castle_moves(row, column, moves, turn)
    '''
    Generate all valid castle 
    '''
    def get_castle_moves(self, r, c, moves, turn):
        _, _, is_in_check = self.check_for_pins_and_checks()
        if is_in_check:
            return
        if (self.whiteToMove and self.white_castle_king_side) or (not self.whiteToMove and self.black_castle_king_side):
            self.get_king_side_castle_moves (r, c, moves, turn)
        if (self.whiteToMove and self.white_castle_queen_side) or (not  self.whiteToMove and self.black_castle_queen_side):
            self.get_queen_side_castle_moves(r, c, moves, turn)

    """
    Get castle move on king side
    """
    def get_king_side_castle_moves(self, r, c, moves, turn):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            king_row = self.white_king_loc[0] if self.whiteToMove else self.black_king_loc[0]
            king_col = self.white_king_loc[1] if self.whiteToMove else self.black_king_loc[1]
            if self.whiteToMove:
                self.white_king_loc = (r, c + 1)
            else:
                self.black_king_loc = (r, c + 1)
            _, _, check_at_one = self.check_for_pins_and_checks()
            if self.whiteToMove:
                self.white_king_loc = (r, c + 2)
            else:
                self.black_king_loc = (r, c + 2)
            _, _, check_at_two = self.check_for_pins_and_checks()
            if self.whiteToMove:
                self.white_king_loc = (king_row, king_col)
            else:
                self.black_king_loc = (king_row, king_col)



    """
    Get castle move on king side
    """
    def get_queen_side_castle_moves(self, r, c, moves, turn):
        if self.board[r][c + 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            pass

class Move:
    ranks_to_rows = {str(rank + 1): (8 - rank - 1) for rank in range(8)}
    rows_to_rank = {value: key for key, value in ranks_to_rows.items()}
    files_to_columns = {file : iter for iter, file in enumerate("abcdefgh") }
    columns_to_files = {value: key for key, value in files_to_columns.items()}
    # print(ranks_to_rows, rows_to_rank, columns_to_files, files_to_columns, sep = "\n")

    def __init__ (self, square_start, square_end, board, enpassant_possible = False, pawn_promoted = False, castle = False):
        self.start_row = square_start[0]
        self.start_col = square_start[1]
        self.end_row = square_end[0]
        self.end_col = square_end[1]
        self.piece_move = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.pawn_promoted = pawn_promoted
        self.enpassant_move = enpassant_possible
        if self.enpassant_move:
            self.piece_captured = 'wp' if self.piece_move == 'bp' else 'bp'
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        self.castle = castle
    """
    Override the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        #you can add to make it real chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.rows_to_rank[row]

class CastleRights:

    def __init__(self, white_king, black_king, white_queen, black_queen):
        self.wks = white_king
        self.bks = black_king
        self.wqs = white_queen
        self.bqs = black_queen