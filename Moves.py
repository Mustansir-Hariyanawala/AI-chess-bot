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
