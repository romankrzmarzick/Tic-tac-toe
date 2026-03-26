class Character:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class User(Character):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)

    def play(self, game, ui):
        while True:
            position = ui.choose_position(game.sqr_wt, self.name )
            if game.insert_move(position, self.symbol):
                break
            ui.invalid_move_message()

class Robot(Character):
    def __init__(self, name, symbol, strategy):
        super().__init__(name, symbol)
        self.strategy = strategy

    def robot_move(self, board, size):
        return self.strategy.choose_move(board, size)
        
    def play(self, game, ui=None):
        game.insert_move(self.robot_move(game.board, game.sqr_wt), self.symbol)

