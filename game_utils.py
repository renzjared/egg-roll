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

from copy import deepcopy
from dataclasses import dataclass
import sys

from terminal_utils import print_format, load_localization

EggRollGrid = list[list[str]]
EggRollLocalization = dict[str, str | list[str]]


@dataclass
class Move:
    """Represents an Egg Roll level movement (grid tilting)."""
    move_string: str #: Direction of the move ('f', 'b', 'l', 'r')

    def __str__(self) -> str:
        """Converts the move direction to an arrow representation.

        Returns:
            str: An arrow symbol representing the move direction.
        """
        arrows = {'f': '↑', 'b': '↓', 'l': '←', 'r': '→'}
        return arrows[self.move_string.lower()]

    def directions(self) -> tuple[int, int]:
        """Converts the move direction to a coordinate change.

        Returns:
            tuple[int, int]: A tuple representing row and column changes (dr, dc).
        """
        coord_change = {"f": (-1, 0), "b": (1, 0), "l": (0, -1), "r": (0, 1),}
        return coord_change[self.move_string]


class Grid:
    """Represents the game grid and its operations.

    Attributes:
        name (str): The name of the level file.
        level (list[str]): The level configuration read from the file.
        max_moves (int): The maximum number of moves allowed for the level.
        moves (list[Move]): The list of moves made by the player.
        points (int): The player's current score.
        level_state (EggRollGrid): The current state of the grid.
        level_states (list[tuple[EggRollGrid, int]]): A history of grid states and scores.
    """

    def __init__(
            self,
            grid_data: tuple[list[str], int] | None = None,
            filename: str = "Unnamed"
    ) -> None:
        """Initializes a Grid object with the given level file.

        Args:
            grid_data (tuple[list[str], int]): The level configuration data.
            filename (str): The path to the level file.
        """
        if grid_data:
            self.level = grid_data[0]
            self.max_moves = grid_data[1]
            self.level_state = [list(line) for line in self.level]
        elif filename:
            self.level = self.read_level(filename)
            self.max_moves = int(self.level[1])
            self.level_state = [list(line) for line in self.level[2:]]
        else:
            raise ValueError("No level data provided.")
        self.name = filename
        self.moves: list[Move] = []
        self.points: int = 0
        self.level_states: list[tuple[EggRollGrid, int]] = [(self.copy_grid(), self.points)]

    def read_level(self, filename: str) -> list[str]:
        """Reads the game level from a specified file.

        Args:
            filename (str): The path to the level file.

        Returns:
            list[str]: A list of strings representing the level configuration.

        Raises:
            Exception: If the file cannot be opened or read.
        """
        loc: EggRollLocalization = load_localization()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                game_level = [line.strip('\n\r') for line in file]  # Remove newlines
                return game_level
        except FileNotFoundError as e:
            print_format(f"File not found: {e}", is_centered=True, args=["red"])
            print_format(str(loc["exit"]), is_centered=True, args=["light_yellow"])
            sys.exit()
        except IOError as e:
            print_format(f"Error reading file: {e}", is_centered=True, args=["red"])
            print_format(str(loc["exit"]), is_centered=True, args=["light_yellow"])
            sys.exit()

    def roll(self, moves: list[Move] | None = None) -> list[EggRollGrid]:
        """Simulate rolling eggs on the grid based on the provided move

        Args:
            moves (list[Move]): A list of moves to simulate on the grid.

        Returns:
            list[EggRollGrid]: A list of snapshots of the grid after the move.
        """
        if moves:
            self.moves = moves

        snapshots = []
        move = self.moves[-1] # The move to be performed is the last move added

        while True:
            snapshots.append([row[:] for row in self.level_state])  # Capture the grid's state
            points_change, moved = self._apply_move(move)
            self.points += points_change
            if not moved:
                break

        return snapshots

    def is_present(self, element: str) -> bool:
        """Check if an element is present in the grid

        Args:
            element (str): The element to search for in the grid.

        Returns:
            bool: True if the element is found, False otherwise.
        """
        return any(element in row for row in self.level_state)

    def copy_grid(self) -> EggRollGrid:
        """Creates a deep copy of the current grid state.

        Returns:
            EggRollGrid: A deep copy of the grid.
        """
        return deepcopy(self.level_state)

    def _set_position(self, pos: tuple[int, int], value: str) -> None:
        """Sets a specific position in the grid to a given value.

        Args:
            pos (tuple[int, int]): The grid position to update (row, column).
            value (str): The value to set at the given position.
        """
        r, c = pos
        self.level_state[r][c] = value

    def _find_eggs(self, move: Move | None = None) -> list[tuple[int, int]]:
        """Finds all egg positions in the grid.

        Args:
            move_direction (Move | None): The previous move made.
            
        Returns:
            list[tuple[int, int]]: A list of egg positions.
        """
        eggs = [(r, c)
            for r in range(len(self.level_state))
            for c in range(len(self.level_state[0]))
            if self.level_state[r][c] == '🥚'
        ]

        # Sort eggs depending on move direction to maintain egg collision
        if move:
            dr, dc = move.directions()
            if dr == -1:    # Forward
                eggs.sort()
            elif dr == 1:   # Backward
                eggs.sort(reverse=True)
            elif dc == -1:  # Left
                eggs.sort(key=lambda x: (x[1], x[0]))
            elif dc == 1:   # Right
                eggs.sort(key=lambda x: (x[1], x[0]), reverse=True)
        return eggs

    def _clear_eggs(self) -> None:
        """Clears eggs from the grid by replacing them with grass."""
        for r, row in enumerate(self.level_state):
            for c, cell in enumerate(row):
                if cell == '🥚':
                    self.level_state[r][c] = '🟩'

    def _apply_move(self, move: Move) -> tuple[int, bool]:
        """Applies a single move to all eggs on the grid.

        Args:
            move (Move): The move to be performed.

        Returns:
            tuple[int, bool]: The change in points, and a bool representing whether any eggs moved.
        """
        # Basically, 'apply_move' only records changes between snapshots
        # while 'roll' keeps track of all snapshots for every directional move
        eggs = self._find_eggs(move)
        current_points = 0
        moved = False

        self._clear_eggs()
        if not eggs:
            return current_points, moved

        for egg in eggs:
            outcome, new_pos = self._calculate_new_position(egg, move)
            if outcome == "move":
                self._set_position(new_pos, '🥚')
                moved = True
            elif outcome == "fill_nest":
                self._set_position(new_pos, '🪺')
                current_points += calculate_points(self.max_moves, self.moves)
                moved = True
            elif outcome == "fry":
                current_points -= 5
                moved = True
            elif outcome == "reset":
                self._set_position(egg, '🥚')

        return current_points, moved

    def _calculate_new_position(
            self, pos: tuple[int, int],
            move: Move,
) -> tuple[str, tuple[int, int]]:
        """
        Calculates the outcome of moving an egg in a specific direction.

        Args:
            pos (tuple[int, int]): The position of the egg to be moved (row, col).
            direction (tuple[int, int]): The change in coordinates (drow, dcol).

        Returns:
            tuple[str, tuple[int, int]]: The outcome of the move, and the new position (row, col).
        """
        r, c = pos
        dr, dc = move.directions()
        new_r, new_c = r + dr, c + dc

        # Check grid boundaries
        if not (0 <= new_r < len(self.level_state) and 0 <= new_c < len(self.level_state[0])):
            return "reset", pos

        target = self.level_state[new_r][new_c]
        if target == '🪹':
            return "fill_nest", (new_r, new_c)
        if target == '🟩':
            return "move", (new_r, new_c)
        if target == '🍳':
            return "fry", pos
        if target in ['🪺', '🧱']:
            return "reset", pos
        return "reset", pos


def calculate_points(max_moves: int, moves: list[Move]) -> int:
    """Calculates points based on moves left and other conditions.

    Args:
        max_moves (int): The maximum number of moves allowed for the level.
        moves (list[Move]): The list of moves made by the player.

    Returns:
        int: The points scored by the player.
    """
    remaining_moves = max_moves - len(moves[1:])
    return 10 + remaining_moves
