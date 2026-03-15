game_board_9 = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]
game_board_25 = [
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "]
]
game_board_49 = [
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "]
]

BOARDS = {3 : game_board_9, 5 : game_board_25, 7 : game_board_49}

class Game:
    def __init__(self, size=3):
        self.board = BOARDS[size]
        self.sqr_wt = size

    def insert_move(self, position, player_symbol):
        if position < 0 or position > (self.sqr_wt * self.sqr_wt): return False
        
        row_index = position // self.sqr_wt
        column_index = position % self.sqr_wt
        
        if not self.board[row_index][column_index] == " ": return False

        self.board[row_index][column_index] = player_symbol
        
        return True
    
    def check_for_win(self):
        # Checks for win in each row.
        for row in self.board:
            symbol = row[0]
            common_row = len(set(row))
            if not " " in row and common_row <= 1:
                return True, symbol
        
        # Checks for win in each column.
        for i in range(self.sqr_wt):
            column = [row[i] for row in self.board]
            common_column = len(set(column))
            if not " " in column and common_column <= 1:
                return True, column[0]

        # Checks for win in diagnal from top-left to bottom-right
        top_left_diagnal = []
        for i in range(self.sqr_wt):
           top_left_diagnal.append(self.board[i][i])
        
        common_left_diagnal = len(set(top_left_diagnal))
        if not " " in top_left_diagnal and common_left_diagnal <= 1:
                return True, top_left_diagnal[0]

        # Checks for win in diagnal from top-right to bottom-left
        top_right_diagnal = []
        for i in range(self.sqr_wt):
            top_right_diagnal.append(self.board[(self.sqr_wt-1) - i][i])
        print(top_right_diagnal)
        common_right_diagnal = len(set(top_right_diagnal))
        if not " " in top_right_diagnal and common_right_diagnal <= 1:
                return True, top_right_diagnal[0]


        return False, None
    
    def is_tie(self):
        for row in self.board:
            if " " in row:
                return True
        return False