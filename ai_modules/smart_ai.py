import random
from constants import GAME_BOARD_SIZE
from itertools import product


class SmartAI:
    def __init__(self, player_symbol, robot_symbol):
        self.p_symbol = player_symbol
        self.r_symbol = robot_symbol
        self.game_size = GAME_BOARD_SIZE

    def best_move(self, board, player_move):
        n = self.game_size
        # Searches through every row of the board
        for row_index, row in enumerate(board):
            if row.count(player_move) == (n - 1) and None in row:
                return True, (row_index, row.index(None))

        # Searches through every column of the board
        columns = list(zip(*board))
        for cell_index, cell in enumerate(columns):
            if cell.count(player_move) == (n - 1) and None in cell:
                return True, (cell.index(None), cell_index)

        # Looks at the diagonal that goes from the top-left to the bottom-right. 
        topl_diag = [(board[i][i]) for i in range(n)]
        if topl_diag.count(player_move) == (n - 1) and None in topl_diag:
            return True, (topl_diag.index(None), topl_diag.index(None))
            
        # Looks at the diagonal that starts at the bottom-left of the board and finishes at the top-right.
        top_r_diag = [board[(n - 1) - i][i] for i in range(n)]
        space_index = next(((n - 1 - i, i) for i in range(n) if board[(n - 1) - i][i] is None), None)
        if top_r_diag.count(player_move) == (n - 1) and space_index is not None:
            return True, space_index
        
        return False, None

    def choose_move(self, board):
        n = self.game_size 
        # Loops through the board to identify availability in the current state for corners and the center piece.
        available_spaces = [(row, col) for row, col in product(range(n), repeat=2) if board[row][col] is None]      

        # Win if possible.
        value, index = self.best_move(board, self.r_symbol)
        if value:
            return index

        # Block player win if possible.
        value, index = self.best_move(board, self.p_symbol)
        if value:
            return index

        # Grab center piece if available.
        center_piece = (n // 2, n // 2) 
        if center_piece in available_spaces:
            return center_piece
        
        # Grab random corner piece if available.
        available_corners = [(0, 0), (n - 1, n - 1), (0, n - 1), (n - 1, 0)]
        corner_spaces = [c for c in available_corners if c in available_spaces]
        if corner_spaces:
            return random.choice(corner_spaces)

        # Random choice
        return random.choice(available_spaces)

