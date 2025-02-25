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

import json
import os
import subprocess
import sys

from pathlib import Path
from typing import Literal, Sequence, cast

# Extend system path to access termcolor folder
# Termcolor is installed locally due to importing issues (may be fixed later)
sys.path.append("termcolor")
from termcolor import colored, COLORS, HIGHLIGHTS, ATTRIBUTES

EggRollLocalization = dict[str, str | list[str]]


def clear_screen() -> None:
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([clear_cmd])


def terminal_dimensions() -> tuple[int, int]:
    """Returns the terminal's current dimensions as (height, width)."""
    terminal = os.get_terminal_size()
    return terminal.lines, terminal.columns


def center_text(text: str, pad_right: bool = True) -> str:
    """Centers the given text horizontally within the terminal.

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


def color_text(
        text: str,
        args: Sequence[str | Sequence[str | None] | None]
) -> str:
    """Applies color and styling to text using the Termcolor library.

    Args:
        text (str): The text to format.
        args Sequence[str | Sequence[str | None] | None]: A sequence of style arguments (e.g., "green").

    Returns:
        str: The colored and styled text.
    """
    # Cast values to the appropriate Literal types (for mypy strict type-checking)
    color = cast(
        Literal[
            "black", "grey", "red", "green", "yellow", "blue", "magenta", "cyan",
            "light_grey", "dark_grey", "light_red", "light_green", "light_yellow",
            "light_blue", "light_magenta", "light_cyan", "white"
        ] | None,
        next((arg for arg in args if arg in COLORS), None)
    )
    highlight = cast(
        Literal[
            "on_black", "on_grey", "on_red", "on_green", "on_yellow", "on_blue",
            "on_magenta", "on_cyan", "on_light_grey", "on_dark_grey", "on_light_red",
            "on_light_green", "on_light_yellow", "on_light_blue", "on_light_magenta",
            "on_light_cyan", "on_white"
        ] | None,
        next((arg for arg in args if arg in HIGHLIGHTS), None)
    )
    attrs = []
    if len(args) > 2 and args[2]:
        attrs = [
            cast(
                Literal["bold", "dark", "underline", "blink", "reverse", "concealed", "strike"],
                arg
            )
            for arg in args[2] if arg in ATTRIBUTES
        ]
    return colored(text, color, highlight, attrs)


def print_format(
        text: str,
        is_centered: bool = False,
        args: Sequence[str | Sequence[str | None] | None] | None = None
) -> None:
    """Prints text in a specified format, with optional centering and color.

    Args:
        text (str): The text to format and print.
        is_centered (bool): Whether to center the text horizontally.
        args (Sequence[str | Sequence[str | None] | None] | None): A sequence of style arguments (e.g., "green").
    """
    # Center the text horizontally first, if needed, because
    # using colors add ANSI escape sequences that offset the centering
    if is_centered:
        text = center_text(text)

    # Apply color formatting if arguments are provided
    if args:
        text = color_text(text, args)
    print(text)


def create_table(
        data: list[list[str | int]],
        headers: list[str | list[str]] | None = None,
        title: str | None = None
) -> str:
    """Creates a formatted table from arbitrary data.

    Args:
        data (list[list[str | int]]): A 2D list representing the table data.
        headers (list[str | list[str]] | None): A list of column headers (defaults to None).
        title (str | None): The title of the table, displayed on the topmost row as a header.

    Returns:
        str: The formatted table as a string.
    """
    _, cols = terminal_dimensions()
    col_widths = [max(len(str(item)) for item in col) + 1 for col in zip(*data)]
    if headers:
        col_widths = [max(len(headers[i]) + 1, col_widths[i]) for i in range(len(headers))]

    col_formats = [f"{{:<{w}}}" for w in col_widths]        # Save widths of table columns
    header_sep = "┼".join("─" * (w + 1) for w in col_widths)
    top_sep = "┬".join("─" * (w + 1) for w in col_widths)

    table_lines = []

    if headers:
        header_line = "│ ".join(fmt.format(hdr) for fmt, hdr in zip(col_formats, headers))
        table_lines.append(f"┌{top_sep}┐")
        table_lines.append(f"│ {header_line}│")
        table_lines.append(f"├{header_sep}┤")

    for row in data:
        row_line = "│ ".join(fmt.format(item) for fmt, item in zip(col_formats, row))
        table_lines.append(f"│ {row_line}│")

    table_lines.append(f"└{'┴'.join('─' * (w + 1) for w in col_widths)}┘")
    centered_table = center_text('\n'.join(table_lines))

    # Add title lines to the centered table last.
    # This allows the table below to be displayed in the center.
    if title:
        title_lines = []
        div = "═" * cols   # horizontal divider line
        title_lines.append(div)
        title_lines.append(color_text(center_text(title), ['light_yellow']))
        title_lines.append(div)
        title_lines.append("")

        titled_table = '\n'.join(title_lines) + centered_table
        return titled_table
    return centered_table


def load_localization(language_code: str | None = None) -> EggRollLocalization:
    """
    Loads the localization file based on the provided language code.

    If no language code is provided, the function will read the set language
    code from the "settings.json" file located in the "localization" directory.
    The default language is "en" (English).

    If the localization file structure is invalid, an empty dictionary is returned.

    Args:
        language_code (str | None): The language code for the localization file.
                                    If None, the set language code will be used.
    Returns:
        EggRollLocalization: A dictionary containing the localization data.
    """ 
    if not language_code:
        settings_file = Path("localization") / "settings.json"
        with open(settings_file, "r", encoding="utf-8") as file:
            language_code = json.load(file)["language"]

    localization_file = Path("localization") / f"{language_code}.json"
    with open(localization_file, "r", encoding="utf-8") as file:
        locale = json.load(file)
        if isinstance(locale, dict):
            return locale
        return {}  # Return an empty dictionary if the structure is invalid
