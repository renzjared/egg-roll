# egg-roll
[![Issues](https://img.shields.io/github/issues/renzjared/egg-roll)](https://github.com/renzjared/egg-roll/issues)
[![License](https://img.shields.io/github/license/renzjared/egg-roll)](https://github.com/renzjared/egg-roll/blob/master/LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/renzjared/egg-roll/badge)](https://www.codefactor.io/repository/github/renzjared/egg-roll)
![Static Badge](https://img.shields.io/badge/Unibersidad_ng-Pilipinas-maroon)

A simple terminal-based game developed in Python for the course CS 11, University of the Philippines Diliman.

<h2>Game Description</h2>
Egg Roll is a 2D puzzle game where players tilt a grid to guide eggs into their nests. Navigate through walls, avoid frying pans, and use strategic moves to score points. Each level presents a unique challenge with a limited number of moves. The goal of the player is to score the most points.<br/> 
<br/>

This implementation of **Egg Roll** includes bonus features, which are marked in this `README.md` file with **`[Bonus]`**.

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

 * **$`10\ Points`$** is awarded for each egg that manages to reach an empty nest.
    * `BONUS` points equivalent to the number of remaining moves (including the current move) is also added to the moves earned.
    * Mathematically, this is equivalent to $10 + (Max\ moves - Number\ of\ moves\ performed)$ points.
 * **$`5\ Points`$** is deducted for each egg that lands on a frying pan.<br>

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
 
**IMPORTANT: The path above is a placeholder. Do replace it with your actual path to the directory.**<br/>

*You may now proceed to the following step (Loading a Level)*

<h2>How to Play</h2>
<h3>Loading a Level</h3>

To load a level, use the following terminal command:
```sh
python3.12 egg_roll_basic.py [filename]
```
or (with Bonus features)
```sh
python3.12 egg_roll.py [filename]
```
Make sure that the level file is located in the same directory as the Python file.<br/>

**Example**<br/>

To load `level1.in`, run:

```sh
python3.12 egg_roll_basic.py level1.in
```
or (with Bonus features)
```sh
python3.12 egg_roll.py level1.in
```

* **[Bonus]**: In the implementation of the game with **Bonus Features**, specifying a level filename argument is optional as doing so will simply open the game's main menu.

<h3>Game Controls</h3>

The grid can be controlled (tilted) by inputting characters in the terminal when prompted.

The player can tilt the grid forward, backward, to the left, or to the right. Each tilt constitutes as a move. When prompted for an input, the player must enter moves either one at a time or several in sequence. The list of valid moves are:<br/>

 * `l` or `L`: Tilt the grid to the left.
 * `r` or `R`: Tilt the grid to the right.
 * `f` or `F`: Tilt the grid forwards (away from you).
 * `b` or `B`: Tilt the grid backwards (towards you).

Invalid moves are simply ignored by the program.<br/>

**[Bonus]** Players also have the option to undo their previous move.<br/>

 * `u` or `U`: Undo the previous move.

<h3>[Bonus] Game Commands</h3>
Players may also enter these commands at any point of the game.<br/>

 * `RESTART` - Restarts the current game level. All progress in the current level will be reset, allowing players to start over.
 * `RETURN` - Exits the current game session and returns the player to the main menu.
 * `TERMINATE` - Ends the current game session and closes the game.

<h2>How the Game Works</h2>
This Egg Roll game is specifically designed to be modular and easy to understand. It consists of six (6) Python scripts (plus an additional script for tests). This also makes testing easier.<br>

<h3>Key Files</h3>

 * `egg_roll_basic.py` - The main entry point of the game. This is the script that is launched by the user to start the game. It initializes the game, processes user inputs, updates the game state, and displays the results.<br/>
 * **[Bonus]** `egg_roll.py` - Same as the above, but contains bonus feature implementations of the game (see **Bonus Points** section below).<br/>
 * `game_utils.py` - Provides core game functionalities and algorithms, including functions for moving eggs, calculating egg positions, and checking game conditions.<br/>
 * **[Bonus]** `terminal_utils.py` - Contains utility functions for handling terminal operations such as creating formattable tables, getting terminal dimensions, and text formatting.<br/>
 * **[Bonus]** `main_menu.py` - Manages the main menu screen, including the options displayed and handling user selections.<br/>
 * **[Bonus]** `leaderboard_utils.py` - Contains utility functions for reading and updating the leaderboards.<br/>

<h3>Game Flow</h3>

 `1.` **Initialization**<br/>
 The game starts when `egg_roll_basic.py` or `egg_roll.py` is called by the user-player. This script first checks if there is a level filename argument thtat is passed by the player.<br/>
 * If a level filename argument (such as `level1.in`) is provided by the user, the level is read by the function `read_level()` and launched.
 * If no level filename argument is provided:
   * [Basic]: An error message is displayed, prompting the player to enter a valid level filename argument. 
   * **[Bonus]**: The main menu is displayed. From the main menu, the player can then launch a level by providing a level filename (or number) to play that particular level.

 `2.` **Main Game Loop**<br/> 
 The main game loop is handled by the `main` function of `egg_roll_basic.py` (or `egg_roll.py`) Once the player has identified a level to play, the initial state of the level grid is displayed and the game loop begins. The game loop continues as long as there are eggs left in the grid **AND** there are still moves to be made.
 * At each loop, the game presents the current state of the level grid and prompts the player for moves.
 * `validate_moves()` is a function that sanitizes the player's input and removes excess moves. It removes excess and invalid characters (such as emojis and numbers).
 * The `roll(grid, moves, max_moves)` function then processes each move *individually*, updates the grid and calculates the points gained or lost.

 `3.` **End of the Game**<br/>
 * When the maximum number of moves is reached by the player **OR** there are no more eggs to move, `display_final_state()` is run and the final game statistics is presented to the player.
 * [Basic]: The game terminates immediately after displaying the final game statistics.
 * **[Bonus]**: The player is then given the option to play again, return to the main menu, or exit the game.

<h2>Running Tests</h2>

**This implementation of **Egg Roll** uses [`unittest`](https://docs.python.org/3/library/unittest.html) for running tests.<br/>**

To run the tests, simply execute the following command in the project directory:
```bash
python3.12 test_egg_roll.py
```
This command will run all the test cases defined in `test_egg_roll.py`. The `test_egg_roll.py` file contains unit tests for **Egg Roll**. These tests ensure that the various functions and components of the game work correctly and as intended.
* In case of failures, `unittest` will display the count of discovered failed cases, as well as details about the individual errors.

<h3>Setup</h3>

**setUpClass()**<br/>

* _A class method called before tests in an individual class are run. `setUpClass` is called with the class as the only argument and must be decorated as a classmethod()_ [[Documentation]](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUpClass) <br/>
* This method initializes the various grid configurations to be tested. This ensures that each test starts with a consistent state, which is especially important for functions like `roll()` and `apply_move()`, which alter the state of the grid they are used on.

**setUp()**<br/>
* _Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure._
* `deepcopy` is used to create fresh copies of the grids before each test. This ensures that modifications in one test do not affect others.

<h3>Thoroughness</h3>
* The `test_egg_roll.py` file is structured in a way such that each method within it corresponds to a function to be tested.
* Each function test in the test function is designed to be independent of each other, meaning that the failure of one function does not affect the other tests.
* Each function test covers basic cases as well as edge cases.

**Edge Cases**
* The unit tests defined in `test_egg_roll.py` are meant to cover a wide variety of scenarios, accounting for user errors, invalid inputs, and other edge cases.
* These tests account for cases such as 'invalid' game levels (in terms of game design), various collision mechanics (egg-to-egg, egg-to-wall, etc..), as well as irregular and invalid user inputs (such as very large number of input moves).
* Exponentiation is used to express large values of numbers. This is used in instances wherein it may be beneficial to test a particularly large volume of input.
   * **Example 1:** In `test_validate_moves`, some input strings are multiplied to an exponentiated number in order to process a string with a very large number of characters.
   * **Example 2:** In `test_find_eggs`, a grid with nothing but $2^15$ eggs was created. This ensures that `find_eggs` is able to find eggs even for grids (game levels) of bigger proportions.
* Unconventional cases are also tested to ensure that they are handled properly, even if their occurence is unrealistic. This includes:
   * A negative number of moves performed
   * Moving an egg that is way outside of the grid's bounds
   * Ensuring that characters unused by the game, such as `A` and `🍅` do not make it into the game somehow

**Parametrization**
* Some tests are parametrized to improve code readability and reduce the need for repetitive lines of tests.\
* An example of this is the `test_calculate_points` method, which compiles the test cases as a list of tuples (`test_cases`) containing the parameters (`max_moves`, `moves`, `intended_result`).

**Random Testing**
* Random testing is used to ensure the reliability of the functions used in **Egg Roll**. It ensures comprehensive coverage and are intended to cover unpredictable scenarios.
* For example, as is used in the `test_calculate_points` method, random moves are generated in order to simulate a wide range of possible user interactions. This ensures that the game can handle various scenarios gracefully.

<h3>Adding New Tests</h3>

New tests can be added to `test_egg_roll.py` by doing the following:

`1.` **Definine a New Test Method**<br/>
* Edit the `test_egg_roll.py` script using any text editor (such as **Sublime Text**) and write the new test methods.
* For organization of code and convenience, it is encouraged that separate methods be written for tests that cover different scopes (example: testing the validation of user input and testing the points system).
* IMPORTANT: The method name should begin with `test_` in order to be recognized by `unittest`. (Example: `test_roll`)

`2.` **Use Assertions**<br/>
* Assertions such as `assertEqual`, `assertTrue`, and `assertFalse` may be added inside the method to check the correctness and validity of the outputs.
* Existing assertions in the `test_egg_roll.py` may be edited and templated for this purpose.
* Please refer to the [official unittest documentation](https://docs.python.org/3/library/unittest.html) for more information.

`3.` **Run the Tests**<br/>
* The newly-added tests can be similarly run by executing the following command in the project directory:
```sh
python3.12 test_egg_roll.py
```

_Note:_ A separate `.py` file may also be created for the additional test cases. Simply do the steps above and run the new `.py` file instead of `test_egg_roll.py`.
```sh
python3.12 new_test_script.py
```

<h2>Bonus Points</h2>

 * **Bonus Level Submissions**<br/>
   `1.` **cs11.in** <br/>
   Try not to _drop_! (the eggs)<br/>
   
   `2.` **labyrinth.in** <br/>
   Navigate, dodge, and don't get lost!<br/>
   
   `3.` **sacrifice.in** <br/>
   _"...He who would attain highly must sacrifice greatly."_ - James Allen<br/>

 * **Main Menu**
    * The game launches on the main menu screen if no filename argument is provided by the player.
    * From the main menu, the player can (1) start the game, (2) read game instructions, (3) change language, (4) see game credits, and (5) terminate the game session.
 * **Level Selector**
    * Upon selecting option `1` (Start Game) from the main menu, the level selector will be displayed.
    * In the main menu, the player is presented with a numbered table of game levels showing the level name, size (`rows` × `columns`), and maximum moves allowed.
    * The player can play a level by (any of the following): entering the number of the level or entering the name of the level
 * **Persistent Game Leaderboard**
    * The player will be asked for their name after playing a game level. If their score is high enough, their score will be recorded in the leaderboard for that particular level.
    * The Top 10 scores of each game level is stored in a JSON file. This allows for a persistent leaderboard, meaning that the high scores are still available for the next time the game is run.
 * **A Fancier User Interface**
    * The display interface of the game levels itself was also improved. For instance, the name of the game level is displayed on the header row. Horizontal dividers also separate different sections of the game screen.
    * A separate function for creating tables (`terminal_utils/create_table`) was also developed to facilitate the creation of dynamic terminal-based tables.
 * **Formatted Text Displays**
    * Text coloring and styling is applied on various menus of the game using the [`termcolor`](https://github.com/termcolor/termcolor) library.
    * Some texts are also centered horizontally to enhance formatting and readability (makes use of terminal dimensions).
 * **Restart, Return, and Terminate Commands**
    * Players may enter these commands at any point of the game.
    * `RESTART` or `UMULIT` - Restarts the current game level. All progress in the current level will be reset, allowing players to start over.
    * `RETURN` or `BUMALIK` - Exits the current game session and returns the player to the main menu.
    * `TERMINATE` or `ISARA` - Ends the current game session and closes the game.
 * **Replayable Levels**
    * At the end of each level (when a player runs out of moves or eggs to move), an option to replay the level is presented.
    * Replaying the level restarts the current game level, allowing the player to start over.
 * **Ability to Undo Moves**
    * Aside from the four (4) directional moves, the player can also choose to undo a move when prompted for an input by entering `u` or `U`.
    * By repeatedly entering `u` or `U`, the player can undo all performed moves.
 * **Tagalog Localization**
    * Egg-roll is now available in Filipino (Tagalog)!
    * The game language can be switched from English to Tagalog (and vice-versa) by selecting option `3` from the main menu.
