
class Game:
    def __init__(self, size):
        self.board = [[" " for _ in range(size)] for _ in range(size)]
        self.sqr_wt = size
    
  
    def insert_move(self, mouse_pos_index, curr_player_num):
        # Add move to board, changing the game state. 
        if not self.board[mouse_pos_index[0]][mouse_pos_index[1]] == " ": return False
        self.board[mouse_pos_index[0]][mouse_pos_index[1]] = curr_player_num
        return True
    
    def check_for_win(self):
        # Checks for win by searching each row.
        for row in self.board:
            symbol = row[0]
            common_row = len(set(row))
            if not " " in row and common_row <= 1:
                return True, symbol
        
        # Checks for win by searching each column.
        for i in range(self.sqr_wt):
            column = [row[i] for row in self.board]
            common_column = len(set(column))
            if not " " in column and common_column <= 1:
                return True, column[0]

        # Checks for win in diagnal from top-left to bottom-right.
        top_left_diagonal = []
        for i in range(self.sqr_wt):
           top_left_diagonal.append(self.board[i][i])
        
        common_left_diagonal = len(set(top_left_diagonal))
        if not " " in top_left_diagonal and common_left_diagonal <= 1:
                return True, top_left_diagonal[0]

        # Checks for win in diagnal from top-right to bottom-left.
        top_right_diagonal = []
        for i in range(self.sqr_wt):
            top_right_diagonal.append(self.board[(self.sqr_wt - 1) - i][i])
        common_right_diagonal = len(set(top_right_diagonal))
        if not " " in top_right_diagonal and common_right_diagonal <= 1:
                return True, top_right_diagonal[0]

        return False, None
    
    def empty_space(self):
        return any(" " in i for i in self.board)
