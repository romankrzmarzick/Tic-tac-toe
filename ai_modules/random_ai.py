import random
from itertools import product
from constants import GAME_BOARD_SIZE

class RandomAi:
    def choose_move(self, board):
        n = GAME_BOARD_SIZE
        available_spaces = [(row, col) for row, col in product(range(n), repeat=2) if board[row][col] is None]
        return random.choice(available_spaces)