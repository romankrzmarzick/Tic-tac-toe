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
        


    def is_move_in_range(self, position):
        return position < 0 or position > 8
        

    def insert_move(self, position, player_symbol):
        if position < 0 or position > 8: return False
        
        row_index = position // 3
        row = position % 3 
        
        if not self.board[row_index][row] == " ": return False
        self.board[row_index][row] = player_symbol
        
        return True