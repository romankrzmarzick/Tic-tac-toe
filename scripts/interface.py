from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.text import Text

class Interface:
    def __init__(self) -> None:
        self.symbols = ["x", "o"]
        self.con = Console()
        self.styles = {
            "main" : "white bold",
            "body" : "white",
            "invalid" : "red",
            "board" : "blue bold"
        }   
    
    #--- Board Display Functions ---
    
    def num_rule_board(self, game):
        print("+----------------------+\n")
        for row_idx in range(game.sqr_wt):
            row_numbers = [(row_idx * game.sqr_wt + col_idx + 1) for col_idx in range(game.sqr_wt)]
            self.con.print(f"|{'|'.join(map(str, row_numbers))}|", style=self.styles['main'])
            
    def display_board(self, board):
        for row in board:
            self.con.print(f"|{'|'.join(row)}|", style=self.styles['board'])
   
    # --- Input Functions ---
    def symbol_nomination(self):
        p1_symbol = Prompt.ask(Text("Choose symbol", style=self.styles['main']), case_sensitive=False, choices=self.symbols).lower().strip()
        r1_symbol = [x for x in self.symbols if not x == p1_symbol][0]
        return p1_symbol, r1_symbol
    
    def choose_position(self, square_width: int, name) -> int:
        number_choices = []
        for i in range(1, (square_width * square_width) + 1):
            number_choices.append(str(i))
        number = (Prompt.ask(Text(f"\n{name}'s Turn", style=self.styles['main']), show_choices=False, choices=number_choices)).strip()
        return int(number) - 1
    
    def choose_name(self) -> str:
        while True:
            name = Prompt.ask(Text("Enter a name", style=self.styles["main"])).lower().title()
    
            if 0 < len(name) <= 15:
                break
            elif not len(name):
                self.con.print("Name is Empty: enter a valid one please.", style=self.styles["invalid"])
            else:
                self.con.print("Name is over 15 Characters: enter a new one please.", style=self.styles["invalid"])
        return name
    
    def replay(self) -> bool:
        return Confirm.ask(Text(f"Play Again?", style=self.styles["main"]))

    # --- Validator Functions ---
    def invalid_move_message(self):
        self.con.print("Invalid move: try again.", style=self.styles['invalid'])

    # --- Display Result Functions ---
    def is_victory(self):
        self.con.print("\nYOU WON!", style=self.styles['main'])

    def is_defeat(self):
        self.con.print("\nYOU LOST!", style=self.styles['main'])

    def is_draw(self):
        self.con.print("\nIT'S A TIE.", style=self.styles['main'])
