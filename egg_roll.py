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

import os
import re
import subprocess
import sys
import time

from game_utils import move_to_arrow, is_present, roll

def main(filename):
    """Main function to run the egg roll game.

    Args:
        filename (str): The path to the file containing the game level.

    The function reads the level file, processes player moves,
    updates the game state, and displays the results until the maximum
    moves are reached or when there are no more eggs to roll.
    """
    # Read game level file, and take the number of rows and number of maximum moves 
    level = read_level(filename)
    rows = int(level[0])
    max_moves = int(level[1])
    moves = []  # initialize move history
    points = 0  # initialize number of points

    level_state = [list(l) for l in level[2:]] # Convert strings into a list of characters

    # Display game prompt until the maximum number of moves is reached
    while len(moves) < max_moves:
        if len(moves) == 0:
            clear_screen()
            for row in level_state:
                print(''.join(row))

        remaining_moves = max_moves - len(moves)
        print("Previous moves:", ''.join(moves))
        print("Remaining moves:", remaining_moves)
        print("Points:", points)

        moveset = take_moves(remaining_moves)
        for move in moveset:
            moves.append(move_to_arrow(move))
            snapshots, points_earned = roll(level_state, moves, max_moves)
            for snapshot in snapshots:        # Print each snapshot with a 0.5s delay
                clear_screen()                # Clear the screen in between snapshots
                for row in snapshot:
                    print(''.join(row))
                time.sleep(0.5)
            points += points_earned           # Update point counter

        if not is_present(level_state[:], '🥚'):  # Check if there are eggs left
            display_final_state(max_moves, moves, points)
            return

    if len(moves) == max_moves:
        display_final_state(max_moves, moves, points)

def clear_screen():
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([clear_cmd])

def display_final_state(max_moves, moves, points):
    """Displays the final game statistics after all moves are made or when there are no more eggs to roll.

    Args:
        max_moves (int): The maximum number of moves allowed.
        moves (list): A list of moves made by the player.
        points (int): The total points earned by the player.
    """
    print("Played moves:", ''.join(moves))
    print("Remaining moves:", max_moves - len(moves))
    print("Points:", points)

def read_level(filename):
    """Reads the game level from a specified file.

    Args:
        filename (str): The path to the level file.
    Returns:
        list: A list of strings representing the level configuration.
    Raises:
        Exception: If the file cannot be opened or read.
    """
    try:
        with open(filename, "r") as level:
            level = [l.strip('\n\r') for l in level]  # Remove newlines
            return level
    except Exception as e:
        print(e)

def take_moves(remaining_moves):
    """Prompts the user for moves and validates the input.

    Args:
        max_moves (int): The remaining number of moves allowed.
    Returns:
        str: A string of valid moves entered by the user, truncated
             if it exceeds the allowed number of remaining moves.

    The function ensures that only valid move characters ('F', 'f', 
    'B', 'b', 'L', 'l', 'R', 'r') are accepted. If the user enters 
    more moves than can be accommodated within the remaining 
    available moves, the excess moves are truncated.
    """
    moveset = re.sub(r'[^FfBbLlRr]', '', input("Enter moves: "))  # Only accept valid moves
    if len(moveset) > remaining_moves:   # Remove excess moves if number exceeds maximum
        moveset = moveset[:remaining_moves-1]
    return moveset

if __name__ == "__main__":
    # Check first if the user included a level filename argument
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])
        main(filename)
    else:
        print("[Error] Please include a filename argument for a game level.")