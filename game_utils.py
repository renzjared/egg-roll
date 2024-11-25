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

def move_to_arrow(move):
    """Convert a single-character move command to an arrow symbol."""
    arrows = {'f': '↑', 'b': '↓', 'l': '←', 'r': '→'}
    return arrows[move.lower()]


def directions(move):
    """Convert a move symbol to a tuple representing coordinate change (d_row, d_col)."""
    coord_change = {"↑": (-1, 0), "↓": (1, 0), "←": (0, -1), "→": (0, 1),}
    return coord_change[move]


def is_present(grid, element):
    """Check if an element is present in the grid"""
    return any(element in row for row in grid)


def roll(grid, moves, max_moves):
    """Simulate rolling eggs on the grid based on the provided move

    Args:
        grid (list): A 2D list representing the grid.
        moves (list): A list of all moves performed, including the move to be performed.
        max_moves (int): The maximum number of moves allowed.
    Returns:
        tuple: A list of snapshots of the grid after the move, and the total points earned.
    """
    snapshots = []
    move = moves[-1]        # The move to be performed is the last move added
    points_earned = 0       # Initialize points
    direction = directions(move)

    while True:
        snapshots.append([row[:] for row in grid])  # Capture the grid's state
        points_change, moved = apply_move(grid, direction, max_moves, moves)
        points_earned += points_change
        if not moved:
            break
    return snapshots, points_earned


def apply_move(grid, direction, max_moves, moves):
    """Apply a single move to all eggs on the grid."""
    eggs = find_eggs(grid, direction)
    points_earned = 0
    moved = False

    clear_eggs(grid)
    if not eggs:
        return points_earned, moved

    for egg in eggs:
        outcome, new_pos = calculate_new_position(grid, egg, direction)
        if outcome == "move":
            set_position(grid, new_pos, '🥚')
            moved = True
        elif outcome == "fill_nest":
            set_position(grid, new_pos, '🪺')
            points_earned += calculate_points(max_moves, moves)
            moved = True
        elif outcome == "fry":
            points_earned -= 5
            moved = True
        elif outcome == "reset":
            set_position(grid, egg, '🥚')

    return points_earned, moved


def find_eggs(grid, move_direction=None):
    """Find all egg positions in the grid."""
    eggs = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '🥚']

    # Sort eggs depending on move direction to maintain egg collision
    if move_direction:
        dr, dc = move_direction
        if dr == -1:    # Forward
            eggs.sort()
        elif dr == 1:   # Backward
            eggs.sort(reverse=True)
        elif dc == -1:  # Left
            eggs.sort(key=lambda x: (x[1], x[0]))
        elif dc == 1:   # Right
            eggs.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return eggs


def clear_eggs(grid):
    """Clear eggs from the grid by replacing them with grass."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '🥚':
                grid[r][c] = '🟩'


def calculate_new_position(grid, pos, direction):
    """
    Calculate the outcome of moving an egg in a specific direction.

    Args:
        grid (list): A 2D list representing the grid.
        pos (tuple): A tuple representing the position of the egg to be moved (row, column).
        direction (tuple): A tuple representing the change in coordinates (row_change, col_change).
    Returns:
        tuple: A string representing the outcome of the movement, and a tuple representing the position of the egg (row, column).
    """
    r, c = pos
    dr, dc = direction
    new_r, new_c = r + dr, c + dc

    # Check grid boundaries
    if not (0 <= new_r < len(grid) and 0 <= new_c < len(grid[0])):
        return "reset", pos

    target = grid[new_r][new_c]
    if target == '🪹':
        return "fill_nest", (new_r, new_c)
    if target == '🟩':
        return "move", (new_r, new_c)
    if target == '🍳':
        return "fry", pos
    if target in ['🪺', '🧱']:
        return "reset", pos
    return "reset", pos


def calculate_points(max_moves, moves):
    """Calculate points based on moves left and other conditions."""
    remaining_moves = max_moves - len(moves[1:])
    return 10 + remaining_moves


def set_position(grid, pos, value):
    """Set a specific position in the grid to a given value."""
    r, c = pos
    grid[r][c] = value
