import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pygame
from constants import WINDOW_SIZE
from scripts.state_pattern import Menu

class Tictactoe:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TicTacToe")
        self.screen = pygame.display.set_mode([WINDOW_SIZE] * 2)
        self.clock = pygame.time.Clock()
        self.current_state = Menu(self.screen)
    def run(self):
        while True:
            self.current_state.handle_input()
            next_state = self.current_state.update()
            self.current_state.render()
            if next_state is not None:
                self.current_state = next_state
          
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    Tictactoe().run()

