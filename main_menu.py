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

import sys
import time
from pathlib import Path

from terminal_utils import center_text, clear_screen, print_format, terminal_dimensions


def display_instructions():
    """Displays the game instructions to the player."""
    clear_screen()
    print("Instructions:")
    print("1. You will be asked to enter a series of moves.")
    print("2. Valid moves are: F (forward), B (backward), L (left), R (right).")
    print("3. Type 'restart' at any time to start over.")
    print("4. Try to collect as many points as you can before your moves run out.")
    print_format("\nPress Enter to return to the main menu...", False, ["yellow", None, ['blink']])
    input()


def display_levels():
    """Displays the list of available levels and allows the player to select one."""
    clear_screen()
    levels_dir = Path("")
    levels = sorted(str(level) for level in levels_dir.glob("*.in"))

    _, cols = terminal_dimensions()
    div = "=" * cols
    print_format(div, is_centered=True)
    print_format("Level Selector", is_centered=True, args=["light_yellow"])
    print_format(div + "\n\n", is_centered=True)

    if not levels:
        print_format("No levels available. Please add level files (.in) to the directory.", is_centered=True, args=["red"])
        print_format("\nPress Enter to return to the main menu...", args=["yellow", None, "blink"])
        input()
        return None
    else:
        menu = '\n'.join(str(num) + ". " + level_path for num, level_path in enumerate(levels, 1))
        print_format("\n" + menu + "\n ", True)
        choice = input(center_text("Enter level file name or number (1-{}): ".format(len(levels)), False))

        try:
            level_index = int(choice) - 1
            if 0 <= level_index < len(levels):
                return levels[level_index]
            else:
                raise ValueError
        except ValueError:
            if choice in levels:
                return choice
            print_format(f"\nInvalid choice: ({choice}). Please try again.", True, args=["red"])
            time.sleep(1.5)
            return display_levels()


def display_main_menu():
    """Displays the main menu and processes user input to start the game, 
    view instructions, or exit.
    """
    while True:
        clear_screen()
        header = """




       ███████╗ ██████╗  ██████╗     ██████╗  ██████╗ ██╗     ██╗         
       ██╔════╝██╔════╝ ██╔════╝     ██╔══██╗██╔═══██╗██║     ██║         
       █████╗  ██║  ███╗██║  ███╗    ██████╔╝██║   ██║██║     ██║         
       ██╔══╝  ██║   ██║██║   ██║    ██╔══██╗██║   ██║██║     ██║         
       ███████╗╚██████╔╝╚██████╔╝    ██║  ██║╚██████╔╝███████╗███████╗    
       ╚══════╝ ╚═════╝  ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝    



        """
        print_format(header, True, args=["green"])
        print_format("Welcome to Egg Roll!", True, args=['yellow', None, ['bold']])

        menu_options = ["Start Game", "Instructions", "Credits", "Exit"]
        menu = '\n'.join(str(num) + ". " + option for num, option in enumerate(menu_options, 1))
        print_format("\n" + menu + "\n ", True)

        choice = input(center_text("Select an option (1-4): ", pad_right = False))

        # Load the game level
        if choice.strip() == '1':
            level_file = display_levels()
            if level_file:
                from egg_roll import main      # Use local import to avoid circular imports
                main(level_file) 

        # Show game instructions
        elif choice.strip() == '2':
            display_instructions()
    
        # Show credits
        elif choice.strip() == '3':
            clear_screen()
            print_format("Developed by Renz Jared G. Rolle.", is_centered=True, args=["green"])
            print_format("License: GPL-3.0", is_centered=True, args=["green"])
            print_format("https://github.com/renzjared/egg-roll", is_centered=True, args=["cyan"])
            print_format("\nPress Enter to return to the main menu...", False, ["yellow", None, ['blink']])
            input()

        # Exit game
        elif choice.strip() == '4':
            print_format("\nExiting the game. Goodbye!\n", True, args=['magenta', None, ['bold']])
            time.sleep(1)
            clear_screen()
            sys.exit()

        # Dispaly error message
        else:
            print_format("\nInvalid choice. Please try again.", True, args=["red"])
            time.sleep(1.5)
