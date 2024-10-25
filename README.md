# egg-roll
A simple terminal-based game developed in Python for the course CS 11, University of the Philippines Diliman.

<h2>Game Description</h2>
Egg Roll is a 2D puzzle game where players tilt a grid to guide eggs into their nests. Navigate through walls, avoid frying pans, and use strategic moves to score points. Each level presents a unique challenge with a limited number of moves. The goal of the player is to score the most points.

<h3>Blocks</h3>
Throughout gameplay, players will encounter the following blocks:<br/>

 * 🧱 **Wall**<br/>
 * 🥚 **Egg**<br/>
 * 🟩 **Grass**<br/>
 * 🪹 **Empty nest**<br/>
 * 🪺 **Full nest**<br/>
 * 🍳 **Frying pan**<br/>


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

<h2>How it Works</h2>
*To be updated*

<h2>Bonus Points</h2>
We have included the following bonus features:  
*To be updated*
