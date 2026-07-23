import pygame

from constants import (
    WINDOW_SIZE,
    GAME_BOARD_SIZE,
    SYMBOL_O,
    SYMBOL_X,
    DIFFICULTIES,
)


class Render:
    FONT = "Arial"

    # --- Teal colour format (kept from the original design) ---
    BG_COLOR = (0, 200, 200)          # base teal, kept for compatibility
    BG_TOP = (0, 214, 208)            # gradient top
    BG_BOTTOM = (0, 150, 150)         # gradient bottom
    GRID_COLOR = (0, 138, 138)        # board lines
    GRID_HILIGHT = (0, 224, 216)      # thin highlight on the lines
    SHADOW_COLOR = (0, 110, 110)      # soft drop shadow
    HOVER_COLOR = (255, 255, 255, 55)  # translucent cell hover
    PANEL_COLOR = (0, 120, 120, 210)  # translucent pill/panel
    BUTTON_COLOR = (255, 255, 255)
    BUTTON_TEXT = (0, 140, 140)
    FONT_COLOR = (40, 60, 60)
    COLOR_MAP = {SYMBOL_X: (45, 52, 64), SYMBOL_O: (250, 250, 252)}

    def __init__(self, screen):
        self.screen = screen
        self.window_size = WINDOW_SIZE
        self.square_width = GAME_BOARD_SIZE
        self.cell_size = self.window_size // self.square_width
        self.symbol_map = {SYMBOL_O: self.draw_o, SYMBOL_X: self.draw_x}
        self._background = self._build_background()

    # ---------- shared helpers ----------
    def _build_background(self):
        """Pre-render a vertical teal gradient so we don't recompute each frame."""
        surface = pygame.Surface((self.window_size, self.window_size))
        top, bottom = self.BG_TOP, self.BG_BOTTOM
        for y in range(self.window_size):
            t = y / max(1, self.window_size - 1)
            color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
            pygame.draw.line(surface, color, (0, y), (self.window_size, y))
        return surface

    def clear_screen(self):
        self.screen.blit(self._background, (0, 0))

    def make_font(self, size_ratio):
        size = int(self.window_size * size_ratio)
        return pygame.font.SysFont(self.FONT, size, True)

    def draw_o(self, pixel_pos, draw_offset, draw_width):
        pygame.draw.circle(self.screen, self.COLOR_MAP[SYMBOL_O], pixel_pos, draw_offset, draw_width)

    def draw_x(self, pixel_pos, draw_offset, draw_width):
        cx, cy = pixel_pos
        color = self.COLOR_MAP[SYMBOL_X]
        p1 = (cx - draw_offset, cy - draw_offset)
        p2 = (cx + draw_offset, cy + draw_offset)
        p3 = (cx + draw_offset, cy - draw_offset)
        p4 = (cx - draw_offset, cy + draw_offset)
        # strokes
        pygame.draw.line(self.screen, color, p1, p2, draw_width)
        pygame.draw.line(self.screen, color, p3, p4, draw_width)
        # rounded end-caps for a softer look
        cap = draw_width // 2
        for point in (p1, p2, p3, p4):
            pygame.draw.circle(self.screen, color, point, cap)

    def draw_pill_button(self, rect, label, size_ratio, hovered,
                         base=None, text_color=None):
        base = base if base is not None else self.BUTTON_COLOR
        text_color = text_color if text_color is not None else self.BUTTON_TEXT
        radius = rect.height // 2
        # drop shadow
        shadow = rect.move(0, max(3, self.window_size // 200))
        pygame.draw.rect(self.screen, self.SHADOW_COLOR, shadow, border_radius=radius)
        # lift the button slightly on hover
        color = tuple(min(255, c + 12) for c in base) if hovered else base
        draw_rect = rect.move(0, -max(2, self.window_size // 320)) if hovered else rect
        pygame.draw.rect(self.screen, color, draw_rect, border_radius=radius)
        font = self.make_font(size_ratio)
        text = font.render(label, True, text_color)
        self.screen.blit(text, text.get_rect(center=draw_rect.center))


class RenderPlay(Render):
    def __init__(self, screen):
        super().__init__(screen)
        self.pixel_multiplier = self.cell_size * 0.5
        self.line_width = self.window_size // 70
        self.draw_width = self.cell_size // 6
        self.draw_offset = self.cell_size * 3 // 9

    def convert_index(self, sqr_idx: tuple) -> tuple:
        """Convert a board (row, col) index to a pixel (x, y) cell centre."""
        row, col = sqr_idx
        x = self.pixel_multiplier * (2 * col + 1)
        y = self.pixel_multiplier * (2 * row + 1)
        return (x, y)

    def draw_board(self):
        # Interior grid lines span the full board so cells stay evenly spaced.
        for i in range(1, self.square_width):
            pos = self.cell_size * i
            # vertical line (line + slim highlight)
            pygame.draw.line(self.screen, self.GRID_COLOR, (pos, 0), (pos, self.window_size), self.line_width)
            pygame.draw.line(self.screen, self.GRID_HILIGHT, (pos, 0), (pos, self.window_size), max(1, self.line_width // 4))
            # horizontal line
            pygame.draw.line(self.screen, self.GRID_COLOR, (0, pos), (self.window_size, pos), self.line_width)
            pygame.draw.line(self.screen, self.GRID_HILIGHT, (0, pos), (self.window_size, pos), max(1, self.line_width // 4))

    def draw_hover(self, cell):
        """Highlight an empty cell under the cursor."""
        row, col = cell
        inset = int(self.cell_size * 0.06)
        rect = pygame.Rect(
            col * self.cell_size + inset,
            row * self.cell_size + inset,
            self.cell_size - inset * 2,
            self.cell_size - inset * 2,
        )
        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(overlay, self.HOVER_COLOR, overlay.get_rect(),
                         border_radius=int(self.cell_size * 0.12))
        self.screen.blit(overlay, rect.topleft)

    def draw_symbols(self, board):
        for row_index, row in enumerate(board):
            for col_index, _ in enumerate(row):
                cell = board[row_index][col_index]
                if cell in self.symbol_map:
                    pixel_cord = self.convert_index((row_index, col_index))
                    self.symbol_map[cell](pixel_cord, self.draw_offset, self.draw_width)

    def draw_status(self, text):
        """Draw a translucent status pill near the top of the board."""
        font = self.make_font(0.045)
        label = font.render(text, True, (255, 255, 255))
        pad_x = int(self.window_size * 0.03)
        pad_y = int(self.window_size * 0.018)
        width = label.get_width() + pad_x * 2
        height = label.get_height() + pad_y * 2
        pill = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(pill, self.PANEL_COLOR, pill.get_rect(), border_radius=height // 2)
        rect = pill.get_rect(center=(self.window_size // 2, int(self.window_size * 0.07)))
        self.screen.blit(pill, rect)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def color_strike(self, winning_symbol):
        return self.COLOR_MAP.get(winning_symbol, (255, 80, 80))

    def draw_strike(self, strike_pos, winning_symbol):
        color = self.color_strike(winning_symbol)
        start = self.convert_index(strike_pos[0])
        end = self.convert_index(strike_pos[1])
        pygame.draw.line(self.screen, color, start, end, self.draw_width)


class RenderMenu(Render):
    # Vertical layout anchors, as a fraction of the window height. Each element
    # is centred on its anchor so the spacing between them stays even.
    TITLE_CY = 0.19
    SUBTITLE_CY = 0.33
    BUTTON_START_CY = 0.48
    BUTTON_GAP = 0.155

    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = {}
        button_w = int(self.window_size * 0.5)
        button_h = int(self.window_size * 0.115)
        cx = int(self.window_size / 2)
        start_y = self.window_size * self.BUTTON_START_CY
        gap = self.window_size * self.BUTTON_GAP
        for i, level in enumerate(DIFFICULTIES):
            rect = pygame.Rect(0, 0, button_w, button_h)
            rect.center = (cx, int(start_y + i * gap))
            self.buttons[level] = rect

    def render(self, mouse_pos):
        self.clear_screen()
        cx = self.window_size // 2

        # Title "Tic Tac Toe" with X / O accent colours, centred on TITLE_CY.
        title_font = self.make_font(0.11)
        parts = [("Tic ", (45, 52, 64)), ("Tac ", (250, 250, 252)), ("Toe", (45, 52, 64))]
        rendered = [(title_font.render(t, True, col),
                     title_font.render(t, True, self.SHADOW_COLOR)) for t, col in parts]
        total_w = sum(surf.get_width() for surf, _ in rendered)
        title_h = max(surf.get_height() for surf, _ in rendered)
        top = int(self.window_size * self.TITLE_CY) - title_h // 2
        x = cx - total_w // 2
        for surf, shadow in rendered:
            self.screen.blit(shadow, (x + 3, top + 3))
            self.screen.blit(surf, (x, top))
            x += surf.get_width()

        subtitle_font = self.make_font(0.045)
        subtitle = subtitle_font.render("Choose your difficulty", True, (255, 255, 255))
        self.screen.blit(subtitle, subtitle.get_rect(center=(cx, int(self.window_size * self.SUBTITLE_CY))))

        for level, rect in self.buttons.items():
            hovered = rect.collidepoint(mouse_pos) if mouse_pos else False
            self.draw_pill_button(rect, level, 0.05, hovered)


class RenderReplay(Render):
    def __init__(self, screen):
        super().__init__(screen)
        self.result_rect = pygame.Rect(self.window_size * (1 / 3), self.window_size * (5 / 8),
                                       self.window_size * (1 / 3), self.window_size * (1 / 8))
        button_w = int(self.window_size * 0.34)
        button_h = int(self.window_size * 0.11)
        cx = self.window_size / 2
        self.again_rect = pygame.Rect(0, 0, button_w, button_h)
        self.again_rect.center = (cx, int(self.window_size * 0.8))
        self.menu_rect = pygame.Rect(0, 0, button_w, button_h)
        self.menu_rect.center = (cx, int(self.window_size * 0.92))
        self.draw_offset = (self.window_size // 3) * 3 // 9
        self.draw_width = (self.window_size // 3) // 6

    def result_message(self, is_win, winning_symbol):
        if is_win:
            result_text = "YOU WIN!"
        elif winning_symbol is not None:
            result_text = "YOU LOSE"
        else:
            result_text = "IT'S A TIE"
        font = self.make_font(0.1)
        text = font.render(result_text, True, self.FONT_COLOR)
        self.screen.blit(text, text.get_rect(center=self.result_rect.center))

    def end_results(self, is_win, winning_symbol):
        if winning_symbol in self.symbol_map:
            self.symbol_map[winning_symbol]((self.window_size // 2, int(self.window_size * 0.34)),
                                            self.draw_offset, self.draw_width)
        else:
            self.draw_x((self.window_size * 3 // 8, int(self.window_size * 0.34)), self.draw_offset, self.draw_width)
            self.draw_o((self.window_size * 5 // 8, int(self.window_size * 0.34)), self.draw_offset, self.draw_width)
        self.result_message(is_win, winning_symbol)

    def render(self, is_win, winning_symbol, mouse_pos):
        self.clear_screen()
        self.end_results(is_win, winning_symbol)
        again_hover = self.again_rect.collidepoint(mouse_pos) if mouse_pos else False
        menu_hover = self.menu_rect.collidepoint(mouse_pos) if mouse_pos else False
        self.draw_pill_button(self.again_rect, "Play Again", 0.04, again_hover)
        self.draw_pill_button(self.menu_rect, "Menu", 0.04, menu_hover)
