import pygame as pg
import sys

WINDOW_SIZE = 600
GAME_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GAME_SIZE
BG_COLOR = (0, 200, 200)
LINE_COLOR = (0, 150, 150)
X_COLOR = (50, 50, 50)
O_COLOR = (255, 255, 255)

pg.init()

class TicTacToe:
    def __init__(self):
        self.screen = pg.display.set_mode([WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()

    mouse_position = (0, 0)
    
    button_rect = pg.Rect(150, 250, 300, 100)


    def run(self):
        pg.display.set_caption('TicTacToe')
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_position = pg.mouse.get_pos()
                  
            self.screen.fill(BG_COLOR)

            self.draw_board()

            self.draw_o((100, 100))
            self.draw_x((300, 300))

            pg.display.flip()
            self.clock.tick(60)
            
        

            
    def draw_board(self):
        for i in range(1, GAME_SIZE):
            pg.draw.line(self.screen, LINE_COLOR, (((WINDOW_SIZE / GAME_SIZE) * i), 0), (((WINDOW_SIZE / GAME_SIZE) * i), WINDOW_SIZE), 10)
            pg.draw.line(self.screen, LINE_COLOR, (0, ((WINDOW_SIZE / GAME_SIZE) * i)) , (WINDOW_SIZE, ((WINDOW_SIZE / GAME_SIZE) * i)), 10)

    def draw_o(self, positon):
        pg.draw.circle(self.screen, O_COLOR, positon, 70, 30)

    def draw_x(self, postion):
        pg.draw.line(self.screen, X_COLOR, postion, (postion[0] + 60, postion[1] + 60), 35)
        pg.draw.line(self.screen, X_COLOR, postion, (postion[0] - 60, postion[1] - 60), 35)
        pg.draw.line(self.screen, X_COLOR, postion, (postion[0] + 60, postion[1] - 60), 35)
        pg.draw.line(self.screen, X_COLOR, postion, (postion[0] - 60, postion[1] + 60), 35)


TicTacToe().run()