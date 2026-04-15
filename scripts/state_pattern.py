import pygame
import sys
from scripts.game import Game
from scripts.character import User
from scripts.character import Robot
from scripts.renderer import RenderMenu, RenderPlay, RenderReplay
from ai_modules.random_ai import RandomAi
from ai_modules.smart_ai import SmartAI
from constants import WINDOW_SIZE, GAME_BOARD_SIZE



class State():
    def __init__(self, screen):
        self.screen = screen
        self.mouse_pos = None
    def handle_input(self):
        self.mouse_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
        
    def index_mouse_pos(self, mouse_pos):
        # mouse_pos = (x, y)
        col = mouse_pos[0] // (WINDOW_SIZE // GAME_BOARD_SIZE)
        row = mouse_pos[1] // (WINDOW_SIZE // GAME_BOARD_SIZE)
        return (row, col)

class Menu(State):
    def __init__(self, screen):
        super().__init__(screen)


class Play(State):
    def __init__(self, screen):
        super().__init__(screen)
        self.game_over = False
        self.game = Game()
        self.player = User(1)
        self.robot = Robot(SmartAI(self.player.symbol, 2), 2)
        self.render_play = RenderPlay(screen)
        self.popup_delay = 1000
        self.player_turn = True
        self.end_time = 0
        self.strike_index = None
        self.winning_symbol = None

    def render(self):
        self.render_play.clear_screen()
        self.render_play.draw_board()
        self.render_play.draw_symbols(self.game.board)
        
        if self.winning_symbol is not None:
            self.render_play.draw_strike(self.strike_index, self.winning_symbol)

    def update(self):
        if not self.game_over:  
            current_player = self.player if self.player_turn else self.robot
            if current_player == self.player and self.mouse_pos is not None:
                index = self.index_mouse_pos(self.mouse_pos)
                pygame.time.wait(500)
                if current_player.play(self.game, index):
                    self.player_turn = not self.player_turn
            if current_player == self.robot:
                pygame.time.wait(500)
                if current_player.play(self.game, None):
                    self.player_turn = not self.player_turn

        is_win, winning_symbol, strike_index,  = self.game.check_for_win()
        
        if is_win:
                self.game_over = True
                self.strike_index = strike_index
                self.winning_symbol = winning_symbol
            
                # Creates a delay between strike and replay screen. 
                if self.end_time == 0:
                    self.end_time = pygame.time.get_ticks()
            
        if not is_win and self.game.empty_space() == False:
                self.game_over = True
                if self.end_time == 0:
                    self.end_time = pygame.time.get_ticks()

        if self.game_over and self.end_time > 0:
            current_time = pygame.time.get_ticks()
                
            if current_time - self.end_time >= self.popup_delay:
                return End(self.screen, is_win, winning_symbol)
        return None
    

class End(State):
    def __init__(self, screen, is_win, winning_symbol):
        super().__init__(screen)
        self.is_win = is_win
        self.winning_symbol = winning_symbol
        self.render_replay = RenderReplay(screen)
    
    
    def render(self):
        self.render_replay.clear_screen()
        self.render_replay.render_button()
        self.render_replay.end_results(self.is_win, self.winning_symbol)
        self.render_replay.result_message(self.is_win)

    def update(self):
        if self.mouse_pos is not None:
            if self.render_replay.button_rect.collidepoint(self.mouse_pos):
                return Play(self.screen)
        return None

