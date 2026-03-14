from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.text import Text

class Interface:
    def __init__(self) -> None:
        self.symbols = ["x", "o"]
        self.con = Console()
        self.styles = {
            "main" : "white bold",
            "body" : "white"
        }

    def display_board(self, board):
        for row in board:
            self.con.print(f"|{'|'.join(row)}|", style=self.styles['body'])

    def choose_square_size(self) -> int:
        size_map = {"3x3" : 3, "5x5" : 5, "7x7" : 7}
        size_choice = [x for x in size_map.keys()]
        square_width = Prompt.ask(Text("Tic-tac-toe square size", style=self.styles['main']), choices=size_choice).strip()
        return size_map.get(square_width, 3)
    
    def symbol_nomination(self):
        p1_symbol = Prompt.ask(Text("Choose symbol", style=self.styles['main']), case_sensitive=False, choices=self.symbols).lower().strip()
        r1_symbol = [x for x in self.symbols if not x == p1_symbol][0]
        return p1_symbol, r1_symbol
    
    def choose_position(self, square_width: int, name) -> int:
        number_choices = []
        for i in range(1, (square_width * square_width) + 1):
            number_choices.append(str(i))

        number = (Prompt.ask(Text(f"{name}'s Turn", style=self.styles['main']), show_choices=False, choices=number_choices)).strip()
        return int(number) - 1
    
    def choose_name(self) -> str:
        while True:
            name = Prompt.ask(Text("Enter a name", style=self.styles["main"])).lower().title()
    
            if 0 < len(name) <= 15:
                break
            elif not len(name):
                self.con.print("Name is Empty: enter a valid one please.", style=self.styles["lose"])
            else:
                self.con.print("Name is over 15 Characters: enter a new one please.", style=self.styles["lose"])
        
        return name

    def invalid_move_message(self):
        self.con.print("Invalid move: try again.", style=self.styles['body'])
