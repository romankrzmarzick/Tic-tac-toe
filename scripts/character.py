class Character:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class User(Character):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)

class Robot(Character):
    def __init__(self, strategy, name="Robot"):
        super().__init__(name)
        self.strategy = strategy

    def robot_move(self, board):
        return self.strategy.choose_move(board)
        
