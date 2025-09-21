# board.py
from typing import List, Optional, Tuple

class Board:
    """
    3x3 Tic Tac Toe board.
    Public API (for now):
      - place_mark(row, col, symbol)
      - is_cell_empty(row, col)
      - available_moves()
      - is_full()
      - reset()
      - __str__()  # pretty print
    Notes:
      - row, col are 0-based (0..2)
      - symbol must be "X" or "O"
    """
    SIZE = 3
    VALID_SYMBOLS = {"X", "O"}

    def __init__(self) -> None:
        self._grid: List[List[Optional[str]]] = [[None]*self.SIZE for _ in range(self.SIZE)]

    def reset(self) -> None:
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                self._grid[r][c] = None

    def is_cell_empty(self, row: int, col: int) -> bool:
        self._validate_coords(row, col)
        return self._grid[row][col] is None

    def place_mark(self, row: int, col: int, symbol: str) -> None:
        """Place 'X' or 'O' at (row, col). Raises ValueError for bad input."""
        self._validate_coords(row, col)
        self._validate_symbol(symbol)
        if not self.is_cell_empty(row, col):
            raise ValueError(f"Cell ({row},{col}) is already occupied.")
        self._grid[row][col] = symbol

    def available_moves(self) -> List[Tuple[int, int]]:
        """List of (row, col) for all empty cells."""
        moves = []
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self._grid[r][c] is None:
                    moves.append((r, c))
        return moves

    def is_full(self) -> bool:
        return all(self._grid[r][c] is not None for r in range(self.SIZE) for c in range(self.SIZE))

    def __str__(self) -> str:
        """Human-friendly board printout."""
        rows = []
        for r in range(self.SIZE):
            symbols = [(self._grid[r][c] or " ") for c in range(self.SIZE)]
            rows.append(" " + " | ".join(symbols) + " ")
        sep = "\n---+---+---\n"
        return sep.join(rows)

    # --- internal validation helpers ---
    def _validate_coords(self, row: int, col: int) -> None:
        if not (0 <= row < self.SIZE and 0 <= col < self.SIZE):
            raise ValueError(f"Row/Col out of range (got {row},{col}). Use 0..2.")

    def _validate_symbol(self, symbol: str) -> None:
        if symbol not in self.VALID_SYMBOLS:
            raise ValueError(f"Invalid symbol '{symbol}'. Use 'X' or 'O'.")
