import pygame as pg
import sys
from scripts.game import Game
from scripts.character import User
from scripts.character import Robot
from ai_modules.minimax import MinimaxAi
from ai_modules.random_ai import RandomAi
from ai_modules.smart import SmartAi

ASSIGN_NUM = (1, 2)
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
        self.robot = Robot("Robot", ASSIGN_NUM[1], MinimaxAi(ASSIGN_NUM[1], ASSIGN_NUM[0]))
        self.font = pg.font.SysFont("Arial", 40, True)
        self.win_font = pg.font.SysFont("Arial", 75, True)

    def run(self):
        self.mouse_position = [0, 0]
        num_state = 0
        end_time = 0
        self.show_popup = False
        self.pop_up_delay = 1000
        self.strike_color = (0, 0, 0)
        button_rect = pg.Rect(0, 0, 0, 0)
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

                    if self.show_popup and button_rect.collidepoint(self.mouse_position):
                            self.game = Game(GAME_SIZE)
                            game_over = False
                            self.show_popup = False
                            num_state = 0
                            end_time = 0
                            self.mouse_down = False
                            pg.time.wait(500)
                    else: 
                        self.mouse_down = True
                    
                    
            # Wipe screen.
            self.wipe_color()

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

            is_win, winning_symbol, strike_index,  = self.game.check_for_win()
            
            if is_win:
                game_over = True
                self.color_strike(winning_symbol)
                self.draw_strike(strike_index)
                 
                if end_time == 0:
                    end_time = pg.time.get_ticks()
                

            if not is_win and self.game.empty_space() == False:
                game_over = True
             
                
                if end_time == 0:
                    end_time = pg.time.get_ticks()

            if game_over and end_time > 0:
                current_time = pg.time.get_ticks()

                if current_time - end_time >= self.pop_up_delay:
                        self.wipe_color()
                        self.replay_screen(winning_symbol)
                        win_rect = pg.Rect(200, 375 , 200, 75)
                        display_text = ""
                        if is_win:
                            display_text = "Won!"
                        else:
                            display_text = "Tie!"
                        text = self.win_font.render(display_text, True, (255, 255, 255))
                        text_win_rect = text.get_rect(center=win_rect.center)
                        self.screen.blit(text, text_win_rect)

                if current_time - end_time >= self.pop_up_delay:
                    self.show_popup = True


                    button_rect = pg.Rect(200, 525 , 200, 75)
                    self.replay_button(button_rect)
                    text_surf = self.font.render("Replay?", True, (0, 0, 0))
                    text_rect = text_surf.get_rect(center=button_rect.center)
                    self.screen.blit(text_surf, text_rect)

            pg.display.flip()
            self.clock.tick(60)

    def color_strike(self, winning_symbol):
        if winning_symbol == self.player.symbol:
            self.strike_color = (50, 50, 50)
        elif winning_symbol == self.robot.symbol:
            self.strike_color = (255, 255, 255)

    def draw_strike(self, strike_pos):
        start_pos = self.find_center_sqr_px(strike_pos[0])
        end_pos = self.find_center_sqr_px(strike_pos[1])
        pg.draw.line(self.screen, self.strike_color, start_pos, end_pos , 30)
            
    def find_center_sqr_px(self, sqr_idx):
        """Uses the index to find the center pixel of a square in the board for alining the drawing."""
        col_pix = 100 * (sqr_idx[0] + sqr_idx[0] + 1)
        row_pix = 100 * (sqr_idx[1] + sqr_idx[1] + 1)
        return (row_pix, col_pix)
    
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
            for col_index, _ in enumerate(row):
                pixel_cord = self.find_center_sqr_px((row_index, col_index))
                if board[row_index][col_index] == 2:
                    self.draw_o(pixel_cord)
                elif board[row_index][col_index] == 1:
                    self.draw_x(pixel_cord)


    def find_index_mouse_position(self, mouse_pos):
        # mouse_pos = (x, y)
        col = mouse_pos[0] // CELL_SIZE
        row = mouse_pos[1] // CELL_SIZE
        return (row, col)

    def wipe_color(self):
        self.screen.fill(BG_COLOR)
        

    def replay_button(self, button):
        pg.draw.rect(self.screen, (255, 255, 255), button)
        pg.draw.rect(self.screen, (0, 0, 0), button, 2)
    
   
    def replay_screen(self, winning_symbol):
        if winning_symbol == self.player.symbol:
            self.draw_x((300, 300))
        elif winning_symbol == self.robot.symbol:
            self.draw_o((300, 300))
        else:
            self.draw_x((230, 300))
            self.draw_o((370, 300))
TicTacToe().run()