# Checkers Game Engine

This is a command-line Checkers game engine written in Python, allowing a human player to compete against the computer. It implements the core rules of American Checkers, including mandatory captures and multi-jumps.


## 1. Game Description

This project provides a functional Checkers game where a human player (controlling WHITE pieces) can play against a computer opponent (controlling BLACK pieces). The computer's "intelligence" is limited to choosing a random valid move from all available options. The game runs in your terminal, displaying the board using text characters.

## 2. Features

Human vs. Computer: Play against a basic AI.

### Core Checkers Rules:

* Standard pawn movement (forward diagonals only).

* King movement (all four diagonal directions).

* Mandatory Captures: If a capture is available, it must be taken.

* Mandatory Multi-Jumps: If a piece can make multiple consecutive jumps, it must continue until no further jumps are possible.

* Pawn promotion to King upon reaching the opponent's home.

### Game End Conditions: 
Detects win/loss by piece count or by a player having no legal moves.

## 3. How to Run
To get the game running on your local machine, follow these steps:

* Save the Code: Copy the entire Python code from the checkers_simplified_code Canvas.

* Create a File: Paste the copied code into a new text file.

* Save as Python File: Save this file with a .py extension (e.g., checkers_game.py). Choose a location on your computer that's easy to access (e.g., your Desktop or a dedicated games folder).

* Open a Terminal/Command Prompt:

    * Windows: Search for "cmd" or "PowerShell" in your Start menu.

    * macOS: Open "Terminal" from Applications > Utilities.

    * Linux: Open your preferred terminal emulator.

* Navigate to the Directory: Use the cd command to go to the folder where you saved checkers_game.py.

    * Example: cd C:\Users\YourUser\Desktop (Windows)

    * Example: cd ~/Desktop/my_games (macOS/Linux)

* Run the Game: Execute the script using the Python interpreter:

    python checkers_game.py

    (If python doesn't work, try python3 instead: python3 checkers_game.py)

The game will start in your terminal.

## 4. How to Play
* Players control the WHITE (WP/WK) pieces. The computer controls the BLACK (BP/BK) pieces.

* Turns: Computer moves first, then turns alternate.

* Board Display: The board is displayed with rows labeled A through H and columns labeled 0 through 7.

    * __: Empty square

    * WP: White Pawn

    * WK: White King

    * BP: Black Pawn

    * BK: Black King

* Making a Move:

    * When it's your turn, the game will prompt you to "Enter your move:".

    * Input your move using the format: StartRowCol->EndRowCol

    * Example: To move a piece from row F, column 0 to row E, column 1, you would type: F0->E1

    * The row character can be uppercase or lowercase.

## 5. Board Notation
The board is displayed as an 8x8 grid:

   0  1  2  3  4  5  6  7
  -----------------------
A|BP __ BP __ BP __ BP __
B|__ BP __ BP __ BP __ BP
C|BP __ BP __ BP __ BP __
D|__ __ __ __ __ __ __ __
E|__ __ __ __ __ __ __ __
F|WP __ WP __ WP __ WP __
G|__ WP __ WP __ WP __ WP
H|WP __ WP __ WP __ WP __
  -----------------------

* Rows: A (top) to H (bottom)

* Columns: 0 (left) to 7 (right)

## 6. Future Enhancements
This game provides a solid foundation. Here are some ideas for future improvements:

* Improved AI:

    * Replace the random AI with a Minimax algorithm (like the one in the previous version) to make the computer a more challenging opponent.

    * Add Alpha-Beta Pruning to the Minimax for better performance.

    * Implement an evaluation function to guide the Minimax search.

* Full Draw Rules: Add detection for draws due to:

    * Threefold repetition of board positions.

    * A certain number of moves without a capture or pawn promotion (e.g., 40-move rule).

* Undo/Redo Moves: Allow players to revert or re-apply moves.

* Move History: Display a log of all moves made during the game.
  
* Setting a time limit to input the valid move
