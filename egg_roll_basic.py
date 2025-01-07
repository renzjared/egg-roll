"""
Copyright 2024 Renz Jared Rolle.

Licensed under the GNU General Public License, Version 3 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://github.com/renzjared/egg-roll/blob/main/LICENSE

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author Renz Jared Rolle <rgrolle@up.edu.ph>
"""

import copy
import os
import re
import subprocess
import sys
import time

from game_utils import Move, Grid
from leaderboard_utils import Leaderboard


def main(filename: str) -> None:
    """Main function to run Egg Roll.

    The function reads the level file, processes player moves,
    updates the game state, and displays the results until the maximum
    moves are reached or when there are no more eggs to roll.

    Args:
        filename (str): The path to the file containing the game level.
    """
    # Read game level file
    game = Grid(filename=filename)

    # Display game prompt until the maximum number of moves is reached
    while len(game.moves) < game.max_moves:
        if not game.moves:
            display_grid(game.level_state)

        display_stats(game)
        remaining_moves: int = game.max_moves - len(game.moves)
        moveset: str = take_moves(remaining_moves)

        for m in moveset:
            move = Move(m)
            game.moves.append(move)

            snapshots = game.roll()
            for snapshot in snapshots:     # Print each snapshot with a 0.3s delay
                display_grid(snapshot)
                time.sleep(0.3)

            # Keep track of level states and cumulative points per move played
            game.level_states.append((copy.deepcopy(snapshots[-1]), game.points))

            if not game.is_present('🥚'):  # Check if there are eggs left
                display_stats(game, is_final=True)
                return

    display_stats(game, is_final=True)


def clear_screen() -> None:
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([clear_cmd])


def display_grid(level_state: list[list[str]]) -> None:
    """Displays the current state of the game grid on the terminal.

    Args:
        level_state (list[list[str]]): A 2D list representing the current state of the grid.
    """
    clear_screen()
    grid = "\n".join(''.join(row) for row in level_state)
    print(grid)


def display_stats(game: Grid, is_final: bool = False) -> None:
    """Displays the current game statistics.

    Args:
        game (Grid): The current game grid object.
        is_final (bool): Indicates if the game has ended.
    """
    arrow_moves = [str(mv) for mv in game.moves]
    print("Played moves:", ''.join(arrow_moves))
    print("Remaining moves:", game.max_moves - len(game.moves))
    print("Points:", game.points)

    if is_final:
        leaderboard = Leaderboard(game.name)
        # Save points for the leaderboard
        prompt: str = "Enter your name for the leaderboard: "
        player_name: str = input(prompt)
        leaderboard.update(player_name, game.points)

        # Display the leaderboard
        leaderboard.display()
        sys.exit()


def validate_moves(moveset: str, remaining_moves: int) -> str:
    """Validates the player's input for moves.

    The function ensures that only valid move characters ('F', 'f', 
    'B', 'b', 'L', 'l', 'R', 'r') are accepted. If the user enters 
    more moves than can be accommodated within the remaining 
    available moves, the excess moves are truncated.

    Args:
        moveset (str): The string of moves entered by the player
        remaining_moves (int): The remaining number of moves allowed.

    Returns:
        str: A string of valid moves entered by the user, truncated
        if it exceeds the allowed number of remaining moves.
    """
    moveset = re.sub(r'[^FfBbLlRr]', '', moveset)   # Only accept valid moves
    if len(moveset) > remaining_moves:              # Remove excess moves if number exceeds maximum
        moveset = moveset[:remaining_moves]
    return moveset


def take_moves(remaining_moves: int) -> str:
    """Prompts the player for moves and passes it through the validator

    The function prompts the player to enter their moves, then uses the `validate_moves`
    function to ensure that only valid characters are accepted and that the number of moves
    does not exceed the remaining allowed moves.

    Args:
        remaining_moves (int): The remaining number of moves allowed.

    Returns:
        str: A string of valid moves entered by the user, truncated 
        if it exceeds the allowed number of remaining moves.
    """
    moveset = input("Enter moves: ")                # Get player input
    return validate_moves(moveset, remaining_moves)


if __name__ == "__main__":
    # Check first if the player included a level filename argument
    if len(sys.argv) > 1:
        LEVEL_FILENAME: str = str(sys.argv[1])
        main(LEVEL_FILENAME)
    else:
        print("[Error] Please include a filename argument for a game level.")
