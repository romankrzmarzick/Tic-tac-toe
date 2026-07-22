import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import math
import random
from itertools import product

from constants import GAME_BOARD_SIZE


class MinimaxAI:
    """Unbeatable opponent (on a 3x3 board) using minimax with alpha-beta pruning.

    For larger boards a full search is too expensive, so the search depth is
    capped and the AI plays a strong-but-not-perfect game there.
    """

    def __init__(self, player_symbol, robot_symbol):
        self.p_symbol = player_symbol
        self.r_symbol = robot_symbol
        self.n = GAME_BOARD_SIZE
        # 3x3 is small enough to solve exactly; cap deeper boards for speed.
        self.max_depth = 9 if self.n == 3 else 4

    def choose_move(self, board):
        n = self.n
        available = [(r, c) for r, c in product(range(n), repeat=2) if board[r][c] is None]

        # Opening move: skip the full search and grab the center for speed/variety.
        if len(available) == n * n:
            return (n // 2, n // 2)

        best_score = -math.inf
        best_moves = []
        for (r, c) in available:
            board[r][c] = self.r_symbol
            score = self._minimax(board, 0, False, -math.inf, math.inf)
            board[r][c] = None
            if score > best_score:
                best_score = score
                best_moves = [(r, c)]
            elif score == best_score:
                best_moves.append((r, c))
        return random.choice(best_moves)

    def _minimax(self, board, depth, maximizing, alpha, beta):
        winner = self._winner(board)
        if winner == self.r_symbol:
            return 10 - depth
        if winner == self.p_symbol:
            return depth - 10
        if not self._has_empty(board) or depth >= self.max_depth:
            return 0

        if maximizing:
            best = -math.inf
            for (r, c) in self._empties(board):
                board[r][c] = self.r_symbol
                best = max(best, self._minimax(board, depth + 1, False, alpha, beta))
                board[r][c] = None
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = math.inf
            for (r, c) in self._empties(board):
                board[r][c] = self.p_symbol
                best = min(best, self._minimax(board, depth + 1, True, alpha, beta))
                board[r][c] = None
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

    def _empties(self, board):
        n = self.n
        return [(r, c) for r, c in product(range(n), repeat=2) if board[r][c] is None]

    def _has_empty(self, board):
        return any(None in row for row in board)

    def _winner(self, board):
        n = self.n

        def line_winner(line):
            first = line[0]
            if first is not None and all(cell == first for cell in line):
                return first
            return None

        lines = list(board)  # rows
        lines += [[board[r][c] for r in range(n)] for c in range(n)]  # columns
        lines.append([board[i][i] for i in range(n)])  # main diagonal
        lines.append([board[(n - 1) - i][i] for i in range(n)])  # anti diagonal

        for line in lines:
            w = line_winner(line)
            if w is not None:
                return w
        return None
