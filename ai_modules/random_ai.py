import random

class RandomAi:
    def choose_move(self, board):
        available_spaces = []
        for row_index, row in enumerate(board):
            for col_index, _ in enumerate(row):
                if board[row_index][col_index] == " ":
                    available_spaces.append((row_index, col_index)) 
        return random.choice(available_spaces)

