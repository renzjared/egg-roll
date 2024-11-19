# egg-roll
[![Issues](https://img.shields.io/github/issues/renzjared/egg-roll)](https://github.com/renzjared/egg-roll/issues)
[![License](https://img.shields.io/github/license/renzjared/egg-roll)](https://github.com/renzjared/egg-roll/blob/master/LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/renzjared/egg-roll/badge)](https://www.codefactor.io/repository/github/renzjared/egg-roll)
![Static Badge](https://img.shields.io/badge/Unibersidad_ng-Pilipinas-maroon)

A simple terminal-based game developed in Python for the course CS 11, University of the Philippines Diliman.

<h2>Game Description</h2>
Egg Roll is a 2D puzzle game where players tilt a grid to guide eggs into their nests. Navigate through walls, avoid frying pans, and use strategic moves to score points. Each level presents a unique challenge with a limited number of moves. The goal of the player is to score the most points.

<h3>Blocks</h3>
Throughout gameplay, players will encounter the following blocks:<br/>

 * 🧱 **Wall** - A solid barrier that cannot be passed through.
 * 🥚 **Egg** - The primary object to be moved. Players must roll the eggs to their destination while avoiding frying pans and other obstacles.
 * 🟩 **Grass** - Open and traversable space where eggs can roll freely.
 * 🪹 **Empty nest** - When an egg reaches an empty nest, it fills the nest, converting it to a full nest, and points are awarded.
 * 🪺 **Full nest** - Indicates a successfully filled nest. This also acts as a solid barrier.
 * 🍳 **Frying pan** - A hazardous block that fries any egg that lands on it, causing a point deduction.

<h3>Earning Points</h3>
The primary objective of the player is to earn the most points possible.<br/>

 * **[+10 Points + BONUS]** For each egg that manages to reach an empty nest.<br>
 * The number of BONUS points earned is equivalent to the number of remaining moves (including the current move).<br>
   
 * **[-5 Points]** For each egg that lands on a frying pan.<br>

<h2>Downloading and Installing the Game</h2>
<h3>Prerequisites</h3>

 * Ensure that you have Python installed on your system. *Egg-roll* is compatible with Python 3.x versions. You can download Python from [python.org](https://www.python.org/).

<h3>Downloading the ZIP File</h3>

 `1.` On the right side of this repository, click the green "Code" button and select "Download ZIP."<br/>
 `2.` Extract the ZIP file once the download is complete.<br/>

<h3>Installation</h3>

 `1.` Open your terminal or command propmpt.<br/>
 `2.` Navigate to the directory where you extracted the downloaded ZIP file.<br/>

```sh
cd path/to/extracted/egg-roll
```
 
*You may now proceed to the following step (Loading a Level)*

<h2>How to Play</h2>
<h3>Loading a Level</h3>

To load a level, use the following terminal command: `python3.12 egg_roll.py [filename]`.
Make sure that the level file is located in the same directory as the Python file.<br/>

**Example**<br/>

To load `level1.in`, run:

```sh
python3.12 egg_roll.py level1.in
```

<h3>Game Controls</h3>

The grid can be controlled (tilted) by inputting characters in the terminal when prompted.

The player can tilt the grid forward, backward, to the left, or to the right. Each tilt constitutes as a move. When prompted for an input, the player must enter moves either one at a time or several in sequence. The list of valid moves are:<br/>

 * `l` or `L`: Tilt the grid to the left.
 * `r` or `R`: Tilt the grid to the right.
 * `f` or `F`: Tilt the grid forwards (away from you).
 * `b` or `B`: Tilt the grid backwards (towards you).

Players also have the option to undo their previous move.<br/>

 * `u` or `U`: Undo the previous move.

 Invalid moves are simply ignored by the program.<br/>

<h3>Game Commands</h3>
Players may also enter these commands at any point of the game.<br/>

 * `RESTART` - Restarts the current game level. All progress in the current level will be reset, allowing players to start over.
 * `RETURN` - Exits the current game session and returns the player to the main menu.
 * `TERMINATE` - Ends the current game session and closes the game.

<h2>How the Game Works</h2>
This Egg Roll game is specifically designed to be modular and easy to understand. It consists of four (4) Python scripts (plus an additional script for tests). This also makes testing easier.<br>

<h3>Key Files</h3>

 * `egg_roll.py` - The main entry point of the game. This is the script that is launched by the user to start the game. It initializes the game, processes user inputs, updates the game state, and displays the results.<br/>
 * `game_utils.py` - This script provides core game functionalities and algorithms, including functions for moving eggs, calculating egg positions, and checking game conditions.<br/>
 * `main_menu.py` - Manages the main menu screen, including the options displayed and handling user selections.<br/>
 * `terminal_utils.py` - Contains utility functions for handling terminal operations such as clearing the screen, getting terminal dimensions, and text formatting.<br>

<h3>Game Flow</h3>

 `1.` **Initialization**<br/>
 The game starts when `egg_roll.py` is called by the user-player. There are two possible scenarios.<br/>
 * If a level filename argument (such as `level1.in`) is provided by the user, the level is launched.
 * If no level filename argument is provided, the game launches the main menu.
   * From the main menu, the player can then launch a level by providing a level filename to play that particular level.

 `2.` **Main Game Loop**<br/>
 The game loop continues as long as there are eggs left in the grid **AND** there are still moves to be made.
 * At each loop, the game presents the current state of the level grid and prompts the player for moves.
 * `validate_moves(moveset, remaining_moves` sanitizes the player's input and removes excess moves.
 * The `roll(grid, moves, max_moves)` function then processes each move *individually*, updates the grid and calculates the points gained or lost.

 `3.` **End of the Game**<br/>
 * When the maximum number of moves is reached by the player **OR** there are no more eggs to move, the final state of the grid and final game statistics is presented to the player.
 * The player is then given the option to play again, return to the main menu, or exit the game.

<h2>Bonus Points</h2>
We have included the following bonus features:<br/>

 * **A Main Menu**
 * **A Fancier User Interface**
 * **Restart, Return, and Terminate Commands**
 * **Formatted Text Displays**
 * **Ability to Undo Moves**
*To be updated*
