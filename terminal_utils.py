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


def clear_screen():
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([clear_cmd])


def center_text(text, pad_right = True):
    """Centers the given text"""
    terminal_width = os.get_terminal_size().columns
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


def print_center(text):
    """Prints the given text in the center of the terminal."""
    centered_text = center_text(text)
    print(centered_text)