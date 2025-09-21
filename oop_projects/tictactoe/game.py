# game.py
from enum import Enum, auto
from typing import Optional, Tuple, List

from board import Board
from player import Player

class GameState(Enum):
    IN_PROGRESS = auto()
    WIN = auto()
    DRAW = auto()

class Game:
    """
    Turn-based Tic Tac Toe engine (no I/O).
    Responsibilities:
      - Own a Board and two Players.
      - Track whose turn it is.
      - Apply moves (row, col) for the current player.
      - Detect winner/draw; lock the game when it ends.
    Public API:
      - current_player -> Player
      - state -> GameState
      - winner_symbol -> Optional[str]  # "X" or "O" when somebody wins
      - board -> Board
      - apply_move(row, col) -> None    # raises if invalid or game over
      - legal_moves() -> list[(r,c)]
      - reset() -> None                 # reset board & state, X always starts
    """
    WIN_LINES: List[List[Tuple[int,int]]] = [
        # Rows
        [(0,0),(0,1),(0,2)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(2,1),(2,2)],
        # Cols
        [(0,0),(1,0),(2,0)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)],
        # Diagonals
        [(0,0),(1,1),(2,2)],
        [(0,2),(1,1),(2,0)],
    ]

    def __init__(self, player_x: Player, player_o: Player, board: Optional[Board] = None) -> None:
        if player_x.symbol != "X" or player_o.symbol != "O":
            raise ValueError("Players must be created with symbols 'X' and 'O' respectively.")
        self._board = board if board is not None else Board()
        self._players = (player_x, player_o)
        self._turn_idx = 0  # X starts
        self._state = GameState.IN_PROGRESS
        self._winner_symbol: Optional[str] = None

    # --- properties ---
    @property
    def board(self) -> Board:
        return self._board

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def winner_symbol(self) -> Optional[str]:
        return self._winner_symbol

    @property
    def current_player(self) -> Player:
        return self._players[self._turn_idx]

    # --- public control methods ---
    def apply_move(self, row: int, col: int) -> None:
        """Apply move for the current player. Raises if game is over or move invalid."""
        if self._state is not GameState.IN_PROGRESS:
            raise RuntimeError("Game is over. Reset to play again.")

        self.current_player.make_move(self._board, row, col)
        self._update_state_after_move()
        if self._state is GameState.IN_PROGRESS:
            self._swap_turn()

    def legal_moves(self):
        return self._board.available_moves()

    def reset(self) -> None:
        self._board.reset()
        self._turn_idx = 0
        self._state = GameState.IN_PROGRESS
        self._winner_symbol = None

    # --- internal helpers ---
    def _swap_turn(self) -> None:
        self._turn_idx ^= 1  # toggle 0<->1

    def _update_state_after_move(self) -> None:
        winner = self._find_winner_symbol()
        if winner is not None:
            self._state = GameState.WIN
            self._winner_symbol = winner
            return
        if self._board.is_full():
            self._state = GameState.DRAW

    def _find_winner_symbol(self) -> Optional[str]:
        grid = [[self._cell_symbol(r, c) for c in range(Board.SIZE)] for r in range(Board.SIZE)]
        for line in self.WIN_LINES:
            a, b, c = line
            s1 = grid[a[0]][a[1]]
            s2 = grid[b[0]][b[1]]
            s3 = grid[c[0]][c[1]]
            if s1 is not None and s1 == s2 == s3:
                return s1
        return None

    def _cell_symbol(self, r: int, c: int) -> Optional[str]:
        # Board stores None/"X"/"O"; read-only access
        return self._board._grid[r][c]  # intentional internal read; no mutation here
