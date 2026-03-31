class Character:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class User(Character):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)

    def play(self, game, mouse_pos):
            game.insert_move(mouse_pos, self.symbol)
            
    
class Robot(Character):
    def __init__(self, name, symbol, strategy):
        super().__init__(name, symbol)
        self.strategy = strategy

    def robot_move(self, board, size):
        return self.strategy.choose_move(board, size)
        
    def play(self, game, mouse_pos=None):
        game.insert_move(self.robot_move(game.board, game.sqr_wt), self.symbol)

