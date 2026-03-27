# Tic-tac-toe

A simple terminal Tic-tac-toe game written in Python. Play against a robot opponent that uses a random move strategy.

## Features

- Player vs robot gameplay
- Input validation for names and moves
- Colored terminal output using `rich`
- Replay option after each match

## Requirements

- Python 3.9+
- `rich`

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Project Structure

```text
main.py
ai_modules/
	random_ai.py
scripts/
	character.py
	game.py
	interface.py
```

## Notes

- This project is a learning-friendly terminal implementation.
- AI currently chooses from available spaces at random.

## License

This project is licensed under the terms in [LICENSE](LICENSE).

