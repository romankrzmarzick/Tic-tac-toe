import pygame as pg
import sys
from scripts.game import Game
from scripts.character import User
from scripts.character import Robot
from ai_modules.random_ai import RandomAi

ASSIGN_NUM = (0, 1)
WINDOW_SIZE = 600
GAME_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GAME_SIZE
BG_COLOR = (0, 200, 200)
LINE_COLOR = (0, 150, 150)
X_COLOR = (50, 50, 50)
O_COLOR = (255, 255, 255)
FIXED_SCALAR = 3.5
WIN_COLOR = (0, 255, 0)
TIE_COLOR = (0, 0, 255)
LOSE_COLOR = (255, 0, 0)

pg.init()

class TicTacToe:
    def __init__(self):
        self.screen = pg.display.set_mode([WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.game = Game(GAME_SIZE)
        self.player = User("Player", ASSIGN_NUM[0])
        self.robot = Robot("Robot", ASSIGN_NUM[1], RandomAi())

    def run(self):
        self.mouse_position = [0, 0]
        num_state = 0
        self.background_color_result = ()
        button_rect = pg.Rect(225, 225 , 150, 100)
        pop_up_delay = 2500
        end_time = 0
        show_popup = False
        made_result = False

        pg.display.set_caption('TicTacToe')
        game_over = False
        
        while True:
            self.mouse_down = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_position = pg.mouse.get_pos()
                    self.mouse_down = True
                    if button_rect.collidepoint(self.mouse_position):
                        pass
            # Wipe screen.
            self.wipe_color(game_over, self.background_color_result)

            self.draw_board()
            if not game_over:

                current_player = self.robot if num_state % 2 else self.player
            
                if self.mouse_down and current_player == self.player:
                    index = self.find_index_mouse_position(self.mouse_position)
                    if current_player.play(self.game, index):
                        num_state += 1
                
                if current_player == self.robot:
                    current_player.play(self.game, None)
                    num_state += 1
            
            self.draw_symbols(self.game.board) 

            is_win , winning_symbol = self.game.check_for_win()
            
            if is_win:
                game_over = True
                if winning_symbol == self.player.symbol:
                    self.background_color_result = WIN_COLOR

                elif winning_symbol == self.robot.symbol:
                    self.background_color_result = LOSE_COLOR
                
                made_result = True
            if not is_win and self.game.empty_space() == False:
                game_over = True
                self.background_color_result = TIE_COLOR
                made_result = True

            if game_over and made_result:
                if end_time == 0:
                    end_time = pg.time.get_ticks()
                self.replay_button(button_rect)

            pg.display.flip()
            self.clock.tick(60)
            


            
    def draw_board(self):
        for i in range(1, GAME_SIZE):
            pg.draw.line(self.screen, LINE_COLOR, (((WINDOW_SIZE / GAME_SIZE) * i), 0), (((WINDOW_SIZE / GAME_SIZE) * i), WINDOW_SIZE), 10)
            pg.draw.line(self.screen, LINE_COLOR, (0, ((WINDOW_SIZE / GAME_SIZE) * i)) , (WINDOW_SIZE, ((WINDOW_SIZE / GAME_SIZE) * i)), 10)

    def draw_o(self, positon):
        offset = CELL_SIZE // FIXED_SCALAR
        scaled_width = (90 // GAME_SIZE)
        pg.draw.circle(self.screen, O_COLOR, positon, offset, scaled_width)

    def draw_x(self, postion):
        offset = CELL_SIZE // FIXED_SCALAR
        scaled_width = (90 // GAME_SIZE)
        pg.draw.line(self.screen, X_COLOR, postion, (postion[0] + offset, postion[1] + offset), scaled_width)
        pg.draw.line(self.screen, X_COLOR, postion, (postion[0] - offset, postion[1] - offset), scaled_width)
        pg.draw.line(self.screen, X_COLOR, postion, (postion[0] + offset, postion[1] - offset), scaled_width)
        pg.draw.line(self.screen, X_COLOR, postion, (postion[0] - offset, postion[1] + offset), scaled_width)


    
    def draw_symbols(self, board):
        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                pixel_cord = self.find_center_sqr_px((row_index, col_index))
                if board[row_index][col_index] == 1:
                    self.draw_o(pixel_cord)
                elif board[row_index][col_index] == 0:
                    self.draw_x(pixel_cord)


    def find_center_sqr_px(self, sqr_idx):
        """Uses the index to find the center pixel of a square in the board for alining the drawing."""
        col_pix = 100 * (sqr_idx[0] + sqr_idx[0] + 1)
        row_pix = 100 * (sqr_idx[1] + sqr_idx[1] + 1)
        return (row_pix, col_pix)
    
    def find_index_mouse_position(self, mouse_pos):
        # mouse_pos = (x, y)
        col = mouse_pos[0] // CELL_SIZE
        row = mouse_pos[1] // CELL_SIZE
        return (row, col)

    def wipe_color(self, game_state, color):
        if not game_state:
            self.screen.fill(BG_COLOR)
        else:
            self.screen.fill(color)

    def replay_button(self, button):
        pg.draw.rect(self.screen, (250, 250, 250), button)

TicTacToe().run()