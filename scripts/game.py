from constants import GAME_BOARD_SIZE
from itertools import chain

class Game:
    def __init__(self):
        self.game_size = GAME_BOARD_SIZE
        self.board = [[None for _ in range(GAME_BOARD_SIZE)] for _ in range(GAME_BOARD_SIZE)]
  
    def insert_move(self, mouse_pos_index: tuple, curr_player_num):
        # Add move to board, changing the game state. 
        if not self.board[mouse_pos_index[0]][mouse_pos_index[1]] is None: 
            return False
        self.board[mouse_pos_index[0]][mouse_pos_index[1]] = curr_player_num
        return True
     
    
    def check_for_win(self):
        n = self.game_size

        def sum_all(line):
            return True if len(set(line)) == 1 and None not in line else False
        
        # Add rows and their index as well for strike index draw.
        rows = ([(row, ((r_i, 0), (r_i, n - 1))) for r_i, row in enumerate(self.board)])

        # Add columns and their index to lines
        cols = []
        for c in range(n):
            col = [self.board[r][c] for r in range(n)]
            cols.append((col, ((0, c,), (n - 1, c))))

        # Add diags to lines for chain check in board.
        diags = [
            ([self.board[i][i] for i in range(n)], ((0, 0), (n - 1, n - 1))),
            ([self.board[(n - 1) - i][i] for i in range(n)], ((0, n - 1), (n - 1, 0)))
            ] 

        # create list and add helper and another var in chain
        for line, index in chain(rows, cols, diags):
            if sum_all(line):
                return True, line[0], index  
        
        return False, None, None

            
    def empty_space(self):
        return any(None in row for row in self.board)
