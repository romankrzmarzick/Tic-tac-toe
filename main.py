from enum import Enum, auto
import pygame
import sys
from scripts.game import Game
from scripts.character import User
from scripts.character import Robot
from scripts.renderer import RenderMenu, RenderPlay, RenderReplay
from ai_modules.random_ai import RandomAi
from constants import WINDOW_SIZE, GAME_BOARD_SIZE

      
class Tictactoe:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TicTacToe")
        self.screen = pygame.display.set_mode([WINDOW_SIZE] * 2)
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.player = User(1)
        self.robot = Robot(RandomAi(), 2)
        self.render_menu = RenderMenu(self.screen)
        self.render_play = RenderPlay(self.screen)
        self.render_replay = RenderReplay(self.screen)

    def run(self):
        self.num_state = 0
        self.end_time = 0
        self.show_popup = False
        self.game_over = False
        self.player_turn = True
        pop_up_delay = 1000

        while True:
            # --- Input ---
            mouse_position = self.input_events()  
            
            # --- Update --- 
            if not self.game_over:    
                current_player = self.player if self.player_turn else self.robot
                
                # Player's turn to go and place their move. 
                if current_player == self.player and mouse_position is not None:
                    index = self.index_mouse_pos(mouse_position)
                    pygame.time.wait(500)
                    if current_player.play(self.game, index):
                        self.player_turn = not self.player_turn

                # Robot's turn to use its ai to choose a move
                if current_player == self.robot:
                    pygame.time.wait(500)
                    if current_player.play(self.game, None):
                        self.player_turn = not self.player_turn
                        
            is_win, winning_symbol, strike_index,  = self.game.check_for_win()
            

            # --- Render ---

            self.render_play.clear_screen()
            self.render_play.draw_board()
            self.render_play.draw_symbols(self.game.board)

            if is_win:
                self.game_over = True
                self.render_play.draw_strike(strike_index, winning_symbol)
                # Creates a delay between strike and replay screen. 
                if self.end_time == 0:
                    self.end_time = pygame.time.get_ticks()
            
            if not is_win and self.game.empty_space() == False:
                self.game_over = True
                if self.end_time == 0:
                    self.end_time = pygame.time.get_ticks()

            if self.game_over and self.end_time > 0:
                current_time = pygame.time.get_ticks()

                if current_time - self.end_time >= pop_up_delay:
                    self.render_replay.clear_screen()
                    self.render_replay.end_results(is_win, winning_symbol)
                    self.render_replay.render_button()
            
            pygame.display.flip()
            self.clock.tick(60)


    def index_mouse_pos(self, mouse_pos):
        # mouse_pos = (x, y)
        col = mouse_pos[0] // (WINDOW_SIZE // GAME_BOARD_SIZE)
        row = mouse_pos[1] // (WINDOW_SIZE // GAME_BOARD_SIZE)
        return (row, col)

    def reset_game(self):
        self.game = Game()
        self.game_over = False
        self.show_popup = False
        self.num_state = 0
        self.end_time = 0
        self.player_turn = True

    def input_events(self):
        mouse_position = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                # Resets the game and variables to start a new one if the statement = True.
                if self.render_replay.button_rect.collidepoint(mouse_position):
                    self.reset_game()
                    mouse_position = None
        return mouse_position

Tictactoe().run()