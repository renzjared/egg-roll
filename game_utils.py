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

rows = 0
cols = 0


def move_to_arrow(move):
    """Convert a single-character move command to an arrow symbol."""
    arrows = {'f': '↑', 'b': '↓', 'l': '←', 'r': '→'}
    return arrows.get(move.lower(), '')

def directions(move):
    """Converts a directional move symbol to a coordinate change.

    Args:
        move (str): A string representing a move direction ('↑', '↓', '←', '→').
    Returns:
        tuple: A tuple representing the change in coordinates (row_change, col_change).
    """
    if move.lower() == "↑":         # forward
        return (-1, 0)
    elif move.lower() == "↓":       # backward
        return (1, 0)
    elif move.lower() == "←":       # left
        return (0, -1)
    elif move.lower() == "→":       # right
        return (0, 1)

def is_present(grid, element):
    """Checks if an element is present in the grid"""
    return any(element in row for row in grid)

def roll(grid, moves, max_moves):
    """Simulates rolling eggs on the grid based on the provided move

    Args:
        grid (list): A 2D list representing the grid.
        moves (list): A list of all moves performed, including the move to be performed.
        max_moves (int): The maximum number of moves allowed.
    Returns:
        tuple: A list of snapshots of the grid after the move, and the total points earned.
    """
    global rows
    global cols
    rows = len(grid)
    cols = len(grid[0])

    snapshots = []
    prev_state = []
    move = moves[-1]       # The move to be performed is the last move added
    points_earned = 0

    while grid != prev_state:
        prev_state = [row[:] for row in grid]                                     # Deep copy of grid
        snapshots.append([row[:] for row in grid]) 
        points_earned += move_eggs(grid, directions(move), moves, max_moves)      # place_eggs returns number of points earned per snapshot
    return snapshots, points_earned

def move_eggs(grid, direction, moves, max_moves):
    """Moves eggs on the grid toward the specified direction.

    Args:
        grid (list): A 2D list representing the grid.
        direction (tuple): A tuple representing the direction to move eggs (row_change, col_change).
        moves (list): A list of all moves performed, including the move to be performed.
        max_moves (int): The maximum number of moves allowed.
    Returns:
        int: The total points earned (or lost) for the particular snapshot.
    """

    eggs = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == '🥚']      # Save position of eggs  
    clear_grid(grid)                                                                     # Temporarily remove eggs

    points_earned = 0      # Initialize points

    while eggs:
        updated = False
        for (r, c) in eggs[:]:
            new_r = r + direction[0]
            new_c = c + direction[1]

            if grid[new_r][new_c] == '🪹':                   # If adjacent to empty nest, 
                grid[new_r][new_c] = '🪺'                    # Fill empty nest with egg
                eggs.remove((r, c))
                bonus_points = (max_moves - len(moves[1:]))  # Earn bonus points equal to the remaining moves left (counting the current move)
                points_earned += 10 + bonus_points           # Earn a minimum of 10 points when an egg reaches a nest
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
                grid[r][c] = '🥚'                           # Restore eggs that couldn't be moved
            break
    return points_earned

def find_eggs(grid):
    """Find all egg positions in the grid."""
    return [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '🥚']

def clear_grid(grid):
    """Clear eggs from the grid by replacing them with grass."""
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '🥚':
                grid[r][c] = '🟩'