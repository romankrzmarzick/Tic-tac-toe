from constants import GAME_BOARD_SIZE

class Game:
    def __init__(self):
        self.sqr_wt = GAME_BOARD_SIZE
        self.board = [[None for _ in range(GAME_BOARD_SIZE)] for _ in range(GAME_BOARD_SIZE)]
  
    def insert_move(self, mouse_pos_index, curr_player_num):
        # Add move to board, changing the game state. 
        if not self.board[mouse_pos_index[0]][mouse_pos_index[1]] == None: return False
        self.board[mouse_pos_index[0]][mouse_pos_index[1]] = curr_player_num
        return True
    
    def check_for_win(self):
        # Checks for win by searching each row.
        for row_index, row in enumerate(self.board):
            symbol = row[0]
            common_row = len(set(row))
            if not None in row and common_row <= 1:
                strike_index_row = ((row_index, 0), (row_index, 2))
                return True, symbol, strike_index_row
        
        # Checks for win by searching each column.
        for i in range(self.sqr_wt):
            column = [row[i] for row in self.board]
            common_column = len(set(column))
            if not None in column and common_column <= 1:
                strike_index_col = ((0, i,), (2, i))
                return True, column[0], strike_index_col

        # Checks for win in diagnal from top-left to bottom-right.
        top_left_diagonal = []
        for i in range(self.sqr_wt):
           top_left_diagonal.append(self.board[i][i])
        common_left_diagonal = len(set(top_left_diagonal))
        if not None in top_left_diagonal and common_left_diagonal <= 1:
                strike_index_ldiag = ((0, 0), (2, 2))
                return True, top_left_diagonal[0], strike_index_ldiag

        # Checks for win in diagnal from top-right to bottom-left.
        top_right_diagonal = []
        for i in range(self.sqr_wt):
            top_right_diagonal.append(self.board[(self.sqr_wt - 1) - i][i])
        common_right_diagonal = len(set(top_right_diagonal))
        if not None in top_right_diagonal and common_right_diagonal <= 1:
                strike_index_rdiag = (((0, 2), (2, 0)))
                return True, top_right_diagonal[0], strike_index_rdiag
        
        return False, None, None
    
    def empty_space(self):
        return any(None in i for i in self.board)
