import pygame
from constants import WINDOW_SIZE
from scripts.state_pattern import Play

class Tictactoe:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TicTacToe")
        self.screen = pygame.display.set_mode([WINDOW_SIZE] * 2)
        self.clock = pygame.time.Clock()
        self.current_state = Play(self.screen)
    def run(self):
        while True:
            self.current_state.handle_input()
            next_state = self.current_state.update()
            self.current_state.render()
            if next_state is not None:
                self.current_state = next_state
          
            pygame.display.flip()
            self.clock.tick(60)



Tictactoe().run()