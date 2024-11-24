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

import json
import sys
import time
from pathlib import Path

from terminal_utils import center_text, clear_screen, print_format, create_table, load_localization


def display_instructions():
    """Displays the game instructions to the player."""
    loc = load_localization()
    clear_screen()
    print(loc["instructions_title"])
    for line in loc["instructions_content"]:
        print(line)
    print_format(f"\n{loc["prompt_press_enter_to_return"]}", False, ["yellow", None, ['blink']])
    input()


def display_levels():
    """Displays the list of available levels and allows the player to select one."""
    loc = load_localization()
    clear_screen()
    levels_dir = Path("")
    levels = sorted(str(level) for level in levels_dir.glob("*.in"))

    if not levels:
        print_format(loc["error_no_levels_found"], is_centered=True, args=["red"])
        print_format(f"\n{loc["prompt_press_enter_to_return"]}", args=["yellow", None, "blink"])
        input()
        return None

    # If levels are found:
    data = []
    for idx, level in enumerate(levels, 1):
        rows, columns, moves_allowed = parse_level(level)
        data.append([idx, Path(level).name, f"{rows} x {columns}", moves_allowed])
    headers = ["#", loc["game_level_name"], loc["game_size"], loc["game_max_moves"]]
    title = loc["level_selector_title"]
    table = create_table(data, headers, title)
    print(table)
    print()         # Blank line to separate table

    # Ask the player for level to be played
    choice = input(center_text(f"\n{loc["prompt_enter_level"]} (1-{len(levels)}): ", pad_right=False))
    try:
        level_index = int(choice) - 1
        if 0 <= level_index < len(levels):
            return levels[level_index]
        raise ValueError
    except ValueError:
        if choice in levels:    # Check if the player entered a valid level file name
            return choice
        print_format(f"\n{loc["error_invalid_choice"]}".format(choice=choice), True, args=["red"])
        time.sleep(1.5)
        return display_levels()


def display_main_menu():
    """Displays the main menu and processes user input to start the game, 
    view instructions, or exit.
    """
    loc = load_localization()
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
        print_format(loc["welcome_message"], True, args=['yellow', None, ['bold']])

        menu_options = [loc["menu_start"], loc["menu_instructions"], loc["menu_change_language"], loc["menu_credits"], loc["menu_exit"]]
        menu = '\n'.join(str(num) + ". " + option for num, option in enumerate(menu_options, 1))
        print_format("\n" + menu + "\n ", True)

        # Prompt user to select from 1 to n = 5
        choice = input(center_text(f"{loc["select_option"]} ".format(n = 5), pad_right = False))

        # Load the game level
        if choice.strip() == '1':
            level_file = display_levels()
            if level_file:
                from egg_roll import main      # Use local import to avoid circular imports
                main(level_file) 

        # Show game instructions
        elif choice.strip() == '2':
            display_instructions()

        # Change game language
        elif choice.strip() == '3':
            language_code = "tl" if loc["language"] == "en" else "en"
            settings_file = Path("localization") / "settings.json"
            with open(settings_file, "w") as file:
                json.dump({"language": language_code}, file)
            loc = load_localization() # Change localization
            display_main_menu()    # Reload main menu

        # Show credits
        elif choice.strip() == '4':
            clear_screen()
            print_format("Developed by Renz Jared G. Rolle.", is_centered=True, args=["green"])
            print_format("License: GPL-3.0", is_centered=True, args=["green"])
            print_format("https://github.com/renzjared/egg-roll", is_centered=True, args=["cyan"])
            print_format(f"\n{loc["prompt_press_enter_to_return"]}", False, ["yellow", None, ['blink']])
            input()

        # Exit game
        elif choice.strip() == '5':
            print_format(f"\n{loc["exit_goodbye"]}\n", True, args=['magenta', None, ['bold']])
            time.sleep(1)
            clear_screen()
            sys.exit()

        # Dispaly error message
        else:
            print_format(loc["error_invalid_choice"].format(choice=choice), True, args=["red"])
            time.sleep(1.5)


def parse_level(level_path):
    """
    Parses the level file to extract the dimensions of the grid and the number of moves allowed.

    Args:
        level_path (str): The path to the level file.

    Returns:
        tuple: A tuple containing the dimensions (rows, columns) and the number of moves allowed.
    """
    with open(level_path, 'r') as file:
        lines = file.readlines()
        rows = len(lines) - 2            # Exclude the first two lines (metadata)
        columns = len(lines[2].strip())  # Assume all rows have the same number of columns
        moves_allowed = int(lines[1].strip())
    return (rows, columns, moves_allowed)
