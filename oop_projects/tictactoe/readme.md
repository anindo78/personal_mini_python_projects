🎯 ### Tasks
1. #### Game Board

Create a class to represent the board.

It should:

1. Store the current state (3×3 grid).

2. Print the grid in a clean format.

3. Allow placing a mark (X or O) at a valid position.

4. Reject invalid moves (e.g., if the cell is already filled or out of range).

---
2. #### Player

Create a class for players.

Each player should have:

1. A name (e.g., “Alice”)

2. A symbol (X or O)

3. The class should expose a method to make a move on the board.
---

3. #### Game Engine

Create a class to run the game.

It should:

1. Track whose turn it is.

2. Ask the current player for a move and update the board.

3. After each move, check for:

4. A win (three in a row)

5. A draw (board full, no winner)

6. Stop the game and announce the result when either occurs.
---

4. #### Play Loop

1. The game should run in the console.

Example flow:
'Current board:
X | O |  
  | X |  
  |   | O

Alice’s turn (X). Enter row and column: 2 2
'
2. Continue until there’s a winner or draw.
---
5. #### Bonus (Optional)

Add an option for Player vs Computer:

Computer randomly picks an available cell.

Add input validation (don’t crash if user types wrong input).
