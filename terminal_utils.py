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
    """Return a tuple representing the of the terminal"""
    height = os.get_terminal_size().lines
    width = os.get_terminal_size().columns
    return height, width

def center_text(text, pad_right = True):
    """Centers the given text horizontally"""
    terminal_width = terminal_dimensions()[1]
    text_width = max([len(line) for line in text.split("\n")])
    padding_width = (terminal_width - text_width) // 2
    padding = " " * padding_width

    centered_text = []
    for line in text.split("\n"):
        if pad_right:
            centered_text.append(padding + line + padding)
        else:
            centered_text.append(padding + line)

    return '\n'.join(centered_text)


def color_text(text, *args):
    """Use the termcolor library to format colored text"""
    return colored(text, *args)


def print_format(text, is_centered, *args):
    """Print the given text, formatted in a certain way."""
    if is_centered:                 # Center the text horizontally first, if needed, because using
        text = center_text(text)    # colors add additional characters that offset the centering
    if args:
        text = color_text(text, *args)
    print(text)
