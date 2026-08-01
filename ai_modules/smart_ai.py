import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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
        for row_index, row in enumerate(board):
            if row.count(player_move) == (n - 1) and None in row:
                return True, (row_index, row.index(None))

        columns = list(zip(*board))
        for cell_index, cell in enumerate(columns):
            if cell.count(player_move) == (n - 1) and None in cell:
                return True, (cell.index(None), cell_index)

        topl_diag = [(board[i][i]) for i in range(n)]
        if topl_diag.count(player_move) == (n - 1) and None in topl_diag:
            return True, (topl_diag.index(None), topl_diag.index(None))

        top_r_diag = [board[(n - 1) - i][i] for i in range(n)]
        space_index = next(((n - 1 - i, i) for i in range(n) if board[(n - 1) - i][i] is None), None)
        if top_r_diag.count(player_move) == (n - 1) and space_index is not None:
            return True, space_index
        
        return False, None

    def choose_move(self, board):
        n = self.game_size
        available_spaces = [(row, col) for row, col in product(range(n), repeat=2) if board[row][col] is None]

        # win if possible
        value, index = self.best_move(board, self.r_symbol)
        if value:
            return index

        # otherwise block the player's win
        value, index = self.best_move(board, self.p_symbol)
        if value:
            return index

        center_piece = (n // 2, n // 2)
        if center_piece in available_spaces:
            return center_piece

        available_corners = [(0, 0), (n - 1, n - 1), (0, n - 1), (n - 1, 0)]
        corner_spaces = [c for c in available_corners if c in available_spaces]
        if corner_spaces:
            return random.choice(corner_spaces)

        return random.choice(available_spaces)

