# Tic-tac-toe

A polished Python and Pygame version of Tic-Tac-Toe against a computer opponent.
Pick a difficulty from the menu, click a square to play, and use the buttons on the
results screen to start another round or return to the menu.

## Running it

Install the dependency:

```bash
pip install pygame
```

Start the game from the project folder:

```bash
python main.py
```

## Controls

Mouse only — pick a difficulty on the menu, then click the square you want.

## Difficulty levels

Choose one from the start menu:

- **Easy** — `random_ai.py`, plays any open square and is simple to beat.
- **Medium** — `smart_ai.py`, tries to win, blocks your winning move, then takes the center and corners.
- **Hard** — `minimax_ai.py`, uses minimax with alpha-beta pruning and is unbeatable on a 3x3 board (the search is depth-capped on larger boards to stay responsive).

## Project structure

- main.py — launches the game loop
- scripts/state_pattern.py — handles the menu, play, and replay states
- scripts/game.py — manages the board and win detection
- scripts/renderer.py — draws the menu, board, symbols, and end screen
- scripts/character.py — defines the player and robot classes
- ai_modules/ — the three AI opponents
- constants.py — window size, board size, and difficulty settings

The grid is not hard-coded. It currently ships as 5x5 — change `GAME_BOARD_SIZE`
in constants.py to 3, 5, or 7 and the board, win detection, and AI will adapt.
