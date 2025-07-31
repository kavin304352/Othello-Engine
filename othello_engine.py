#Kavin Ilanchezhian

import math
import random
from copy import deepcopy

#used typing for clarity when explaining to non python users :)
from typing import List, Tuple, Optional


# board representation
BLACK, WHITE, EMPTY = 1, -1, 0

# directions to move 
_DIRS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1),
]

# using heuristics from resarching, here are positional weights I decided on
_POS_WEIGHTS = [
    [100, -20, 10,  5,  5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10,  -2,  -1, -1, -1, -1,  -2,  10],
    [5,   -2,  -1, -1, -1, -1,  -2,   5],
    [5,   -2,  -1, -1, -1, -1,  -2,   5],
    [10,  -2,  -1, -1, -1, -1,  -2,  10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10,  5,  5, 10, -20, 100],
]

class OthelloBoard:
    SIZE = 8

    def __init__(self) -> None:
        self.grid: List[List[int]] = [[EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        mid = self.SIZE // 2
        

        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK

    
    def copy(self) -> "OthelloBoard":
        return deepcopy(self)

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.SIZE and 0 <= c < self.SIZE

    
    # different type of moves listed down below
    
    def _captures_in_dir(self, r: int, c: int, dr: int, dc: int, player: int) -> List[Tuple[int, int]]:
        #this method will return a list of all captured pieces
        captures = []
        i, j = r + dr, c + dc
        while self._in_bounds(i, j) and self.grid[i][j] == -player:
            captures.append((i, j))
            i += dr
            j += dc
        if self._in_bounds(i, j) and self.grid[i][j] == player and captures:
            return captures
        return []

    def legal_moves(self, player: int) -> List[Tuple[int, int]]:
        #this method will return a list of all legal moves
        moves = []
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] != EMPTY:
                    continue
                for dr, dc in _DIRS:
                    if self._captures_in_dir(r, c, dr, dc, player):
                        moves.append((r, c))
                        break
        return moves

    def apply_move(self, player: int, move: Tuple[int, int]) -> None:
        #this method acctually does the move and then flips the corresponding pieces
        r, c = move
        self.grid[r][c] = player
        for dr, dc in _DIRS:
            flips = self._captures_in_dir(r, c, dr, dc, player)
            for fr, fc in flips:
                self.grid[fr][fc] = player

    #helper methods
    def disk_counts(self) -> Tuple[int, int]:
        #return number of black and white disks
        black = sum(cell == BLACK for row in self.grid for cell in row)
        white = sum(cell == WHITE for row in self.grid for cell in row)
        return black, white

    def terminal(self) -> bool:
        return not self.legal_moves(BLACK) and not self.legal_moves(WHITE)

    # HERE IS THE ADDED EVALUATION FUNCTION!!!
    def evaluate(self, player: int) -> int:
        opponent = -player
        black, white = self.disk_counts()
        parity = black - white if player == BLACK else white - black

        positional_score = 0
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] == player:
                    positional_score += _POS_WEIGHTS[r][c]
                elif self.grid[r][c] == opponent:
                    positional_score -= _POS_WEIGHTS[r][c]
        # implements the chosen weights for each position
        return 10 * parity + positional_score

'''
 Negamax search with alpha‑beta pruning
'''

def negamax(board: OthelloBoard, player: int, depth: int, alpha: int, beta: int) -> Tuple[int, Optional[Tuple[int, int]]]:
    # return (score, best_move) for the player up to depth using negamax alpha beta pruning.
    if depth == 0 or board.terminal():
        return board.evaluate(player), None

    best_move: Optional[Tuple[int, int]] = None
    max_score = -math.inf
    moves = board.legal_moves(player)

    # edge case, we pass the move if no legal moves
    if not moves:
        score, _ = negamax(board, -player, depth - 1, -beta, -alpha)
        return -score, None

    for move in moves:
        child = board.copy()
        child.apply_move(player, move)
        score, _ = negamax(child, -player, depth - 1, -beta, -alpha)
        score = -score

        if score > max_score:
            max_score = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break  
            #alpha beta pruning algo

    return max_score, best_move

#method that calles negamax 
def best_move(board: OthelloBoard, player: int, depth: int = 5) -> Tuple[int, int]:
    # use negamax and then return the best move
    _, move = negamax(board, player, depth, -math.inf, math.inf)
    if move is None:
        raise ValueError("No legal moves available")
    return move

#testing purposes
def play_game(depth_black: int = 4, depth_white: int = 4, verbose: bool = False) -> int:
    # return the winner after self‑play.
    board = OthelloBoard()
    player = BLACK

    depths = {BLACK: depth_black, WHITE: depth_white}

    while not board.terminal():
        moves = board.legal_moves(player)
        if moves:
            move = best_move(board, player, depths[player])
            board.apply_move(player, move)
            if verbose:
                print(f"Player {'B' if player==BLACK else 'W'} -> {move}")
        player = -player  # go to other players turn

    black, white = board.disk_counts()
    if verbose:
        print("Final score – Black:", black, "White:", white)
    return BLACK if black > white else WHITE if white > black else 0

# for testing
if __name__ == "__main__":
    random.seed(0)
    winner = play_game(depth_black=3, depth_white=3, verbose=True)
    print("Winner: ", "Black" if winner == BLACK else "White" if winner == WHITE else "Draw")
