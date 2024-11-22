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
import shutil
import subprocess
import sys

# Extend system path to access termcolor folder
# Termcolor is installed locally due to importing issues (may be fixed later)
sys.path.append("termcolor")
from termcolor import colored


def clear_screen():
    """Clear the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([clear_cmd])


def terminal_dimensions():
    """Return the terminal's current dimensions as (height, width)."""
    terminal = os.get_terminal_size()
    return terminal.lines, terminal.columns


def center_text(text, pad_right = True):
    """Center the given text horizontally within the terminal.

    Args:
        text (str): The text to be centered.
        pad_right (bool): Whether to pad on both sides or only on the left.

    Returns:
        str: The horizontally-centered text.
    """
    _, terminal_width = terminal_dimensions()


    # Check if the text is purely composed of these emojis
    # Emojis are twice as wide as alphanumeric characters.
    # This is considered so that emojis are centerede properly.
    emojis = {"🧱","🥚","🟩","🪹","🪺","🍳"}
    cleaned = set(text.replace('\n', '').replace(' ', ''))
    if cleaned.issubset(emojis):
        text_width = max(len(line) for line in text.splitlines())
        text_width *= 2 # Doubled to account for emoji width
    else:
        text_width = max(len(line) for line in text.splitlines())

    padding_width = (terminal_width - text_width) // 2
    padding = " " * padding_width
    rpadding = padding if pad_right else '' # Add padding to the right, if needed

    # Apply padding to each line of the text
    return '\n'.join(
        f"{padding}{line}{rpadding}" for line in text.splitlines()) 


def color_text(text, args):
    """Apply color and styling to text using the termcolor library.

    Args:
        text (str): The text to format.
        args (list): A list containing arguments for color and style (e.g., "green").

    Returns:
        str: The colored and styled text.
    """
    return colored(text, *args)


def print_format(text, is_centered=False, args=None):
    """Print text in a specified format, with optional centering and color.

    Args:
        text (str): The text to format and print.
        is_centered (bool): Whether to center the text horizontally.
        args (list): A list containing arguments for color and style (e.g., "green").
    """
    # Center the text horizontally first, if needed, because
    # using colors add ANSI escape sequences that offset the centering
    if is_centered:
        text = center_text(text)

    # Apply color formatting if arguments are provided
    if args:
        text = color_text(text, args)
    print(text)
