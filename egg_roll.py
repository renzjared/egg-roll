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

from game_utils import clear_screen, move_to_arrow, is_present, roll

VALID_MOVES = ["F", "f", "B", "b", "L", "l", "R", "r"]

def main(filename):
    # Read game level file, and take the number of rows and number of maximum moves 
    level = read_level(filename)
    rows = int(level[0])
    max_moves = int(level[1])
    moves = []   # initialize move history
    points = 0  # initialize number of points

    level_state = [list(l) for l in level[2:]]  

    # Display game prompt until the maximum number of moves is reached
    while(len(moves) < max_moves):
        if len(moves) == 0:
            clear_screen()
            for row in level_state:
                print(''.join(row))

        print("Previous moves:", ''.join(moves))
        print("Remaining moves:", max_moves - len(moves))
        moveset = input("Enter moves: ") 

        if not all(move in VALID_MOVES for move in moveset):
            print('Error: Invalid move sequence')
            continue
        elif len(moveset) > max_moves - len(moves):
            print("Max moves error")
            continue

        for move in moveset:
            snapshots = roll(level_state, move)
            for snapshot in snapshots:
                clear_screen()
                for row in snapshot:
                    print(''.join(row))  # Print each row as a string
                time.sleep(0.5)
            moves.append(move_to_arrow(move))

        if not is_present(level_state[:], '🥚') and is_present(level_state[:], '🪹'):
            print("Eggs cooked")
            return
        elif not is_present(level_state[:], '🥚'):
            print("win state")
            return

    if len(moves) == max_moves:
        print("[!] You ran out of moves.")

def read_level(filename):
    # Check if file exists; send error message if the file does not exist
    # We assume that the file is valid (as per MP1 Section 3)
    try:
        with open(filename, "r") as level:
            level = [l.strip('\n\r') for l in level]  # Remove newlines
            return level
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Check first if the user included a level filename argument
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])
        main(filename)
    else:
        print("[Error] Please include a filename argument for a game level.")