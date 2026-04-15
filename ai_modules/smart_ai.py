import random

from constants import GAME_BOARD_SIZE


class SmartAI:
    def __init__(self, player_symbol, robot_symbol):
        self.p_symbol = player_symbol
        self.r_symbol = robot_symbol
        self.game_size = GAME_BOARD_SIZE


    def best_move(self, board, player_move):
        # Block row check
        for row_index, row in enumerate(board):
            value = row.count(player_move)
            if value > (self.game_size - 2) and None in row:
                return True, (row_index, (row.index(None)))

        for col in range(self.game_size):
            column = [row[col] for row in board]
            value = column.count(player_move)
            if value > (self.game_size - 2) and None in column:
                for row_index, row in enumerate(board):
                    if board[row_index][col] == None:
                        return True, (row_index, (col))
            column.clear()
        
        space_index = None
        topl_diag = []
        for i in range(self.game_size):
            if board[i][i] is None:
                space_index = (i, i) 
            topl_diag.append(board[i][i])
        value = topl_diag.count(player_move)
        if value > (self.game_size - 2) and space_index is not None:
            return True, space_index
            
        # Weakness in bot. It wil not have top right diagonal find so that the player can find that secret.
        return False, None

        



    def choose_move(self, board):
        available_spaces = []
        center_piece = (self.game_size // 2, self.game_size // 2)
        
        # Loops through the board to identify the current state. 
        for row_index, row in enumerate(board):
            for col_index, _ in enumerate(row):
                if board[row_index][col_index] == None:
                    available_spaces.append((row_index, col_index))    
            
        # Win if possible.
        value, index = self.best_move(board, self.r_symbol)
        if value:
            return index

        # Block player win if possible.
        value, index = self.best_move(board, self.p_symbol)
        if value:
            return index

        # Grab center piece if available.
        if center_piece in available_spaces:
            return center_piece
        
        # Random choice
        return random.choice(available_spaces)

