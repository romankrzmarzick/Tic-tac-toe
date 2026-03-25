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
pygame.init()

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game()

    def intial(self):
        pygame.display.set_caption('TicTacToe')
        self.clock.tick(60)

    def run(self):
        self.intial()
        running = True
        x_load = pygame.image.load('images/x.png')
        o_load = pygame.image.load('images/o.png')
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mysX, mysY) = (event.pos[0], event.pos[1])
                    





            self.screen.fill(BG_COLOR)
            self.draw_lines()
            
            self.screen.blit(x_load, (300, 300))
            self.screen.blit(o_load, (150, 150))

            pygame.display.update()





    def draw_lines(self):
        for i in range (1, BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, ((WIDTH / BOARD_COLS) * i , 0), ((WIDTH / BOARD_COLS) * i, HEIGHT), LINE_WIDTH)
            pygame.draw.line(self.screen, LINE_COLOR, (0, (HEIGHT / BOARD_ROWS) * i), (WIDTH, (HEIGHT / BOARD_ROWS) * i), LINE_WIDTH)

    def create_rects(self):
        


def rud():
    ui = Interface()
    player_name = ui.choose_name()
    player_symbol, robot_symbol = ui.symbol_nomination()
    random_ai = RandomAi()


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
    
Main().run()
