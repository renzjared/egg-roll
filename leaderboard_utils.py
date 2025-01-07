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
from pathlib import Path

from terminal_utils import clear_screen, print_format, create_table, load_localization

LEADERBOARD_FILE = "leaderboard.json"
EggRollLeaderboards = dict[str, list[dict[str, str | int]]]
EggRollLocalization = dict[str, str | list[str]]


class Leaderboard:
    """A class to manage and display game leaderboards.

    Attributes:
        filename (str): A JSON file where all game leaderboards are stored.
        level_name (str): The name of the game level associated with the leaderboard.
    """

    def __init__(self, level_name: str):
        """Initializes the Leaderboard instance.

        Args:
            level_name (str): The name of the game level.
        """
        self.filename = LEADERBOARD_FILE
        self.level_name = level_name

    def update(self, player_name: str, score: int) -> None:
        """Updates the leaderboard with a new score.

        The leaderboard is sorted to only keep the top 10 scores.

        Args:
            player_name (str): The name of the player to be added.
            score (int): The player's score.
        """
        leaderboards = read_leaderboards()
        if self.level_name not in leaderboards: # Initialize JSON Object if level is not yet stored
            leaderboards[self.level_name] = []
        leaderboards[self.level_name].append({"name": player_name, "score": score})
        leaderboards[self.level_name] = sorted(
            leaderboards[self.level_name], key=lambda x: x["score"], reverse=True
        )[:10]  # Keep top 10 scores
        self._write(leaderboards)

    def display(self) -> None:
        """Displays the leaderboard for the current game level.

        If no leaderboard exists for the current level, an error message is shown.
        """
        loc: EggRollLocalization = load_localization()
        leaderboards: EggRollLeaderboards = read_leaderboards()

        clear_screen()
        if self.level_name in leaderboards:
            data = [[idx + 1, entry['name'], entry['score']]
                for idx, entry in enumerate(leaderboards[self.level_name])]
            headers: list[str | list[str]] = ["#", loc['game_name'], loc['game_score']]
            title: str = f"{loc['leaderboard_title']}: {self.level_name}"
            table: str = create_table(data, headers, title)
            print(table)
            print()         # Blank line to separate table
        else:
            print_format(
                f"\n{loc['error_no_leaderboard_found']} {self.level_name}",
                is_centered=True,
                args=["red"]
            )

    def _write(self, leaderboards: EggRollLeaderboards) -> None:
        """Writes the leaderboard to the JSON file.

        Args:
            leaderboards (EggRollLeaderboards): Dictionary containing leaderboard data of all levels.
        """
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
            json.dump(leaderboards, file, indent=4)


def read_leaderboards() -> EggRollLeaderboards:
    """Reads the leaderboard from the JSON file.
    
    If the file exists but does not have a valid structure, an empty dictionary is returned.

    Returns:
        EggRollLeaderboards: A dictionary containing leaderboard data for all game levels,
        or an empty dictionary if the file does not exist or is invalid.
    """
    if Path(LEADERBOARD_FILE).is_file():
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            leaderboard = json.load(file)
            if isinstance(leaderboard, dict):
                return leaderboard
            return {}  # Return an empty dictionary if the structure is invalid
    return {} # File does not exist
