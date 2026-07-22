import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


class Character:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name

class User(Character):
    def __init__(self, symbol, name="Player"):
        super().__init__(symbol, name)

    def play(self, game, mouse_pos):
            return game.insert_move(mouse_pos, self.symbol)
            
class Robot(Character):
    def __init__(self, strategy, symbol, name="Robot"):
        super().__init__(symbol, name)
        self.strategy = strategy

    def robot_move(self, board):
        return self.strategy.choose_move(board)
        
    def play(self, game, mouse_pos=None):
        return game.insert_move(self.robot_move(game.board), self.symbol)

