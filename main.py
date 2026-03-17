from scripts.character import Character
from scripts.game import Game
from scripts.interface import Interface
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_turn(ui, game, current_player):
    while True:
        position = ui.choose_position(game.sqr_wt, current_player.name )
        if game.insert_move(position, current_player.symbol):
            break
        ui.invalid_move_message()

def run():
    ui = Interface()
    player_name = ui.choose_name()
    player_symbol, robot_symbol = ui.symbol_nomination()
    game = Game(ui.choose_square_size())

    player = Character(player_name, player_symbol)
    robot = Character("Robot", robot_symbol)

    i = 0
    while not game.tie():
        turn_number = i % 2
        current_player = player if turn_number == 0 else robot

        play_turn(ui, game, current_player)
        clear_screen()
        ui.display_board(game.board)
        value, win_symbol = game.check_for_win()
        
        if value: break
        i += 1
        
        
    if win_symbol == player.symbol:
        print(f"{player.name} Won!")
    elif win_symbol == robot.symbol:
        print(f"{robot.name} Won!")
    else:
        print("Tie!")
    
    

run()