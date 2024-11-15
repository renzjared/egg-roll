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

 * 🧱 **Wall** - A solid barrier that cannot be passed through.<br/>
 * 🥚 **Egg** - The primary object to be moved. Players must roll the eggs to their destination while avoiding frying pans and other obstacles.<br/>
 * 🟩 **Grass** - Open and traversable space where eggs can roll freely.<br/>
 * 🪹 **Empty nest** - When an egg reaches an empty nest, it fills the nest, converting it to a full nest, and points are awarded.<br/>
 * 🪺 **Full nest** - Indicates a successfully filled nest. This also acts as a solid barrier.<br/>
 * 🍳 **Frying pan** - A hazardous block that fries any egg that lands on it, causing a point deduction.<br/>


<h2>How to Play</h2>
<h3>Loading a Level</h3>

To load a level, call: `python3.12 egg_roll.py [filename]`.
Make sure that the level file is located in the same directory as the Python file.

<h3>Game Controls</h3>
The player can tilt the grid forward, backward, to the left, or to the right. Each tilt constitutes as a move. When prompted for an input, the player must enter moves either one at a time or several in sequence. The list of valid moves are:<br/>

 * `l` or `L`: Tilt the grid to the left.<br/>
 * `r` or `R`: Tilt the grid to the right.<br/>
 * `f` or `F`: Tilt the grid forwards (away from you).<br/>
 * `b` or `B`: Tilt the grid backwards (towards you).<br/>

**Sample**<br/>
Correct: `l`<br/>
Correct: `lblf`<br/>
Wrong: `n`<br/>
<br/>
 Invalid moves are simply ignored by the program.<br/>

<h3>Game Commands</h3>
Players may also enter these commands at any point of the game.<br/>

 * `RESTART` - Restarts the current game level. All progress in the current level will be reset, allowing players to start over.<br/>
 * `RETURN` - Exits the current game session and returns the player to the main menu.<br/>
 * `TERMINATE` - Ends the current game session and closes the game.<br/>

<h2>How it Works</h2>
*To be updated*

<h2>Bonus Points</h2>
We have included the following bonus features:<br/>
 * **A Main Menu**
 * **Restart. Return, and Terminate Commands**
 * **Formatted Text Displays**
*To be updated*