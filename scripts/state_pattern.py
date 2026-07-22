import os
import sys
from itertools import cycle

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pygame

from scripts.game import Game
from scripts.character import User
from scripts.character import Robot
from scripts.renderer import RenderPlay, RenderReplay, RenderMenu
from ai_modules.random_ai import RandomAi
from ai_modules.smart_ai import SmartAI
from ai_modules.minimax_ai import MinimaxAI
from constants import (
    WINDOW_SIZE,
    GAME_BOARD_SIZE,
    SYMBOL_O,
    SYMBOL_X,
    EASY,
    MEDIUM,
    HARD,
)


def make_strategy(difficulty, player_symbol, robot_symbol):
    """Return the AI strategy that matches the chosen difficulty."""
    if difficulty == EASY:
        return RandomAi()
    if difficulty == HARD:
        return MinimaxAI(player_symbol, robot_symbol)
    return SmartAI(player_symbol, robot_symbol)  # MEDIUM (default)


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
        self.render_menu = RenderMenu(screen)

    def render(self):
        self.render_menu.render(pygame.mouse.get_pos())

    def update(self):
        if self.mouse_pos is not None:
            for level, rect in self.render_menu.buttons.items():
                if rect.collidepoint(self.mouse_pos):
                    return Play(self.screen, level)
        return None


class Play(State):
    def __init__(self, screen, difficulty=MEDIUM):
        super().__init__(screen)
        self.difficulty = difficulty
        self.game_over = False
        self.game = Game()
        self.player = User(SYMBOL_X)
        strategy = make_strategy(difficulty, self.player.symbol, SYMBOL_O)
        self.robot = Robot(strategy, SYMBOL_O)
        self.render_play = RenderPlay(screen)
        self.popup_delay = 1000
        self.player_turn = True
        self.end_time = 0
        self.strike_index = None
        self.winning_symbol = None
        self.move_delay = 450
        self.last_move = 0
        self.players = cycle([self.player, self.robot])
        self.current_player = next(self.players)

    def render(self):
        self.render_play.clear_screen()
        self.render_play.draw_board()

        # Highlight the empty cell under the cursor on the player's turn.
        if not self.game_over and self.current_player is self.player:
            row, col = self.index_mouse_pos(pygame.mouse.get_pos())
            if 0 <= row < GAME_BOARD_SIZE and 0 <= col < GAME_BOARD_SIZE \
                    and self.game.board[row][col] is None:
                self.render_play.draw_hover((row, col))

        self.render_play.draw_symbols(self.game.board)

        if self.game_over:
            status_text = "Game over"
        elif self.current_player is self.robot:
            status_text = "Robot is thinking..."
        else:
            status_text = "Your turn (%s)" % self.difficulty

        self.render_play.draw_status(status_text)

        if self.winning_symbol is not None:
            self.render_play.draw_strike(self.strike_index, self.winning_symbol)

    def update(self):
        if not self.game_over:
            moved = False
            now = pygame.time.get_ticks()
            if now - self.last_move >= self.move_delay:

                if self.current_player is self.player and self.mouse_pos is not None:
                    index = self.index_mouse_pos(self.mouse_pos)
                    moved = self.current_player.play(self.game, index)

                elif self.current_player is self.robot:
                    moved = self.current_player.play(self.game, None)

                if moved:
                    self.current_player = next(self.players)
                    self.last_move = now

        is_win, winning_symbol, strike_index = self.game.check_for_win()

        if is_win:
            self.game_over = True
            self.strike_index = strike_index
            self.winning_symbol = winning_symbol

            # Creates a delay between strike and replay screen.
            if self.end_time == 0:
                self.end_time = pygame.time.get_ticks()

        if not is_win and self.game.has_empty_space() is False:
            self.game_over = True
            if self.end_time == 0:
                self.end_time = pygame.time.get_ticks()

        if self.game_over and self.end_time > 0:
            current_time = pygame.time.get_ticks()

            if current_time - self.end_time >= self.popup_delay:
                # A win only counts for the human player.
                player_won = is_win and winning_symbol == self.player.symbol
                return End(self.screen, player_won, winning_symbol, self.difficulty)
        return None


class End(State):
    def __init__(self, screen, is_win, winning_symbol, difficulty=MEDIUM):
        super().__init__(screen)
        self.is_win = is_win
        self.winning_symbol = winning_symbol
        self.difficulty = difficulty
        self.render_replay = RenderReplay(screen)

    def render(self):
        self.render_replay.render(self.is_win, self.winning_symbol, pygame.mouse.get_pos())

    def update(self):
        if self.mouse_pos is not None:
            if self.render_replay.again_rect.collidepoint(self.mouse_pos):
                return Play(self.screen, self.difficulty)
            if self.render_replay.menu_rect.collidepoint(self.mouse_pos):
                return Menu(self.screen)
        return None
