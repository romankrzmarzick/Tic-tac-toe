from scripts.character import User
from scripts.character import Robot
from scripts.game import Game
from scripts.interface import Interface
from scripts.random_ai import RandomAI
from scripts.minimax_ai import MinimaxAI

import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def turn(ui, game, player):
    while True:
        position = ui.choose_position(game.sqr_wt, player.name )
        if game.insert_move(position, player.symbol):
            break
        ui.invalid_move_message()

def run():
    ui = Interface()
    player_name = ui.choose_name()
    player_symbol, robot_symbol = ui.symbol_nomination()
    random_ai = RandomAI()
    minimax_ai = MinimaxAI()

    while True:
        game = Game()
        player = User(player_name, player_symbol)
        robot = Robot("Robot", robot_symbol, rand)
        ui.num_rule_board(game)
       
        i = 0
        while not game.tie():
            # Uses modulus to switch turns using even and odd numbers.
            turn_number = i % 2
            turn(ui, game, player) if turn_number == 0 else 
            clear_screen()
            ui.display_board(game.board)
            value, win_symbol = game.check_for_win()
            
            if value: break
            i += 1

        # Displays the Result of the match.
        if win_symbol == player.symbol:
            ui.is_victory()
        elif win_symbol == robot.symbol:
            ui.is_defeat()
        else:
            ui.is_draw()
        
        # Asks the user if he wants to play another match.
        if not ui.replay():
            sys.exit()
    

run()