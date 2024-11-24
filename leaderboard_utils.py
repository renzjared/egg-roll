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
from terminal_utils import print_format, terminal_dimensions, create_table

from pathlib import Path

LEADERBOARD_FILE = "leaderboard.json"

def read_leaderboard():
    """Reads the leaderboard from the JSON file."""
    if Path(LEADERBOARD_FILE).is_file():
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    return {}

def write_leaderboard(leaderboards):
    """Writes the leaderboard to the JSON file."""
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboards, file, indent=4)

def update_leaderboard(name, score, level_name):
    """Updates the leaderboard with a new score."""
    leaderboards = read_leaderboard()
    if level_name not in leaderboards:   # Initialize JSON Object if level is not yet stored
        leaderboards[level_name] = []
    leaderboards[level_name].append({"name": name, "score": score})
    leaderboards[level_name] = sorted(leaderboards[level_name], key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10 scores
    write_leaderboard(leaderboards)

def display_leaderboard(level_name):
    """Displays the leaderboard for a particular level."""
    leaderboards = read_leaderboard()
    if level_name in leaderboards:
        data = [[idx + 1, entry['name'], entry['score']] for idx, entry in enumerate(leaderboards[level_name])]
        headers = ["#", "Name", "Score"]
        title = f"Leaderboard: {level_name}"

        table = create_table(data, headers, title)
        print(table)
        print()         # Blank line to separate table
    else:
        print_format(f"\nNo leaderboard found for Level: {level_name}", is_centered=True, args=["red"])
