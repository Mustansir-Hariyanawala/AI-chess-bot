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
            ['--', '--', '--', '--', 'bQ', '--', '--', '--'],
            ['--', '--', '--', 'wQ', '--', '--', '--', '--'],
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

    #takes moves as parameter and executes it (this will not work for castling, pawn promotion and en passant
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_move
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap player's turn

    def undo_move(self):
        if len(self.moveLog) == 0:
            return
        move = self.moveLog.pop() #retrieving recent move
        self.board[move.start_row][move.start_col] = move.piece_move #place to be undoed
        self.board[move.end_row][move.end_col] = move.piece_captured #place captured pawn again
        self.whiteToMove = not self.whiteToMove #reswap player's turn

    '''
    All moves considering checks
    '''
    def get_valid_moves(self):
        return self.get_all_possible_move()
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
        # let's add promotion later

    def get_rook_moves (self, row, column, moves):
        flag = True
        opponent = 'b' if self.whiteToMove else 'w'
        turn = 'w' if self.whiteToMove else 'b'
        for r in range(1, row + 1):
            if self.board[row - r][column][0] != turn and flag:
                moves.append(Move((row, column), (row - r, column), self.board))
                if self.board[row - r][column][0] == opponent:
                    flag = False
            else:
                break
        flag = True
        for r in range(1, 8 - row):
            if self.board[row + r][column][0] != turn and flag:
                moves.append(Move((row, column), (row + r, column), self.board))
                if self.board[row + r][column][0] == opponent:
                    flag = False
            else:
                break
        flag = True
        for c in range(1, column + 1):
            if self.board[row][column - c][0] != turn and flag:
                moves.append(Move((row, column), (row, column - c), self.board))
                if self.board[row][column - c][0] == opponent:
                    flag = False
            else:
                break
        flag = True
        for c in range(1, 8 - column):
            if self.board[row][column + c][0] != turn and flag:
                moves.append(Move((row, column), (row, column + c), self.board))
                if self.board[row][column + c][0] == opponent:
                    flag = False
            else:
                break

    def get_bishop_moves(self, row, column, moves):
        turn = 'w' if self.whiteToMove else 'b'
        opponent = 'b' if self.whiteToMove else 'w'
        flag = True
        for r in range(1, min(row + 1, column + 1)):
            if flag and self.board[row - r][column - r][0] != turn:
                moves.append(Move((row, column), (row - r, column - r), self.board))
                if self.board[row - r][column][0] == opponent:
                    flag = False
            else:
                break
        flag = True
        for r in range(1, min(8 - row, column + 1)):
            if flag and self.board[row + r][column - r][0] != turn:
                moves.append(Move((row, column), (row + r, column - r), self.board))
                if self.board[row + r][column - r][0] == opponent:
                    flag = False

            else:
                break
        flag = True
        for c in range(1, min(8 - column, row + 1)):
            if flag and self.board[row - c][column + c][0] != turn:
                moves.append(Move((row, column), (row - c, column + c), self.board))
                if self.board[row - c][column + c][0] == opponent:
                    flag = False
            else:
                break
        flag = True
        for c in range(1, min(8 - column, 8 - row)):
            if flag and self.board[row + c][column + c][0] != turn:
                moves.append(Move((row, column), (row + c, column + c), self.board))
                if self.board[row + c][column + c][0] == opponent:
                    flag = False
            else:
                break

    def get_knight_moves(self, row, column, moves):
        pass

    def get_queen_moves(self, row, column, moves):
        self.get_bishop_moves(row, column, moves)
        self.get_rook_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):
        pass




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