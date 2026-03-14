from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.text import Text

class Interface:
    def __init__(self) -> None:
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
        size = Prompt.ask(Text("Tic-tac-toe square size", style=self.styles['main']), choices=size_choice).strip()
        return size_map.get(size, 3)
    
    def choose_symbol(self):
        return Prompt.ask(Text("Choose symbol", style=self.styles['main']), case_sensitive=False, choices=["X", "O"]).lower().strip()
    
    def choose_position(self, size: int) -> int:
        number_choices = []
        for i in range(1, (size * size) + 1):
            number_choices.append(str(i))

        number = (Prompt.ask(Text("Where shall you go", style=self.styles['main']), show_choices=False, choices=number_choices)).strip()
        next_1 = int(number) - 1
        print(next_1)
        return next_1
ui = Interface()

ui.choose_position(5)