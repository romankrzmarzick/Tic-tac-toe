import random

class RandomAi:
    def choose_move(self, board, size):
        available_spaces = []
        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if board[row_index][col_index] == " ":
                    available_spaces.append(row_index * size + col_index) 
        return random.choice(available_spaces)

