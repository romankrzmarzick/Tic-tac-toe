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
            if not " " in row and len(set(row)) <= 1:
                return True
        
        # Checks for win in each column.
        for i in range(self.sqr_wt):
            column = [row[i] for row in self.board]
            if not " " in column and len(set(column)) <= 1:
                return True

        return False
        