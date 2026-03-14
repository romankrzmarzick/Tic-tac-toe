from scripts.character import Character
from scripts.game import Game
from scripts.interface import Interface



def play_turn(ui, game, player_symbol, name):
    while True:
        position = ui.choose_position(game.sqr_wt, name )
        if game.insert_move(position, player_symbol):
            break
        ui.invalid_move_message()

def run():
    ui = Interface()
    player_name = ui.choose_name()
    player_symbol, robot_symbol = ui.symbol_nomination()
    game = Game(ui.choose_square_size())
    
    p1 = Character(player_name, player_symbol)
    r1 = Character("robot", robot_symbol)

    while True:

        play_turn(ui, game, p1.symbol, p1.name)
        ui.display_board(game.board)
        if game.check_for_win:
            print("You won")
run()