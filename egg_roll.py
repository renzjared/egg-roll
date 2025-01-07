"""
Copyright 2025 Renz Jared Rolle.

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

from game_utils import Move, Grid
from main_menu import display_main_menu
from terminal_utils import (
    center_text, clear_screen, terminal_dimensions, print_format, load_localization
)
from leaderboard_utils import Leaderboard

EggRollLocalization = dict[str, str | list[str]]


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


class EndReason(Enum):
    """Enumeration for reasons why a game ;eve; ended.

    Attributes:
        RESTART (str): Indicates that the player ran out of moves.
        NO_MORE_EGGS (str): Indicates that there are no more eggs left to roll.
    """
    RAN_OUT_OF_MOVES = "ran_out_of_moves"
    NO_MORE_EGGS = "no_more_eggs"

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
            display_grid(game.level_state, game.name)

        display_stats(game)
        remaining_moves: int = game.max_moves - len(game.moves)
        moveset: str | GameState = take_moves(remaining_moves)

        if isinstance(moveset, GameState):    # Checks if the player entered a special command
            update_game(moveset, filename)    # instead of a moveset
            return

        if moveset == "u":                    # Undo latest move
            undo_last_move(game)
        else:
            for m in moveset:
                move = Move(m)
                game.moves.append(move)

                snapshots = game.roll()
                for snapshot in snapshots:     # Print each snapshot with a 0.3s delay
                    display_grid(snapshot, filename)
                    time.sleep(0.3)

                # Keep track of level states and cumulative points per move played
                game.level_states.append((copy.deepcopy(snapshots[-1]), game.points))

                if not game.is_present('🥚'):
                    display_stats(game, EndReason.NO_MORE_EGGS)
                    return

    display_stats(game, EndReason.RAN_OUT_OF_MOVES)


def undo_last_move(game: Grid) -> None:
    """Undoes the last move made by the player.

    Args:
        game (Grid): The current game grid object.
    """
    if game.moves:
        game.moves.pop()
        game.level_states.pop()
        game.level_state, game.points = game.level_states[-1]
        display_grid(game.level_state, game.name)


def display_grid(level_state: list[list[str]], filename: str) -> None:
    """Displays the current state of the game grid on the terminal.

    Args:
        level_state (list[list[str]]): A 2D list representing the current state of the grid.
        filename (str): The name of the level file being played.
    """
    loc = load_localization()
    _, cols = terminal_dimensions()
    div: str = "═" * cols
    clear_screen()
    print_format(div, is_centered=True)
    print_format(f" {loc['game_level']}: " + filename, is_centered=False, args=["green"])
    print_format(div + "\n\n", is_centered=True)

    grid = "\n".join(''.join(row) for row in level_state)
    print_format(grid + "\n ", is_centered=True)
    print_format(div, is_centered=True)


def display_stats(game: Grid, end_reason: EndReason | None = None) -> None:
    """Displays the current game statistics.

    Args:
        game (Grid): The current game grid object.
        is_final (bool): Indicates if the game has ended.
    """
    loc: EggRollLocalization = load_localization()
    remaining_moves: str = str(game.max_moves - len(game.moves))

    arrow_moves = [str(mv) for mv in game.moves]
    print_format(
        str(loc["game_previous_moves"]) + ''.join(arrow_moves),
        is_centered=False,
        args=["light_yellow"]
    )
    print_format(
        str(loc["game_remaining_moves"]) + remaining_moves,
        is_centered=False,
        args=["light_yellow"]
    )
    print_format(
        str(loc["game_points"]) + str(game.points),
        is_centered=False,
        args=["light_yellow"]
    )

    if end_reason:
        print_format(
            str(loc[f"game_ended_{end_reason.value}"]),
            is_centered=True,
            args=["light_yellow"]
        )

        leaderboard = Leaderboard(game.name)
        # Save points for the leaderboard
        prompt: str = str(loc["prompt_name_leaderboard"])
        player_name: str = input(center_text(prompt, pad_right=False))
        leaderboard.update(player_name, game.points)

        # Display the leaderboard
        leaderboard.display()

        # Ask if player wants to play again
        prompt_user: bool = True
        while prompt_user:  # Ask again until the player responds with a valid answer: [y,Y,n,N]
            prompt = str(loc["prompt_play_again"])
            response: str = input(center_text(prompt, pad_right=False))
            if response.upper() == 'Y':
                prompt_user = False
                main(game.name)         # Replay level
            elif response.upper() == 'N':
                prompt_user = False
                display_main_menu()     # Go back to main menu


def update_game(gamestate: GameState, filename: str) -> None:
    """Updates the game based on the player's input.

    Args:
        gamestate (GameState): The gamestate command to be made.
        filename (str): The name of the level being played.
    """
    if gamestate == GameState.RESTART:
        main(filename)
    elif gamestate == GameState.RETURN:
        display_main_menu()
    elif gamestate == GameState.TERMINATE:
        loc: EggRollLocalization = load_localization()
        print_format(f"\n{loc['exit_goodbye']}\n", True, args=['magenta', None, ('bold',)])
        time.sleep(1)
        clear_screen()
        sys.exit()


def validate_moves(moveset: str, remaining_moves: int) -> str | GameState:
    """Validates the player's input for moves.

    The function ensures that besides 'restart', 'return', and 'exit' (and their aliases),
    only valid move characters ('F', 'f', 'B', 'b', 'L', 'l', 'R', 'r') are accepted.
    If the user enters more moves than can be accommodated within the remaining 
    available moves, the excess moves are truncated.

    Args:
        moveset (str): The string of moves entered by the player
        remaining_moves (int): The remaining number of moves allowed.

    Returns:
        Union[str, GameState]: A string of valid moves entered by the user, truncated if needed, or
        a special GameState command for updating present game state.
    """
    if moveset.strip().lower() in ['restart', 'umulit']:
        return GameState.RESTART
    if moveset.strip().lower() in ['menu', 'return', 'bumalik']:
        return GameState.RETURN
    if moveset.strip().lower() in ['exit', 'terminate', 'isara']:
        return GameState.TERMINATE
    if moveset.strip().lower() in ['u', 'undo']:
        return "u"
    if remaining_moves <= 0:    # Return empty string if the number of remaining moves
        return ""               # is zero or a negative integer

    moveset = re.sub(r'[^FfBbLlRr]', '', moveset)   # Only accept valid moves
    if len(moveset) > remaining_moves:              # Remove excess moves if number exceeds maximum
        moveset = moveset[:remaining_moves]
    return moveset


def take_moves(remaining_moves: int) -> str | GameState:
    """Prompts the player for moves or commands and validates the input.

    Args:
        remaining_moves (int): The remaining number of moves allowed.
        
    Returns:
        str | GameState: Either a string of valid moves or a game state command.
    """
    loc: EggRollLocalization = load_localization()
    moveset = input(loc["prompt_enter_moves_or_cmd"])      # Get player input
    return validate_moves(moveset, remaining_moves)


if __name__ == "__main__":
    # Check if the player included a level filename argument
    # If not, the main menu is displayed
    if len(sys.argv) > 1:
        LEVEL_FILENAME = str(sys.argv[1])
        main(LEVEL_FILENAME)
    else:
        display_main_menu()
