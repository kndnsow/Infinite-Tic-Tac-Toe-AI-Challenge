# Infinite Tic Tac Toe - AI Challenge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Optional license badge -->

A visually enhanced game of Tic Tac Toe with a twist and a formidable AI opponent! This isn't your standard 3-in-a-row; the "infinite" rule adds a layer of complexity where your oldest piece disappears after you've placed three. Can you outsmart the AI?

![Screenshot]

## Features

*   **Classic Tic Tac Toe Goal:** Be the first to get three of your marks (X or O) in a row, column, or diagonal.
*   **Infinite Rule:** Once a player has 3 marks on the board, placing their 4th mark will cause their *oldest* existing mark to be removed. This keeps the board dynamic!
*   **Challenging AI:** Play against a bot using the Minimax algorithm (with adjustable search depth) to provide a tough opponent.
*   **Visual Enhancements:** Custom color scheme and clean UI built with Tkinter.
*   **Removal Highlighting:** The piece that is next in line to be removed (if you place another piece) is highlighted with a distinct background color.
*   **Score Tracking:** Keeps track of wins between the Human and the Bot across rounds.
*   **Auto-Restart:** The game automatically restarts shortly after a win, loss, or draw.

## Technology

*   **Python 3**
*   **Tkinter** (Python's standard GUI library - usually built-in)

## How to Play

1.  **Objective:** Get 3 of your marks (you'll be assigned X or O) in a line.
2.  **Gameplay:** Click on an empty square to place your mark.
3.  **The Infinite Rule:** Pay attention! After you have 3 marks down, your *next* move will place your 4th mark AND remove your 1st mark. The highlighted piece (with the darker background) shows which one will disappear next.
4.  **Turns:** The game alternates turns between you and the AI bot. The status bar indicates whose turn it is.

## Running the Game

There are two ways to play:

**1. Running from Source:**
   *   Ensure you have Python 3 installed.
   *   Clone this repository or download the source code.
   *   Rename the main script file if you chose a different name (e.g., `infinite_tictactoe_ai.py`).
   *   Make sure the `icon.ico` file is in the same directory as the script.
   *   Run the script from your terminal:
     ```bash
     python infinite_tictactoe_ai.py
     ```
   *   *(Tkinter is typically included with standard Python installations. No external libraries are needed.)*

**2. Using the Executable:**
   *   Download the pre-compiled executable file (`infinite_tictactoe_ai.exe` or similar) from the `dist/` directory (if provided in the release/repository).
   *   Ensure the `icon.ico` file is included alongside the `.exe` in the `dist/` directory if it wasn't bundled correctly (the provided PyInstaller command *should* bundle it).
   *   Double-click the `.exe` file to run the game directly on Windows.

## The Challenge!

Think you've mastered Tic Tac Toe? Think again! The AI opponent in this version uses a strong Minimax search algorithm, making it incredibly difficult to defeat, especially with the added complexity of the infinite rule.

*   **Can you find a winning strategy?**
*   **Can you even force a draw consistently?**

Test your strategic thinking and see if you can beat the bot!

## Building from Source (Optional)

If you want to create the `.exe` file yourself:

1.  Install PyInstaller: `pip install pyinstaller`
2.  Make sure `icon.ico` is in the same directory as your `.py` script.
3.  Run the following command in your terminal from that directory (replace `infinite_tictactoe_ai.py` if you used a different name):
    ```bash
    pyinstaller --onefile --add-data "icon.ico;." --windowed --icon=icon.ico infinite_tictactoe_ai.py
    ```
4.  The executable will be created in the `dist` sub-directory.

## Contributing

Contributions, bug reports, and feature suggestions are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details (optional - consider adding a LICENSE file).
