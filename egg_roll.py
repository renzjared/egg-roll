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

from game_utils import clear_screen, roll



VALID_MOVES = ["F", "f", "B", "b", "L", "l", "R", "r"]

def main(filename):
    # Read game level file, and take the number of rows and number of maximum moves 
    level = read_level(filename)
    rows = int(level[0]); max_moves = int(level[1])
    moves = 0

    level_state = [list(l) for l in level[2::]]  

    # Display game prompt until the maximum number of moves is reached
    while(moves < max_moves):
        for row in level_state:
            print(''.join(row))
        print("Remaining moves:", max_moves - moves)
        moveset = input("Enter moves: ") 

        if not all(move in VALID_MOVES for move in moveset):
            print('Error: Invalid move sequence')
            continue
        if len(moveset) > max_moves - moves:
            print("Max moves error")
            continue

        for move in moveset:
            clear_screen()
            snapshots = roll(level_state, move)
            for snapshot in snapshots:
                for row in snapshot:
                    print(''.join(row))  # Print each row as a string
                time.sleep(0.5)
                clear_screen()
            moves += 1

        # TO DO: Detect win/lose state

def read_level(filename):
    # Check if file exists; send error message if the file does not exist
    # We assume that the file is valid (as per MP1 Section 3)
    try:
        level = open(filename, "r") 
        level = [l.strip('\n\r') for l in level]            # Remove newlines
        return level
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # check first if the user included a level filename
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])
        main(filename)
    else:
        print("[Error] Please include a filename argument for a game level.")