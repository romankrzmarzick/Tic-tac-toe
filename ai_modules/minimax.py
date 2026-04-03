import math

class MinimaxAi:
    def __init__(self, ai_symbol, opponent_symbol):
        self.ai_symbol = ai_symbol
        self.opponent_symbol = opponent_symbol

    def choose_move(self, board):
        best_score = -math.inf
        move = None
        
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    board[r][c] = self.ai_symbol
                    # Start recursion to see where this move leads
                    score = self.minimax(board, 0, False)
                    board[r][c] = None # Undo move
                    
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        return move

    def minimax(self, board, depth, is_maximizing):
        # 1. Base Case: Check for terminal states (win/loss/tie)
        # Using a simplified version of your win logic
        state = self.check_status(board)
        if state == self.ai_symbol: return 10 - depth
        if state == self.opponent_symbol: return depth - 10
        if not any(None in row for row in board): return 0

        if is_maximizing:
            best_score = -math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] is None:
                        board[r][c] = self.ai_symbol
                        score = self.minimax(board, depth + 1, False)
                        board[r][c] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] is None:
                        board[r][c] = self.opponent_symbol
                        score = self.minimax(board, depth + 1, True)
                        board[r][c] = None
                        best_score = min(score, best_score)
            return best_score

    def check_status(self, board):
        # Simplified win check specifically for the AI's internal simulations
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None: return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None: return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None: return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None: return board[0][2]
        return None