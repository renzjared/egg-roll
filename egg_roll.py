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
import re
import sys
import time

from enum import Enum
from game_utils import move_to_arrow, is_present, roll
from main_menu import display_main_menu
from terminal_utils import clear_screen, terminal_dimensions, color_text, print_format


class GameState(Enum):
    """Enumeration for special game commands that control game flow.

    Attributes:
        RESTART (str): Command to restart the game.
        RETURN (str): Command to return to the main menu.
        TERMINATE (str): Command to terminate the game session.
    """
    RESTART = "restart"
    RETURN = "return"
    TERMINATE = "terminate"


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
    max_moves = int(level[1])
    moves = []  # initialize move history
    points = 0  # initialize number of points

    level_states = []
    level_state = [list(line) for line in level[2:]] # Convert strings into a list of characters
    level_states.append((copy.deepcopy(level_state), 0))

    # Display game prompt until the maximum number of moves is reached
    while len(moves) < max_moves:
        if len(moves) == 0:
            display_grid(level_state, filename)

        display_state(max_moves, moves, points)
        remaining_moves = max_moves - len(moves)

        moveset = take_moves(remaining_moves)
        if isinstance(moveset, GameState):    # Checks if the player entered a special command
            update_game(moveset, filename)    # instead of a moveset
            return
        if moveset == "u":                    # Undo latest move
            if len(moves) > 0:
                moves = moves[:-1]
                level_states = level_states[:-1]
                level_state, points = level_states[-1]
                display_grid(level_state, filename)
        else:
            for move in moveset:
                moves.append(move_to_arrow(move))
                snapshots, points_earned = roll(level_state, moves, max_moves)
                for snapshot in snapshots:     # Print each snapshot with a 0.5s delay
                    display_grid(snapshot, filename)
                    time.sleep(0.5)
                points += points_earned        # Update point counter

                # Keep track of level states and cumulative points per move played
                level_states.append((copy.deepcopy(snapshots[-1]), points))

                if not is_present(level_state[:], '🥚'):  # Check if there are eggs left
                    display_final_state(max_moves, moves, points, filename)
                    return

    if len(moves) == max_moves:
        display_final_state(max_moves, moves, points, filename)


def display_grid(level_state, filename):
    """
    Displays the current state of the game grid on the terminal.

    Args:
        level_state (list): A 2D list representing the current state of the grid.
        filename (str): The name of the level file being played.
    """
    _, cols = terminal_dimensions()
    div = "=" * cols
    clear_screen()
    print_format(div, is_centered=True)
    print_format(" Level: " + filename, is_centered=False, args=["green"])
    print_format(div + "\n\n", is_centered=True)

    grid = "\n".join(''.join(row) for row in level_state)
    print_format(grid + "\n ", is_centered=True)
    print_format(div, is_centered=True)


def display_state(max_moves, moves, points):
    """
    Displays the current game statistics, including the previous moves, 
    remaining moves, and the total points.

    Args:
        max_moves (int): The maximum number of moves allowed in the game.
        moves (list): A list of moves made by the player.
        points (int): The total points earned by the player.
    """
    remaining_moves = str(max_moves - len(moves))
    print_format("Previous moves: " + ''.join(moves), is_centered=False, args=["light_yellow"])
    print_format("Remaining moves: " + remaining_moves, is_centered=False, args=["light_yellow"])
    print_format("Points: " + str(points), is_centered=False, args=["light_yellow"])


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
    display_state(max_moves, moves, points)
    # Ask if player wants to play again
    prompt = True
    while prompt:      # Ask again until the player responds with a valid answer: [y,Y,n,N]
        response = input("Play again? [Y/N] ")
        if response.upper() == 'Y':
            prompt = False
            main(filename)
        elif response.upper() == 'N':
            prompt = False
            display_main_menu()     # Go back to main menu


def update_game(gamestate, filename):
    """Update the game based on the player's input"""
    if gamestate == GameState.RESTART:
        main(filename)
    elif gamestate == GameState.RETURN:
        display_main_menu()
    elif gamestate == GameState.TERMINATE:
        sys.exit()


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
            level = [line.strip('\n\r') for line in level]  # Remove newlines
            return level
    except Exception as e:
        print(e)
        return


def validate_moves(moveset, remaining_moves):
    """Validates the player's input for moves.
       Also checks if the player has called for a restart

    Args:
        moveset (str): The string of moves entered by the player
        remaining_moves (int): The remaining number of moves allowed.
    Returns:
        str: A string of valid moves entered by the user, truncated
             if it exceeds the allowed number of remaining moves.
        GameState: A special case for when the player has called
             for a game restart, termination, or return to main menu

    The function ensures that besides 'restart', only valid move characters
    ('F', 'f', 'B', 'b', 'L', 'l', 'R', 'r') are accepted. If the user enters 
    more moves than can be accommodated within the remaining 
    available moves, the excess moves are truncated.
    """
    if moveset.strip().lower() == 'restart':
        return GameState.RESTART
    if moveset.strip().lower() in ['menu', 'return']:
        return GameState.RETURN
    if moveset.strip().lower() in ['exit', 'terminate']:
        return GameState.TERMINATE
    if moveset.strip().lower() in ['u', 'undo']:
        return "u"
    if remaining_moves <= 0:    # Return empty string if the number of remaining moves
        return ""               # is zero or a negative integer

    moveset = re.sub(r'[^FfBbLlRr]', '', moveset)   # Only accept valid moves
    if len(moveset) > remaining_moves:              # Remove excess moves if number exceeds maximum
        moveset = moveset[:remaining_moves]
    return moveset


def take_moves(remaining_moves):
    """Prompts the player for moves or commands and passes it through the validator"""
    moveset = input("Enter moves or command: ")      # Get player input
    return validate_moves(moveset, remaining_moves)

if __name__ == "__main__":
    # Check if the player included a level filename argument
    # If not, the main menu is displayed
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])
        main(filename)
    else:
        display_main_menu()
