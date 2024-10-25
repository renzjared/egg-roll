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

rows = 0
cols = 0

def directions(move):
    if move.lower() == "↑":         # forward
        return (-1, 0)
    elif move.lower() == "↓":       # backward
        return (1, 0)
    elif move.lower() == "←":       # left
        return (0, -1)
    elif move.lower() == "→":       # right
        return (0, 1)

def clear_screen():
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([clear_cmd])

def is_present(grid, element):
    return any(element in row for row in grid)

def move_to_arrow(move):
    if move.lower() == "f":         # forward
        return '↑'
    elif move.lower() == "b":       # backward
        return '↓'
    elif move.lower() == "l":       # left
        return '←'
    elif move.lower() == "r":       # right
        return '→'

def roll(grid, moves, max_moves):
    global rows
    global cols
    rows = len(grid)
    cols = len(grid[0])

    snapshots = []
    prev_state = []
    move = moves[len(moves)-1]       # Take the last move
    points_earned = 0

    while grid != prev_state:
        prev_state = [row[:] for row in grid]               # Deep copy of grid
        snapshots.append([row[:] for row in grid]) 
        points_earned += move_eggs(grid, directions(move), moves, max_moves)      # place_eggs returns number of points earned per snapshot
    return snapshots, points_earned

def move_eggs(grid, direction, moves, max_moves):
    eggs = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == '🥚']      # Save position of eggs  
    clear_grid(grid)                                                                    # Temporarily remove eggs
    return place_eggs(grid, eggs, direction, moves, max_moves)# Returns the number of points earned

def clear_grid(grid):
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '🥚':
                grid[r][c] = '🟩'                          # Replace eggs with grass

def place_eggs(grid, eggs, direction, moves, max_moves):
    points_earned = 0

    while eggs:
        updated = False
        for (r, c) in eggs[:]:
            new_r = r + direction[0]
            new_c = c + direction[1]

            if grid[new_r][new_c] == '🪹':                   # If adjacent to empty nest, 
                grid[new_r][new_c] = '🪺'                    # Fill empty nest with egg
                eggs.remove((r, c))
                bonus_points = (max_moves - len(moves[1:]))  # Earn bonus points equal to the remaining moves left (counting the current move)
                points_earned += 10 +  bonus_points          # Earn a minimum of 10 points when an egg reaches a nest
                updated = True
            elif grid[new_r][new_c] == '🟩' and (new_r, new_c) not in eggs:           # Roll to empty space
                grid[new_r][new_c] = '🥚'
                eggs.remove((r, c))
                updated = True
            elif grid[new_r][new_c] == '🍳':                 # Egg gets cooked
                eggs.remove((r, c))
                points_earned += -5                          # Lose 5 points when an egg falls into a frying pan
                updated = True
            elif grid[new_r][new_c] in ['🪺', '🧱']:        # These act as permanent barriers
                grid[r][c] = '🥚'                            # Reset original position
                eggs.remove((r, c))
                updated = True

        if not updated:
            for (r, c) in eggs[:]:
                grid[r][c] = '🥚'                    # Restore eggs that couldn't be moved
            break

    return points_earned