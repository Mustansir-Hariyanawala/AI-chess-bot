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
        self.check_mate = False
        self.stale_mate = False

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

    '''
    All moves considering checks
    '''
    def get_valid_moves(self):
        #1.) generate all possible moves
        moves = self.get_all_possible_move()
        #2.) for each move, make the move
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            #3.) generate all opponent's moves
            #4.) for each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.is_in_check():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undo_move()
        if len(moves) == 0:
            if self.is_in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        #5.) if they do attack your king, not a valid move
        return moves
    """
    Determine if the current player is in check
    """

    def is_in_check(self):
        if self.whiteToMove:
            return self.square_under_attack(self.white_king_loc[0], self.white_king_loc[1])
        return self.square_under_attack(self.black_king_loc[0], self.black_king_loc[1])

    """
    Determine if the enemy can attack the square row , column
    """
    def square_under_attack(self, row, column):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        opponent_move = self.get_all_possible_move()
        self.whiteToMove = not self.whiteToMove
        for move in opponent_move:
            if move.end_row == row and move.end_col == column:
                return True
        return False

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
        if self.whiteToMove: #white to move
            if self.board[row - 1][column] == '--': #1 square pawn advance
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == '--':
                    moves.append(Move((row, column), (row - 2, column), self.board))

            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row, column),(row - 1, column - 1),self.board))

            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row, column),(row - 1, column + 1),self.board))

        else:  # black to move
            if self.board[row + 1][column] == '--': #1 square pawn advance
                moves.append(Move((row, column),(row + 1, column),self.board))
                if row == 1 and self.board[row + 2][column] == '--':
                    moves.append(Move((row, column),(row + 2, column), self.board))

            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == 'w': #enemy piece to capture
                    moves.append(Move((row, column),(row + 1, column - 1), self.board))

            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0] == 'w': #enemy piece to capture
                    moves.append(Move((row, column), (row + 1, column + 1),self.board))

    def get_rook_moves(self, row, column, moves):
        opponent = 'b' if self.whiteToMove else 'w'
        turn = 'w' if self.whiteToMove else 'b'
        for r in range(1, row + 1):
            if self.board[row - r][column][0] != turn:
                moves.append(Move((row, column), (row - r, column), self.board))
                if self.board[row - r][column][0] == opponent:
                    break
            else:
                break
        for r in range(1, 8 - row):
            if self.board[row + r][column][0] != turn:
                moves.append(Move((row, column), (row + r, column), self.board))
                if self.board[row + r][column][0] == opponent:
                    break
            else:
                break
        for c in range(1, column + 1):
            if self.board[row][column - c][0] != turn :
                moves.append(Move((row, column), (row, column - c), self.board))
                if self.board[row][column - c][0] == opponent:
                    break
            else:
                break
        for c in range(1, 8 - column):
            if self.board[row][column + c][0] != turn:
                moves.append(Move((row, column), (row, column + c), self.board))
                if self.board[row][column + c][0] == opponent:
                    break
            else:
                break

    def get_bishop_moves(self, row, column, moves):
        turn = 'w' if self.whiteToMove else 'b'
        opponent = 'b' if self.whiteToMove else 'w'
        for r in range(1, min(row + 1, column + 1)):
            if self.board[row - r][column - r][0] != turn:
                moves.append(Move((row, column), (row - r, column - r), self.board))
                if self.board[row - r][column][0] == opponent:
                    break
            else:
                break
        for r in range(1, min(8 - row, column + 1)):
            if self.board[row + r][column - r][0] != turn:
                moves.append(Move((row, column), (row + r, column - r), self.board))
                if self.board[row + r][column - r][0] == opponent:
                    break
            else:
                break
        for c in range(1, min(8 - column, row + 1)):
            if self.board[row - c][column + c][0] != turn:
                moves.append(Move((row, column), (row - c, column + c), self.board))
                if self.board[row - c][column + c][0] == opponent:
                    break
            else:
                break
        for c in range(1, min(8 - column, 8 - row)):
            if self.board[row + c][column + c][0] != turn:
                moves.append(Move((row, column), (row + c, column + c), self.board))
                if self.board[row + c][column + c][0] == opponent:
                    break
            else:
                break

    def get_knight_moves(self, row, column, moves):
        opponent = 'b' if self.whiteToMove else 'w'
        turn = 'w' if self.whiteToMove else 'b'
        pre_compute = ((-2, -1), (-1, -2), (-1, 2), (2, -1), (1, -2), (-2, 1), (1, 2), (2, 1))
        for pre in pre_compute:
            new_row = row + pre[0]
            new_col = column + pre[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col][0] != turn:
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
            print(new_row, new_col)
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col][0] != turn:
                    moves.append(Move((row, column), (new_row, new_col), self.board))

class Move:
    ranks_to_rows = {str(rank + 1): (8 - rank - 1) for rank in range(8)}
    rows_to_rank = {value: key for key, value in ranks_to_rows.items()}
    files_to_columns = {file : iter for iter, file in enumerate("abcdefgh") }
    columns_to_files = {value: key for key, value in files_to_columns.items()}
    # print(ranks_to_rows, rows_to_rank, columns_to_files, files_to_columns, sep = "\n")

    def __init__ (self, square_start, square_end, board):
        self.start_row = square_start[0]
        self.start_col = square_start[1]
        self.end_row = square_end[0]
        self.end_col = square_end[1]
        self.piece_move = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # print(self.moveID)
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