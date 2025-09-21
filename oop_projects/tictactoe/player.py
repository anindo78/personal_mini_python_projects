# player.py
from typing import Final
from board import Board

class Player:
    """
    Simple Tic Tac Toe player.
    - name: display name (e.g., "Alice")
    - symbol: "X" or "O"
    Public API:
      - make_move(board, row, col) -> None  # places this player's symbol
    """
    def __init__(self, name: str, symbol: str) -> None:
        symbol = symbol.upper().strip()
        if symbol not in Board.VALID_SYMBOLS:
            raise ValueError(f"Invalid symbol '{symbol}'. Use one of {Board.VALID_SYMBOLS}.")
        self._name: Final[str] = name
        self._symbol: Final[str] = symbol

    @property
    def name(self) -> str:
        return self._name

    @property
    def symbol(self) -> str:
        return self._symbol

    def make_move(self, board: Board, row: int, col: int) -> None:
        """
        Attempts to place this player's symbol at (row, col).
        Raises ValueError if the move is invalid (board enforces rules).
        """
        board.place_mark(row, col, self._symbol)

    def __repr__(self) -> str:
        return f"Player(name={self._name!r}, symbol={self._symbol!r})"
