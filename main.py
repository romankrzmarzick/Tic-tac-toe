from scripts.character import User
from scripts.character import Robot
from scripts.game import Game
from scripts.interface import Interface
from ai_modules.random_ai import RandomAi
import sys


def run():
    ui = Interface()
    player_name = ui.choose_name()
    player_symbol, robot_symbol = ui.symbol_nomination()
    random_ai = RandomAi()


    while True:
        game = Game()
        player = User(player_name, player_symbol)
        robot = Robot("Robot", robot_symbol, random_ai)
        ui.num_rule_board(game)
        win_symbol = None
       
        i = 0
        while game.empty_space():
            # Uses modulus to switch turns using even and odd numbers.
            turn_number = i % 2
            current_player = player if turn_number == 0 else robot
            current_player.play(game, ui)
        
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


if __name__ == "__main__":
    run()
