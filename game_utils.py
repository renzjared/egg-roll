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
    if move.lower() == "f":         # forward
        return (-1, 0)
    elif move.lower() == "b":       # backward
        return (1, 0)
    elif move.lower() == "l":       # left
        return (0, -1)
    elif move.lower() == "r":       # right
        return (0, 1)

def clear_screen():
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([clear_cmd])
    pass

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

def roll(grid, move):
    global rows
    global cols
    rows = len(grid)
    cols = len(grid[0])

    snapshots = []
    prev_state = []
    dy, dx = directions(move)

    while grid != prev_state:
        prev_state = [row[:] for row in grid]  # Deep copy of grid
        snapshots.append([row[:] for row in grid]) 
        move_eggs(grid, dx, dy)
    return snapshots

def move_eggs(grid, dx, dy):
    eggs = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == '🥚']      # Save position of eggs  
    clear_grid(grid)                                                                      # Temporarily remove eggs
    place_eggs(grid, eggs, dx, dy)

def clear_grid(grid):
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '🥚':
                grid[r][c] = '🟩'                    # Replace eggs with grass

def place_eggs(grid, eggs, dx, dy):
    while eggs:
        updated = False
        for (r, c) in eggs[:]:
            new_r = r + dy
            new_c = c + dx

            if grid[new_r][new_c] == '🪹':             # If adjacent to empty nest, 
                grid[new_r][new_c] = '🪺'              # Fill empty nest with egg
                eggs.remove((r, c))
                updated = True
            elif grid[new_r][new_c] == '🟩' and (new_r, new_c) not in eggs:           # Roll to empty space
                grid[new_r][new_c] = '🥚'
                eggs.remove((r, c))
                updated = True
            elif grid[new_r][new_c] == '🍳':           # Egg gets cooked
                eggs.remove((r, c))
                updated = True
            elif grid[new_r][new_c] in ['🪺', '🧱']:   # These act as permanent barriers
                grid[r][c] = '🥚'                      # Reset original position
                eggs.remove((r, c))
                updated = True

        if not updated:
            for (r, c) in eggs[:]:
                grid[r][c] = '🥚'                    # Restore eggs that couldn't be moved
            break