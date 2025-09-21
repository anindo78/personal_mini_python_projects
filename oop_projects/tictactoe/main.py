# main.py
from typing import Tuple
from board import Board
from player import Player
from game import Game, GameState

def parse_move(raw: str) -> Tuple[int, int]:
    """
    Accepts inputs like:
      - "1 3" (row col, 1-based)
      - "0,2" (row,col, 0-based)
      - "2, 2" or "2 2"
    Returns (row, col) as 0-based ints.
    Raises ValueError on bad format.
    """
    raw = raw.strip().replace(",", " ")
    parts = [p for p in raw.split() if p]
    if len(parts) != 2:
        raise ValueError("Please enter two numbers (row col).")
    r, c = int(parts[0]), int(parts[1])

    # Support both 1-based and 0-based: if values are 1..3, convert to 0..2
    if r in (1, 2, 3) and c in (1, 2, 3):
        r -= 1
        c -= 1

    if not (0 <= r <= 2 and 0 <= c <= 2):
        raise ValueError("Row/Col must be in 0..2 (or 1..3).")
    return r, c

def print_board_with_coords(board: Board) -> None:
    """Show the board plus a tiny coordinate guide."""
    print("\nCurrent board:")
    print(board)
    print("\nCoordinates: rows/cols can be 0..2 or 1..3")
    print("  (row col) e.g., 0 2  or  1 3")

def play_once() -> None:
    px = Player(input("Enter Player X name: ").strip() or "Player X", "X")
    po = Player(input("Enter Player O name: ").strip() or "Player O", "O")
    game = Game(px, po)

    while game.state is GameState.IN_PROGRESS:
        print_board_with_coords(game.board)
        player = game.current_player
        raw = input(f"\n{player.name}'s turn ({player.symbol}). Enter row and column: ")
        try:
            r, c = parse_move(raw)
            game.apply_move(r, c)
        except Exception as e:
            print(f"❌ {e}")
            continue  # retry same player

    # Game over
    print_board_with_coords(game.board)
    if game.state is GameState.WIN:
        print(f"\n🎉 {game.winner_symbol} wins! "
              f"({px.name if game.winner_symbol=='X' else po.name})")
    else:
        print("\n🤝 It's a draw!")

def main() -> None:
    print("=== Tic Tac Toe (Console) ===")
    while True:
        play_once()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
