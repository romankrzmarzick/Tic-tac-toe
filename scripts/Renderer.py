import pygame
from constants import WINDOW_SIZE, GAME_BOARD_SIZE, symbol_o, symbol_x

class Render:  
    FONT = "Arial" 
    BG_COLOR = (0, 200, 200)
    COLOR_MAP = {symbol_x : (50, 50, 50), symbol_o : (255, 255, 255)}
    def __init__(self, screen):
        self.screen = screen
        self.window_size = WINDOW_SIZE
        self.square_width = GAME_BOARD_SIZE
        self.cell_size = self.window_size // self.square_width
        self.symbol_map = {symbol_o : self.draw_o, symbol_x : self.draw_x}


    def clear_screen(self):
        # Wipes screen when called.
        self.screen.fill(self.BG_COLOR)

    def make_font(self, size_ratio):
        size = int(self.window_size * size_ratio)
        return pygame.font.SysFont(self.FONT, size, True)
       
    def draw_o(self, pixel_pos, draw_offset, draw_width):
        pygame.draw.circle(self.screen, self.COLOR_MAP[symbol_o], pixel_pos, draw_offset, draw_width)

    def draw_x(self, pixel_pos, draw_offset, draw_width):
        pygame.draw.line(self.screen, self.COLOR_MAP[symbol_x], pixel_pos, (pixel_pos[0] + draw_offset, pixel_pos[1] + draw_offset),draw_width)
        pygame.draw.line(self.screen, self.COLOR_MAP[symbol_x], pixel_pos, (pixel_pos[0] - draw_offset, pixel_pos[1] - draw_offset), draw_width)
        pygame.draw.line(self.screen, self.COLOR_MAP[symbol_x], pixel_pos, (pixel_pos[0] + draw_offset, pixel_pos[1] - draw_offset), draw_width)
        pygame.draw.line(self.screen, self.COLOR_MAP[symbol_x], pixel_pos, (pixel_pos[0] - draw_offset, pixel_pos[1] + draw_offset), draw_width)

class RenderPlay(Render):
    LINE_COLOR = (0, 150, 150)  
    def __init__(self, screen):
        super().__init__(screen)
        self.pixel_multiplier = self.cell_size * (1/2)
        self.line_width = self.window_size // 60
        self.draw_width = self.cell_size // 5
        self.draw_offset = self.cell_size * 3 // 9

    def convert_index(self, sqr_idx: tuple) -> tuple:
        """Takes the index agrument and converts to the position on the board in pixels."""
   
        col_pix = self.pixel_multiplier * (sqr_idx[0] + sqr_idx[0] + 1)
        row_pix = self.pixel_multiplier * (sqr_idx[1] + sqr_idx[1] + 1)
        return (row_pix, col_pix)
    
    def draw_board(self):
        for i in range(1, self.square_width):
            pygame.draw.line(self.screen, self.LINE_COLOR, (((self.cell_size) * i), 0), (((self.cell_size) * i), self.window_size), self.line_width)
            pygame.draw.line(self.screen, self.LINE_COLOR, (0, ((self.cell_size) * i)) , (self.window_size, ((self.cell_size) * i)), self.line_width)

    def draw_symbols(self, board):
        for row_index, row in enumerate(board):
            for col_index, _ in enumerate(row):
                cell = board[row_index][col_index]
                if cell in self.symbol_map:
                    pixel_cord = self.convert_index((row_index, col_index))
                    self.symbol_map[cell](pixel_cord, self.draw_offset, self.draw_width)

    def color_strike(self, winning_symbol):
        """Safely gets color from the map and returns the color red if the symbol wasn't found."""
        return self.COLOR_MAP.get(winning_symbol, (255, 0, 0))
        
    def draw_strike(self, strike_pos, winning_symbol):
        """
        Strike_pos are the two end indices that are passed in from game to help create the strike. 
        Color is found from the color_strike fucntion.
        """
        color = self.color_strike(winning_symbol)
        pygame.draw.line(self.screen, color, self.convert_index(strike_pos[0]), self.convert_index(strike_pos[1]) , self.draw_width)
                                                              

class RenderReplay(Render):
    FONT_COLOR = (50, 50, 50)
    BUTTON_COLOR = (255, 255, 255)
    
    def __init__(self, screen):
        super().__init__(screen)
        self.button_rect = pygame.Rect(self.window_size * (1/3), self.window_size * (7/8) , self.window_size * (1/3), self.window_size * (1/8))
        self.result_rect = pygame.Rect(self.window_size * (1/3), self.window_size * (5/8) , self.window_size * (1/3), self.window_size * (1/8))
        self.draw_offset = (self.window_size // 3) * 3 // 9
        self.draw_width = (self.window_size // 3) // 5

    def draw_button(self):
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.button_rect)
    
    def render_button(self):
        self.draw_button()
        font = self.make_font(.085)
        text = font.render("Replay?", True, self.FONT_COLOR)
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)

    def result_message(self, is_win):
        result_text = "WIN" if is_win else "TIE"
        font = self.make_font(.125)
        text = font.render(result_text, True, self.FONT_COLOR)
        text_rect = text.get_rect(center=self.result_rect.center)
        self.screen.blit(text, text_rect)

    def end_results(self, is_win, winning_symbol):
        
        
        if winning_symbol in self.symbol_map:
            self.symbol_map[winning_symbol]((self.window_size // 2, self.window_size // 2), self.draw_offset, self.draw_width)
        else:
            self.draw_x((self.window_size * 3 // 8, self.window_size // 2), self.draw_offset, self.draw_width)
            self.draw_o((self.window_size * 5 // 8, self.window_size // 2), self.draw_offset, self.draw_width)
        
        self.result_message(is_win)

   
