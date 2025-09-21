"""Tic-tac-toe game implementation with board management."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Board:
    """Represent a tic-tac-toe board and manage cell state."""

    size: int = 3
    grid: List[List[str]] = field(default_factory=lambda: [[" " for _ in range(3)] for _ in range(3)])

    def display(self) -> str:
        """Return a string representation of the current board."""
        rows = [" | ".join(row) for row in self.grid]
        return "\n".join(rows)

    def place_mark(self, row: int, col: int, symbol: str) -> bool:
        """Place a player's symbol on the board if the move is valid."""
        if symbol not in {"X", "O"}:
            raise ValueError("Symbol must be 'X' or 'O'.")
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError("Row and column must be within the board boundaries.")
        if self.grid[row][col] != " ":
            return False
        self.grid[row][col] = symbol
        return True

    def is_full(self) -> bool:
        """Return True if the board has no empty spaces left."""
        return all(cell != " " for row in self.grid for cell in row)

    def reset(self) -> None:
        """Clear the board so a new game can start."""
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c] = " "

@dataclass
class Player:
    """Represent a tic-tac-toe player with a name and symbol."""

    name: str
    symbol: str

    def __post_init__(self) -> None:
        """Validate that the player's symbol is valid."""
        if self.symbol not in {"X", "O"}:
            raise ValueError("Player symbol must be either 'X' or 'O'.")

    def make_move(self, board: Board, row: int, col: int) -> bool:
        """Attempt to place the player's symbol on the board."""
        try:
            return board.place_mark(row, col, self.symbol)
        except (IndexError, ValueError):
            return False

@dataclass
class GameEngine:
    """Coordinate the overall tic-tac-toe gameplay between two players."""

    player_one: Player
    player_two: Player
    board: Board = field(default_factory=Board)
    current_index: int = 0
    winner: Player | None = None
    is_draw: bool = False

    @property
    def current_player(self) -> Player:
        """Return the player whose turn it currently is."""
        return (self.player_one, self.player_two)[self.current_index]

    def play_turn(self, row: int, col: int) -> bool:
        """Process a move for the current player and evaluate game state."""
        if self.winner or self.is_draw:
            return False
        if not self.current_player.make_move(self.board, row, col):
            return False
        if self._check_winner(self.current_player.symbol):
            self.winner = self.current_player
            return True
        if self.board.is_full():
            self.is_draw = True
            return True
        self._swap_turn()
        return True

    def _swap_turn(self) -> None:
        """Toggle the current player index."""
        self.current_index = 1 - self.current_index

    def _check_winner(self, symbol: str) -> bool:
        """Return True if the given symbol has three in a row."""
        lines = []
        lines.extend(self.board.grid)
        lines.extend([[self.board.grid[r][c] for r in range(self.board.size)] for c in range(self.board.size)])
        lines.append([self.board.grid[i][i] for i in range(self.board.size)])
        lines.append([self.board.grid[i][self.board.size - 1 - i] for i in range(self.board.size)])
        return any(all(cell == symbol for cell in line) for line in lines)

@dataclass
class ComputerPlayer(Player):
    """Automated player that chooses moves randomly from available cells."""

    def choose_move(self, board: Board) -> tuple[int, int]:
        """Pick a free cell at random and return its coordinates."""
        import random
        available = [
            (row, col)
            for row in range(board.size)
            for col in range(board.size)
            if board.grid[row][col] == " "
        ]
        if not available:
            raise RuntimeError("No moves available for the computer player.")
        return random.choice(available)


class ConsoleGame:
    """Run a tic-tac-toe match in the console using a game engine."""

    def __init__(self, engine: GameEngine) -> None:
        self.engine = engine

    def run(self) -> None:
        """Run the interactive game loop until a win or draw occurs."""
        print("Starting tic-tac-toe! Enter moves as 'row col' (1-based indices).\n")
        while not self.engine.winner and not self.engine.is_draw:
            self._print_board()
            player = self.engine.current_player
            row, col = self._select_move(player)
            if not self.engine.play_turn(row, col):
                print("Invalid move. Try again.\n")
                continue
        self._print_board()
        self._announce_result()

    def _select_move(self, player: Player) -> tuple[int, int]:
        """Return the coordinates for the current player's move."""
        if isinstance(player, ComputerPlayer):
            row, col = player.choose_move(self.engine.board)
            print(f"{player.name} (computer) chose: {row + 1} {col + 1}\n")
            return row, col
        return self._prompt_for_move(player)

    def _prompt_for_move(self, player: Player) -> tuple[int, int]:
        """Prompt the human player for a move and return zero-based coordinates."""
        while True:
            raw = input(f"{player.name}'s turn ({player.symbol}). Enter row and column: ").strip()
            parts = raw.split()
            if len(parts) != 2:
                print("Please enter exactly two numbers separated by space (e.g., '1 3').")
                continue
            try:
                row_input, col_input = (int(part) for part in parts)
            except ValueError:
                print("Only numeric input is accepted. Please try again.")
                continue
            row, col = row_input - 1, col_input - 1
            if not (0 <= row < self.engine.board.size and 0 <= col < self.engine.board.size):
                print("Coordinates must be between 1 and 3. Please try again.")
                continue
            return row, col

    def _print_board(self) -> None:
        """Display the current board in the console."""
        print("Current board:")
        print(self.engine.board.display())
        print()

    def _announce_result(self) -> None:
        """Output the final game result."""
        if self.engine.winner:
            print(f"{self.engine.winner.name} wins with symbol {self.engine.winner.symbol}!")
        elif self.engine.is_draw:
            print("The game is a draw.")


def create_console_game(player_one_name: str, player_two_name: str | None = None, vs_computer: bool = False) -> ConsoleGame:
    """Create a configured console game with human or computer opponents."""
    player_one = Player(name=player_one_name, symbol="X")
    if vs_computer:
        player_two = ComputerPlayer(name=player_two_name or "Computer", symbol="O")
    else:
        if player_two_name is None:
            raise ValueError("Second player name required when not playing against the computer.")
        player_two = Player(name=player_two_name, symbol="O")
    engine = GameEngine(player_one=player_one, player_two=player_two)
    return ConsoleGame(engine)


if __name__ == "__main__":
    game = create_console_game("Player 1", vs_computer=True)
    game.run()
