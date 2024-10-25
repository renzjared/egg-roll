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

from enum import Enum
from game_utils import move_to_arrow, is_present, roll

class GameState(Enum):
    RESTART = "restart"

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
        if isinstance(moveset, GameState):    # Checks if the player entered a special command instead of a moveset
            update_game(moveset, filename)
            return
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
                display_final_state(max_moves, moves, points, filename)
                return

    if len(moves) == max_moves:
        display_final_state(max_moves, moves, points, filename)

def clear_screen():
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([clear_cmd])

def display_final_state(max_moves, moves, points, filename):
    """Displays the final game statistics after all moves are made or when
       there are no more eggs to roll, and asks if the player wants to
       play again.

    Args:
        max_moves (int): The maximum number of moves allowed.
        moves (list): A list of moves made by the player.
        points (int): The total points earned by the player.
        filename (str): The path to the level file.
    """
    print("Played moves:", ''.join(moves))
    print("Remaining moves:", max_moves - len(moves))
    print("Points:", points)

    # Ask if player wants to play again
    prompt = True
    while(prompt):      # Ask again until the player responds with a valid answer: [y,Y,n,N]
        response = input("Play again? [Y/N] ")
        if response.upper() == 'Y':
            prompt = False
            main(filename)
        elif response.upper() == 'N':
            prompt = False
            main_menu()     # Go back to main menu

def update_game(gamestate, filename):
    """Update the game based on the player's input"""
    if gamestate == GameState.RESTART:
        main(filename)

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

def validate_moves(moveset, remaining_moves):
    """Validates the player's input for moves.
       Also checks if the player has called for a restart

    Args:
        moveset (str): The string of moves entered by the player
        remaining_moves (int): The remaining number of moves allowed.
    Returns:
        str: A string of valid moves entered by the user, truncated
             if it exceeds the allowed number of remaining moves.
        GameState: A special case for when the player has called for a game restart

    The function ensures that besides 'restart', only valid move characters
    ('F', 'f', 'B', 'b', 'L', 'l', 'R', 'r') are accepted. If the user enters 
    more moves than can be accommodated within the remaining 
    available moves, the excess moves are truncated.
    """
    if moveset.lower() == 'restart':
        return GameState.RESTART
    elif remaining_moves <= 0:    # Return empty string if the number of remaining moves
        return ""                 # is zero or a negative integer

    moveset = re.sub(r'[^FfBbLlRr]', '', moveset)   # Only accept valid moves
    if len(moveset) > remaining_moves:              # Remove excess moves if number exceeds maximum
        moveset = moveset[:remaining_moves]
    return moveset

def take_moves(remaining_moves):
    """Prompts the player for moves and passes it through the validator

    Args:
        remaining_moves (int): The remaining number of moves allowed.
    Returns:
        str: A string of valid moves entered by the user, truncated
             if it exceeds the allowed number of remaining moves.
        GameState: A special case for when the player has called for a game restart

    The function prompts the player to enter their moves, then uses the `validate_moves`
    function to ensure that only valid characters are accepted and that the number of moves
    does not exceed the remaining allowed moves.
    """
    moveset = input("Enter moves or command: ")      # Get player input
    return validate_moves(moveset, remaining_moves)

def main_menu():
    """Displays the main menu and processes user input to start the game, 
    view instructions, or exit.
    """
    while True:
        clear_screen()
        print("Welcome to Egg Roll!")
        print("1. Start Game")
        print("2. Instructions")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")

        if choice == '1':
            filename = input("Enter the level filename: ")
            main(filename)  # Start the game
        elif choice == '2':
            display_instructions()  # Show instructions
        elif choice == '3':
            print("Exiting the game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

def display_instructions():
    """Displays the game instructions to the player."""
    clear_screen()
    print("Instructions:")
    print("1. You will be asked to enter a series of moves.")
    print("2. Valid moves are: F (forward), B (backward), L (left), R (right).")
    print("3. Type 'restart' at any time to start over.")
    print("4. Try to collect as many points as you can before your moves run out.")
    input("Press Enter to return to the main menu...")

if __name__ == "__main__":
    # Check if the player included a level filename argument
    # If not, the main menu is displayed
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])
        main(filename)
    else:
        main_menu()