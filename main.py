from scripts.character import User
from scripts.character import Robot
from scripts.game import Game
from scripts.interface import Interface
from ai_modules.minimax_ai import MinimaxAI
from ai_modules.random_ai import RandomAi
import pygame
import sys

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
<<<<<<< HEAD
=======

running = True

pygame.init()

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def intial(self):
        pygame.display.set_caption('TicTacToe')
        self.clock.tick(60)

    def run(self):
        self.intial()
        running = True
        
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            
            self.screen.fill(BG_COLOR)
            self.draw_lines()
            
            pygame.display.update()




    def draw_lines(self):
        for i in range (1, BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, ((WIDTH / BOARD_COLS) * i , 0), ((WIDTH / BOARD_COLS) * i, HEIGHT), LINE_WIDTH)
            pygame.draw.line(self.screen, LINE_COLOR, (0, (HEIGHT / BOARD_ROWS) * i), (WIDTH, (HEIGHT / BOARD_ROWS) * i), LINE_WIDTH)


>>>>>>> main

pygame.init()

<<<<<<< HEAD
class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game()
        

    def run(self):
        pygame.display.set_caption('TicTacToe')
        
        mys_pos = [0, 0]
        
        running = True
        while running:
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mys_pos = [event.pos[0], event.pos[1]]
                    


            pygame.draw.circle(self.screen, LINE_COLOR, tuple(mys_pos), 3, 5)

            # WIPE
            self.screen.fill(BG_COLOR)
            self.draw_lines()
            
            self.screen.blit(pygame.image.load('images/x.png').convert_alpha(), (300, 300))
            self.screen.blit(pygame.image.load('images/o.png').convert_alpha(), (150, 150))
            

            self.clock.tick(60)
            # RENDER GAME
            self.clock.tick(60)
            pygame.display.flip()


    def draw_lines(self):
        for i in range (1, BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, ((WIDTH / BOARD_COLS) * i , 0), ((WIDTH / BOARD_COLS) * i, HEIGHT), LINE_WIDTH)
            pygame.draw.line(self.screen, LINE_COLOR, (0, (HEIGHT / BOARD_ROWS) * i), (WIDTH, (HEIGHT / BOARD_ROWS) * i), LINE_WIDTH)



# def rud():
#     ui = Interface()
#     player_name = ui.choose_name()
#     player_symbol, robot_symbol = ui.symbol_nomination()
#     random_ai = RandomAi()


#     while True:
#         game = Game()
#         player = User(player_name, player_symbol)
#         robot = Robot("Robot", robot_symbol, random_ai)
#         ui.num_rule_board(game)
       
#         i = 0
#         while game.empty_space():
#             # Uses modulus to switch turns using even and odd numbers.
#             turn_number = i % 2
#             current_player = player if turn_number == 0 else robot
#             current_player.play(game, ui)
        
#             ui.display_board(game.board)
#             value, win_symbol = game.check_for_win()
            
#             if value: break
#             i += 1

#         # Displays the Result of the match.
#         if win_symbol == player.symbol:
#             ui.is_victory()
#         elif win_symbol == robot.symbol:
#             ui.is_defeat()
#         else:
#             ui.is_draw()
        
#         # Asks the user if he wants to play another match.
#         if not ui.replay():
#             sys.exit()
=======
    while True:
        game = Game()
        player = User(player_name, player_symbol)
        robot = Robot("Robot", robot_symbol, random_ai)
        ui.num_rule_board(game)
       
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
>>>>>>> main
    
Main().run()
