# Tic-tac-toe

Tic-tac-toe in Python and pygame, played against the computer. Click a square to take it.
When the game ends you can click to play again.

## Running it

You need Python and pygame:

```
pip install pygame
```

Then run it from the project folder:

```
python main.py
```

## Controls

Mouse only — click the square you want.

## The computer opponent

There are two opponents in `ai_modules/`:

- **`random_ai.py`** — picks any open square. Easy to beat.
- **`smart_ai.py`** — actually tries. In order, it will:
  1. Take a winning move if it has one
  2. Block you if you're about to win
  3. Take the center
  4. Take a corner
  5. Otherwise pick at random

It's a set of rules rather than a search, so it's quick and hard to beat without being
literally unbeatable.

## How it's put together

- `main.py` — starts the game and runs the loop
- `scripts/state_pattern.py` — handles what screen you're on (playing, game over)
- `scripts/game.py` — the board and the win checking
- `scripts/Renderer.py` — draws everything
- `scripts/character.py` — the players
- `constants.py` — window and board size

The grid isn't hard-coded to 3×3 — change `GAME_BOARD_SIZE` in `constants.py` to 5 or 7
and the board, the win check, and the computer opponent all adjust.
