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

import unittest
from copy import deepcopy
from random import choice, randint

import egg_roll
import egg_roll_basic
import game_utils
from egg_roll import GameState


class TestEggRoll(unittest.TestCase):
    """
    Test suite for Egg Roll.

    This test suite contains various test cases to validate the functionality of Egg Roll,
    including grid initialization, move validation, grid tilting, and egg movements.

    Methods:
        setUpClass(cls): Sets up the initial grid configurations for the test cases.
        setUp(self): Initializes grid instances by deep copying predefined grid data.
        test_validate_moves(self): Tests the `validate_moves` function of the `egg_roll` module.
        test_update_game_states(self): Tests that the game state is correctly updated when a player inputs a command.
        test_move_to_arrow(self): Tests that all possible inputs return the correct arrow symbol.
        test_directions(self): Tests that all possible inputs return the correct positional change values.
        test_roll(self): Tests the `roll` method of the grid class.
        test_is_present(self): Tests the `is_present` method of the `Grid` class.
        test_set_position(self): Tests the `_set_position` method of the grid objects.
        test_find_eggs(self): Tests the `_find_eggs` method of the `Grid` class.
        test_clear_eggs(self): Tests the `_clear_eggs` method of the `Grid` class.
        test_apply_move(self): Tests applying moves to a grid.
        test_calculate_new_position(self): Tests the `_calculate_new_position` method of the `Grid` class.
        test_calculate_points(self): Tests the `calculate_points` function of the `game_utils` module.
    """

    initial_grids: dict[str, list[str]]

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up the initial grid configurations for the test cases."""
        cls.initial_grids = {
            "grid1": [
                '🧱🧱🧱🧱🧱',
                '🧱🟩🥚🟩🧱',
                '🧱🪹🟩🍳🧱',
                '🧱🧱🧱🧱🧱'
            ],
            "grid2": [
                '🧱🧱🧱🧱🧱',
                '🧱🥚🟩🟩🧱',
                '🧱🪹🍳🧱🧱',
                '🧱🪺🟩🍳🧱',
                '🧱🧱🧱🧱🧱'
            ],
            "grid3": [
                '🧱🧱🧱🧱🧱🧱',
                '🧱🍳🟩🟩🍳🧱',
                '🧱🟩🟩🥚🪹🧱',
                '🧱🪺🧱🥚🪹🧱',
                '🧱🧱🧱🧱🧱🧱'
            ],
            "grid4": [
                '🧱🧱🧱🧱🧱🧱',
                '🧱🍳🟩🟩🍳🧱',
                '🧱🟩🪹🟩🟩🧱',
                '🧱🪺🟩🟩🪹🧱',
                '🧱🧱🧱🧱🧱🧱'
            ],
            "grid5": [
                '🍳🧱🟩',
                '🧱🟩🟩',
                '🟩🍳🧱'
            ],
            "grid_cs11": [
                '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱',
                '🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱',
                '🧱🟩🟩🟩🧱🧱🟩🟩🟩🧱🧱🧱🟩🟩🧱',
                '🧱🟩🟩🧱🟩🟩🧱🟩🧱🟩🟩🟩🟩🟩🧱',
                '🧱🟩🟩🪹🟩🟩🟩🟩🟩🧱🧱🟩🟩🟩🧱',
                '🧱🟩🟩🧱🟩🟩🧱🥚🟩🟩🟩🧱🟩🟩🧱',
                '🧱🟩🟩🟩🧱🧱🟩🥚🟩🧱🧱🪹🟩🟩🧱',
                '🧱🟩🟩🟩🟩🟩🟩🪹🟩🟩🟩🟩🟩🟩🧱',
                '🧱🟩🟩🟩🟩🧱🟩🥚🟩🧱🟩🟩🟩🟩🧱',
                '🧱🟩🟩🟩🧱🧱🟩🟩🧱🧱🟩🟩🟩🟩🧱',
                '🧱🟩🟩🟩🟩🧱🟩🟩🟩🧱🟩🟩🟩🟩🧱',
                '🧱🟩🟩🟩🟩🧱🟩🟩🟩🧱🟩🟩🟩🟩🧱',
                '🧱🪺🟩🟩🧱🧱🧱🟩🧱🧱🧱🟩🟩🪺🧱',
                '🧱🪺🪺🟩🟩🟩🟩🟩🟩🟩🟩🟩🪺🪺🧱',
                '🧱🍳🍳🍳🍳🍳🍳🍳🍳🍳🍳🍳🍳🍳🧱'
            ],
            "grid_labyrinth": [
                '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱',
                '🧱🥚🥚🟩🟩🟩🟩🟩🟩🟩🟩🧱🟩🟩🧱',
                '🧱🥚🧱🧱🟩🧱🧱🧱🟩🟩🧱🧱🟩🧱🧱',
                '🧱🟩🧱🍳🟩🧱🧱🍳🟩🟩🧱🟩🟩🟩🧱',
                '🧱🟩🧱🧱🟩🧱🟩🟩🟩🟩🧱🟩🧱🧱🧱',
                '🧱🟩🟩🟩🟩🧱🟩🟩🟩🟩🟩🟩🟩🪹🧱',
                '🧱🟩🧱🧱🧱🧱🧱🟩🧱🧱🧱🟩🧱🧱🧱',
                '🧱🟩🟩🟩🟩🍳🟩🟩🟩🟩🟩🟩🟩🍳🧱',
                '🧱🟩🧱🧱🟩🧱🧱🟩🧱🧱🧱🟩🧱🧱🧱',
                '🧱🟩🟩🧱🟩🧱🟩🟩🟩🧱🟩🟩🟩🟩🧱',
                '🧱🟩🟩🟩🟩🧱🧱🟩🟩🧱🟩🟩🧱🧱🧱',
                '🧱🧱🧱🧱🥚🟩🟩🟩🟩🧱🧱🟩🧱🧱🧱',
                '🧱🟩🟩🟩🟩🧱🟩🟩🟩🟩🟩🟩🟩🟩🧱',
                '🧱🍳🧱🟩🍳🧱🧱🟩🟩🍳🧱🍳🟩🪹🧱',
                '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱'
            ],
            "grid_sacrifice": [
                '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱',
                '🧱🧱🧱🧱🟩🟩🟩🟩🟩🟩🟩🧱🧱🧱🧱',
                '🧱🧱🧱🟩🧱🟩🍳🧱🍳🟩🧱🟩🧱🧱🧱',
                '🧱🧱🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱🧱🧱',
                '🧱🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱🧱',
                '🧱🟩🟩🟩🟩🧱🧱🥚🧱🧱🟩🟩🟩🟩🧱',
                '🧱🟩🧱🟩🪺🟩🟩🟩🟩🟩🪺🟩🧱🟩🧱',
                '🧱🟩🟩🟩🟩🟩🥚🍳🪹🟩🟩🟩🟩🟩🧱',
                '🧱🟩🍳🟩🟩🟩🟩🟩🟩🟩🟩🟩🍳🟩🧱',
                '🧱🟩🧱🧱🟩🟩🧱🟩🧱🟩🟩🧱🧱🟩🧱',
                '🧱🟩🧱🟩🟩🟩🟩🧱🟩🟩🟩🟩🧱🟩🧱',
                '🧱🟩🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱🟩🧱',
                '🧱🟩🧱🟩🟩🧱🟩🟩🟩🧱🟩🟩🧱🟩🧱',
                '🧱🟩🟩🟩🟩🟩🍳🧱🍳🟩🟩🟩🟩🟩🧱',
                '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱'
            ],
            "empty_grid": [] # Edge case
        }

    def setUp(self) -> None:
        """
        Sets up the test environment.

        This method initializes several grid instances by deep copying
        predefined grid data from `self.initial_grids`.
        """

        self.grid1 = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["grid1"], 5)))
        self.grid2 = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["grid2"], 5)))
        self.grid3 = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["grid3"], 5)))
        self.grid4 = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["grid4"], 5)))
        self.grid5 = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["grid5"], 5)))
        self.grid_cs11 = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["grid_cs11"], 15)))
        self.grid_labyrinth = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["grid_labyrinth"], 15)))
        self.grid_sacrifice = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["grid_sacrifice"], 15)))
        self.empty_grid = deepcopy(game_utils.Grid(grid_data=(self.initial_grids["empty_grid"], 5)))


    def test_validate_moves(self) -> None:
        """
        Tests the `validate_moves` function of the `egg_roll` module.

        This validates that single and multiple valid moves are accepted,
        to which the function returns the valid moves up to the remaining moves.
        Invalid characters are filtered out, and edge cases (such as
        exponentially large inputs, and input of symbols) are handled gracefully.
        """

        self.assertEqual(egg_roll.validate_moves('f', 5), 'f')
        self.assertEqual(egg_roll.validate_moves('Bl', 3), 'Bl')
        self.assertEqual(egg_roll.validate_moves('l', 5), 'l')
        self.assertEqual(egg_roll.validate_moves('R', 1), 'R')
        self.assertEqual(egg_roll.validate_moves('lllll', 5), 'lllll')

        # Tests that valid moves equal to remaining moves are accepted.
        self.assertEqual(egg_roll.validate_moves('LRFB', 4), 'LRFB')
        self.assertEqual(egg_roll.validate_moves('lRrB', 4), 'lRrB')
        self.assertEqual(egg_roll.validate_moves('FB', 2), 'FB')
        self.assertEqual(egg_roll.validate_moves('Bb', 2), 'Bb')
        self.assertEqual(egg_roll.validate_moves('f', 1), 'f')

        # Tests that an empty moveset returns an empty string.
        self.assertEqual(egg_roll.validate_moves('', 5), '')
        self.assertEqual(egg_roll.validate_moves('', 0), '')
        self.assertEqual(egg_roll.validate_moves('', 2048), '')
        self.assertEqual(egg_roll.validate_moves('', 31415926535), '')
        self.assertEqual(egg_roll.validate_moves('', -11235813), '')
        self.assertEqual(egg_roll.validate_moves('', -31415926535), '')
        self.assertEqual(egg_roll.validate_moves('', 2**50), '')
        self.assertEqual(egg_roll.validate_moves('', 2**10000), '')

        # Tests that moves exceeding remaining moves are truncated.
        self.assertEqual(egg_roll.validate_moves('llllll', 5), 'lllll')
        self.assertEqual(egg_roll.validate_moves('FFFFF', 3), 'FFF')
        self.assertEqual(egg_roll.validate_moves('FFFFF', 3), 'FFF')
        self.assertEqual(egg_roll.validate_moves('llllll', 2), 'll')
        self.assertEqual(egg_roll.validate_moves('FFFFF', 3), 'FFF')
        self.assertEqual(egg_roll.validate_moves('l', 0), '')       # These cases *should* not occur
        self.assertEqual(egg_roll.validate_moves('gfdsgsed694tseaAKfest4905wef0rtgw35%*@#$tskg5&@#$fdfgh', -3214124), '')

        # Tests that invalid characters are filtered out.
        self.assertEqual(egg_roll.validate_moves('a', 7), '')
        self.assertEqual(egg_roll.validate_moves('p', 9), '')
        self.assertEqual(egg_roll.validate_moves('@', 5645678), '')
        self.assertEqual(egg_roll.validate_moves('#*U$@&*$*(&@%@%', 4), '')
        self.assertEqual(egg_roll.validate_moves('%L35w6r463%@apoe%', 4), 'Lr')
        self.assertEqual(egg_roll.validate_moves('asfhuiosedtwe', 99), 'f')
        self.assertEqual(egg_roll.validate_moves('9459156*23#$@B', 5), 'B')
        self.assertEqual(egg_roll.validate_moves('FFFFGHHH', 5), 'FFFF')
        self.assertEqual(egg_roll.validate_moves('LrFb!@#$%', 5), 'LrFb')
        self.assertEqual(egg_roll.validate_moves('LFRBxyz', 3), 'LFR')
        self.assertEqual(egg_roll.validate_moves('fgsdasdrhyRbadfadr@355345', 3), 'frR')
        self.assertEqual(egg_roll.validate_moves('lawsdas463@dasdasrds^#Q$adwda^#&&#slwadvh345253r', 4), 'lrlr')
        self.assertEqual(egg_roll.validate_moves('lawsdas463@dasdasrds^#Q$adwda^#&&#slwadvh345253r'*999, 4), 'lrlr')
        self.assertEqual(egg_roll.validate_moves('a'*2**10, 10), '')
        self.assertEqual(egg_roll.validate_moves('a'*2**10, 2*10), '')
        self.assertEqual(egg_roll.validate_moves('lr'*(10**8), 4), 'lrlr')


    def test_validate_moves_basic(self) -> None:
        """
        Tests the `validate_moves` function of the `egg_roll_basic` module.

        This validates that single and multiple valid moves are accepted,
        to which the function returns the valid moves up to the remaining moves.
        Invalid characters are filtered out, and edge cases (such as
        exponentially large inputs, and input of symbols) are handled gracefully.
        """

        self.assertEqual(egg_roll_basic.validate_moves('f', 5), 'f')
        self.assertEqual(egg_roll_basic.validate_moves('Bl', 3), 'Bl')
        self.assertEqual(egg_roll_basic.validate_moves('l', 5), 'l')
        self.assertEqual(egg_roll_basic.validate_moves('R', 1), 'R')
        self.assertEqual(egg_roll_basic.validate_moves('lllll', 5), 'lllll')

        # Tests that valid moves equal to remaining moves are accepted.
        self.assertEqual(egg_roll_basic.validate_moves('LRFB', 4), 'LRFB')
        self.assertEqual(egg_roll_basic.validate_moves('lRrB', 4), 'lRrB')
        self.assertEqual(egg_roll_basic.validate_moves('FB', 2), 'FB')
        self.assertEqual(egg_roll_basic.validate_moves('Bb', 2), 'Bb')
        self.assertEqual(egg_roll_basic.validate_moves('f', 1), 'f')

        # Tests that an empty moveset returns an empty string.
        self.assertEqual(egg_roll_basic.validate_moves('', 5), '')
        self.assertEqual(egg_roll_basic.validate_moves('', 0), '')
        self.assertEqual(egg_roll_basic.validate_moves('', 2048), '')
        self.assertEqual(egg_roll_basic.validate_moves('', 31415926535), '')
        self.assertEqual(egg_roll_basic.validate_moves('', -11235813), '')
        self.assertEqual(egg_roll_basic.validate_moves('', -31415926535), '')
        self.assertEqual(egg_roll_basic.validate_moves('', 2**50), '')
        self.assertEqual(egg_roll_basic.validate_moves('', 2**10000), '')

        # Tests that moves exceeding remaining moves are truncated.
        self.assertEqual(egg_roll.validate_moves('llllll', 5), 'lllll')
        self.assertEqual(egg_roll.validate_moves('FFFFF', 3), 'FFF')
        self.assertEqual(egg_roll.validate_moves('FFFFF', 3), 'FFF')
        self.assertEqual(egg_roll.validate_moves('llllll', 2), 'll')
        self.assertEqual(egg_roll.validate_moves('FFFFF', 3), 'FFF')
        self.assertEqual(egg_roll.validate_moves('l', 0), '')       # These cases *should* not occur
        self.assertEqual(egg_roll.validate_moves('gfdsgsed694tseaAKfest4905wef0rtgw35%*@#$tskg5&@#$fdfgh', -3214124), '')

        # Tests that invalid characters are filtered out.
        self.assertEqual(egg_roll_basic.validate_moves('a', 7), '')
        self.assertEqual(egg_roll_basic.validate_moves('p', 9), '')
        self.assertEqual(egg_roll_basic.validate_moves('@', 5645678), '')
        self.assertEqual(egg_roll_basic.validate_moves('#*U$@&*$*(&@%@%', 4), '')
        self.assertEqual(egg_roll_basic.validate_moves('%L35w6r463%@apoe%', 4), 'Lr')
        self.assertEqual(egg_roll_basic.validate_moves('asfhuiosedtwe', 99), 'f')
        self.assertEqual(egg_roll_basic.validate_moves('9459156*23#$@B', 5), 'B')
        self.assertEqual(egg_roll_basic.validate_moves('FFFFGHHH', 5), 'FFFF')
        self.assertEqual(egg_roll_basic.validate_moves('LrFb!@#$%', 5), 'LrFb')
        self.assertEqual(egg_roll_basic.validate_moves('LFRBxyz', 3), 'LFR')
        self.assertEqual(egg_roll_basic.validate_moves('fgsdasdrhyRbadfadr@355345', 3), 'frR')
        self.assertEqual(egg_roll_basic.validate_moves('lawsdas463@dasdasrds^#Q$adwda^#&&#slwadvh345253r', 4), 'lrlr')
        self.assertEqual(egg_roll_basic.validate_moves('lawsdas463@dasdasrds^#Q$adwda^#&&#slwadvh345253r'*999, 4), 'lrlr')
        self.assertEqual(egg_roll_basic.validate_moves('a'*2**10, 10), '')
        self.assertEqual(egg_roll_basic.validate_moves('a'*2**10, 2*10), '')
        self.assertEqual(egg_roll_basic.validate_moves('lr'*(10**8), 4), 'lrlr')


    def test_update_game_states(self) -> None:
        """
        Tests that ensure the correct game state is returned when a player inputs a command.
        
        This verifies that the present game state is correctly updated when a player
        inputs a command rather than a move or move sequence. Game states are
        RESTART, RETURN, and TERMINATE.
        """
        self.assertEqual(egg_roll.validate_moves('restart', 1), GameState.RESTART)
        self.assertEqual(egg_roll.validate_moves('restart', 99), GameState.RESTART)
        self.assertEqual(egg_roll.validate_moves('RESTART', -54456), GameState.RESTART)
        self.assertEqual(egg_roll.validate_moves('ReStArT', 1), GameState.RESTART)
        self.assertEqual(egg_roll.validate_moves('reSTART', 942475674567878987), GameState.RESTART)
        self.assertEqual(egg_roll.validate_moves('return', 1), GameState.RETURN)
        self.assertEqual(egg_roll.validate_moves('menu', 99), GameState.RETURN)
        self.assertEqual(egg_roll.validate_moves('RETURN', -54456), GameState.RETURN)
        self.assertEqual(egg_roll.validate_moves('mEnU', 1), GameState.RETURN)
        self.assertEqual(egg_roll.validate_moves('reTURN', 942475674567878987), GameState.RETURN)
        self.assertEqual(egg_roll.validate_moves('terminate', 1), GameState.TERMINATE)
        self.assertEqual(egg_roll.validate_moves('exit', 99), GameState.TERMINATE)
        self.assertEqual(egg_roll.validate_moves('tErMINatE', -54456), GameState.TERMINATE)
        self.assertEqual(egg_roll.validate_moves('TERMINATE', 1), GameState.TERMINATE)
        self.assertEqual(egg_roll.validate_moves('ExIt', 942475674567878987), GameState.TERMINATE)


    # We can guarantee that this function would not take invalid inputs
    # because the moves have already been validated (test cases above)
    def test_move_to_arrow(self) -> None:
        """Tests that all of the possible inputs return correct arrow symbol"""
        self.assertEqual(str(game_utils.Move('f')), '↑')
        self.assertEqual(str(game_utils.Move('F')), '↑')
        self.assertEqual(str(game_utils.Move('b')), '↓')
        self.assertEqual(str(game_utils.Move('B')), '↓')
        self.assertEqual(str(game_utils.Move('l')), '←')
        self.assertEqual(str(game_utils.Move('L')), '←')
        self.assertEqual(str(game_utils.Move('r')), '→')
        self.assertEqual(str(game_utils.Move('R')), '→')


    # We can guarantee that this function would not take invalid inputs.
    # We only test the four possible inputs.
    def test_directions(self) -> None:
        """Tests that all of the possible inputs return correct positional change values"""
        self.assertEqual(game_utils.Move('f').directions(), (-1, 0))
        self.assertEqual(game_utils.Move('b').directions(), (1, 0))
        self.assertEqual(game_utils.Move('l').directions(), (0, -1))
        self.assertEqual(game_utils.Move('r').directions(), (0, 1))


    def test_roll(self) -> None:
        """
        Tests the `roll` method of the grid class.

        This test verifies that the method correctly simulates the tilting of the game board
        in various directions and scenarios, including cases wherein eggs are unable to move,
        or when eggs collide with each other after being in motion.
        """

        # Test roll with grid configurations and moves
        # Only one move is tested (the move at the end of the tuple `moves`)

        grid1 = self.grid1
        moves = [game_utils.Move('r')]
        snapshots = grid1.roll(moves)
        self.assertEqual(len(snapshots), 2)
        self.assertEqual(snapshots[0][1][3], '🟩')
        self.assertEqual(snapshots[1][1][3], '🥚')
        self.assertEqual(grid1.points, 0)
    
        grid2 = self.grid2
        moves = [game_utils.Move('l'), game_utils.Move('l'), game_utils.Move('l'), game_utils.Move('b')]
        snapshots = grid2.roll(moves)
        self.assertEqual(len(snapshots), 2)
        self.assertEqual(snapshots[0][1][1], '🥚')
        self.assertEqual(snapshots[0][2][1], '🪹')
        self.assertEqual(snapshots[1][2][1], '🪺')
        self.assertEqual(snapshots[1][1][3], '🟩')
        self.assertEqual(snapshots[1][2][2], '🍳')
        self.assertEqual(grid2.points, 12)

        grid_cs11 = self.grid_cs11
        moves = [game_utils.Move('b')]
        snapshots = grid_cs11.roll(moves)
        self.assertEqual(len(snapshots), 7)
        self.assertEqual(snapshots[-1][0][7], '🧱')
        self.assertEqual(snapshots[-1][1][7], '🟩')
        self.assertEqual(snapshots[-1][4][7], '🟩')
        self.assertEqual(snapshots[-1][5][7], '🟩')
        self.assertEqual(snapshots[-1][6][7], '🥚')
        self.assertEqual(snapshots[-1][7][7], '🪺')
        self.assertEqual(snapshots[-1][8][7], '🟩')
        self.assertEqual(snapshots[-1][13][7], '🟩')
        self.assertEqual(snapshots[-1][14][7], '🍳')
        self.assertEqual(grid_cs11.points, 20)

        grid_sacrifice_data = [
            '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱',
            '🧱🧱🧱🧱🟩🟩🟩🟩🟩🟩🟩🧱🧱🧱🧱',
            '🧱🧱🧱🟩🧱🟩🍳🧱🍳🟩🧱🥚🧱🧱🧱',
            '🧱🧱🧱🟩🟩🟩🟩🟩🟩🟩🟩🥚🧱🧱🧱',
            '🧱🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱🧱',
            '🧱🟩🟩🟩🟩🧱🧱🟩🧱🧱🟩🟩🟩🟩🧱',
            '🧱🟩🧱🟩🪺🟩🟩🟩🟩🟩🪺🟩🧱🟩🧱',
            '🧱🟩🟩🟩🟩🟩🟩🍳🪹🟩🟩🟩🟩🟩🧱',
            '🧱🟩🍳🟩🟩🟩🟩🟩🟩🟩🟩🟩🍳🟩🧱',
            '🧱🟩🧱🧱🟩🟩🧱🟩🧱🟩🟩🧱🧱🟩🧱',
            '🧱🟩🧱🟩🟩🟩🟩🧱🟩🟩🟩🟩🧱🟩🧱',
            '🧱🟩🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱🟩🧱',
            '🧱🟩🧱🟩🟩🧱🟩🟩🟩🧱🟩🟩🧱🟩🧱',
            '🧱🟩🟩🟩🟩🟩🍳🧱🍳🟩🟩🟩🟩🟩🧱',
            '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱'
        ]
        # Test for when all eggs are unable to move
        grid_sacrifice = game_utils.Grid(grid_data=(grid_sacrifice_data, 15))
        moves = [game_utils.Move('l'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('f')]
        snapshots = grid_sacrifice.roll(moves)
        self.assertEqual(len(snapshots), 1)
        self.assertEqual(snapshots[-1][2][11], '🥚')  # Eggs stay in their current positions
        self.assertEqual(snapshots[-1][3][11], '🥚')
        self.assertEqual(grid_sacrifice.points, 0)

        # Test if eggs do not merge into each other when colliding after being in motion
        moves = [game_utils.Move('l'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('b')]
        snapshots = grid_sacrifice.roll(moves)
        self.assertEqual(snapshots[-1][2][11], '🟩')
        self.assertEqual(snapshots[-1][3][11], '🟩')
        self.assertEqual(snapshots[-1][7][11], '🥚')
        self.assertEqual(snapshots[-1][8][11], '🥚')
        self.assertEqual(grid_sacrifice.points, 0)

        moves = [game_utils.Move('l'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('b'), game_utils.Move('l')]
        snapshots = grid_sacrifice.roll(moves)
        self.assertEqual(snapshots[-1][7][11], '🟩')
        self.assertEqual(snapshots[-1][8][11], '🟩')
        self.assertEqual(snapshots[-1][7][8], '🪺')
        self.assertEqual(grid_sacrifice.points, 14)


    def test_is_present(self) -> None:
        """
        Tests the `is_present` method of the `Grid` class.

        This test checks if various game elements are correctly identified as present or absent
        in the grid's level state (snapshot).

        Elements tested include game-related characters (e.g., '🥚', '🍳') and non-game characters
        (e.g., '🍅', '.', 'A', '5', '/', '🟦', '🟩🟩').
        """
        # For assurance, we also test for characters that are not part of the game. (Example: 🍅)
        elements: list[str] = ['🥚', '🍳', '🪹', '🪺', '🧱', '🍅', '.', 'A', '5', '/', '🟦', '🟩🟩']
        grid_names: list[str] = ["cs11.in", "labyrinth.in", "sacrifice.in", "level1.in", "level2.in"]

        for grid_name in grid_names:
            grid_obj: game_utils.Grid = game_utils.Grid(filename=grid_name)
            for element in elements:
                expected: bool = element in str(grid_obj.level_state)
                self.assertEqual(grid_obj.is_present(element), expected)

        grids: list[game_utils.Grid] = [self.grid1, self.grid2, self.grid3, self.grid4, self.grid5, self.empty_grid]
        for grid in grids:
            for element in elements:
                expected = element in str(grid.level_state)
                self.assertEqual(grid.is_present(element), expected)


    def test_set_position(self) -> None:
        """
        Tests the `_set_position` method of the grid objects.

        This test iterates over a list of Grids and changes the value of each cell in
        the Grids to verify that the `_set_position` method correctly updates the Grids'
        `level_state`.

        Note: Some test scenarios are not possible during actual gameplay as eggs cannot pass
        through solid objects such as walls. The purpose of this test is solely to verify
        the functionality of the `_set_position` method.
        """
        grids = [self.grid1, self.grid2, self.grid3, self.grid4, self.grid5, self.grid_cs11, self.grid_labyrinth, self.grid_sacrifice]
        for grid in grids:
            for r, row in enumerate(grid.level_state):
                for c, _ in enumerate(row):
                    grid._set_position((r, c), '🥚')
                    self.assertEqual(grid.level_state[r][c], '🥚')
                    grid._set_position((r, c), '🪺')
                    self.assertEqual(grid.level_state[r][c], '🪺')


    def test_find_eggs(self) -> None:
        """
        Tests the `_find_eggs` method of the Grid class.

        This test verifies that the _find_eggs method correctly identifies the positions
        of eggs in various grid level configurations.
        """

        # Test finding eggs in the grid
        self.assertEqual(self.grid1._find_eggs(), [(1, 2)])
        self.assertEqual(self.grid2._find_eggs(), [(1, 1)])
        self.assertEqual(self.grid3._find_eggs(), [(2, 3), (3, 3)])
        self.assertEqual(self.grid4._find_eggs(), [])
        self.assertEqual(self.grid5._find_eggs(), [])
        self.assertEqual(self.grid_cs11._find_eggs(), [(5, 7), (6, 7), (8, 7)])
        self.assertEqual(self.grid_labyrinth._find_eggs(), [(1, 1), (1, 2), (2, 1), (11, 4)])
        self.assertEqual(self.grid_sacrifice._find_eggs(), [(5, 7), (7, 6)])
        self.assertEqual(self.empty_grid._find_eggs(), [])

        # Eggs in corners
        grid1 = [
            '🥚🧱🧱🧱🥚',
            '🧱🟩🟩🟩🧱',
            '🧱🪹🥚🍳🧱',
            '🥚🧱🧱🧱🥚'
        ]
        grid2 = [
            '🥚🧱🧱🧱🥚',
            '🧱🟩🟩🟩🧱',
            '🧱🪹🟩🍳🧱',
            '🥚🧱🧱🧱🥚'
        ]
        self.assertEqual(game_utils.Grid(grid_data=(grid1, randint(1, 100)))._find_eggs(), [(0, 0), (0, 4), (2, 2), (3, 0), (3, 4)])
        self.assertEqual(game_utils.Grid(grid_data=(grid2, randint(1, 100)))._find_eggs(), [(0, 0), (0, 4), (3, 0), (3, 4)])
        
        # All eggs
        grid3 = [
            '🥚🥚',
            '🥚🥚'
        ]
        grid4 = [
            '🥚'*2**15,
        ]
        self.assertEqual(game_utils.Grid(grid_data=(grid3, randint(1, 100)))._find_eggs(), [(0, 0), (0, 1), (1, 0), (1, 1)])
        assertion_res = [(0, n) for n in range(2**15)]
        self.assertEqual(game_utils.Grid(grid_data=(grid4, randint(1, 100)))._find_eggs(), assertion_res)


    def test_clear_eggs(self) -> None:
        """
        Tests the `_clear_eggs` method of the `Grid` class.

        This test verifies that the `_clear_eggs` method correctly removes all egg
        symbols ('🥚') from various grid level configurations and updates the grid's
        level state accordingly.
        """
        # Test clearing eggs from the grid
        # Level design should not matter much for these tests as the objective
        # is to show that the function works.

        cleared_grid1 = [
                ['🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🟩', '🟩', '🟩', '🧱'],
                ['🧱', '🪹', '🟩', '🍳', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱']
            ]
        cleared_grid2 = [
                ['🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🟩', '🟩', '🟩', '🧱'],
                ['🧱', '🪹', '🍳', '🧱', '🧱'],
                ['🧱', '🪺', '🟩', '🍳', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱']
            ]
        cleared_grid3 = [
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🍳', '🟩', '🟩', '🍳', '🧱'],
                ['🧱', '🟩', '🟩', '🟩', '🪹', '🧱'],
                ['🧱', '🪺', '🧱', '🟩', '🪹', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱']
            ]
        cleared_grid4 = [
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🍳', '🟩', '🟩', '🍳', '🧱'],
                ['🧱', '🟩', '🪹', '🟩', '🟩', '🧱'],
                ['🧱', '🪺', '🟩', '🟩', '🪹', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱']
            ]
        cleared_grid5 = [
                ['🍳', '🧱', '🟩'],
                ['🧱', '🟩', '🟩'],
                ['🟩', '🍳', '🧱']
            ]
        cleared_grid_cs11 = [
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🪹", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🪹", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪹", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🪺", "🟩", "🟩", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🪺", "🧱"],
                ["🧱", "🪺", "🪺", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪺", "🪺", "🧱"],
                ["🧱", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🧱"]
            ]
        cleared_grid_labyrinth = [
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱"],
                ["🧱", "🟩", "🧱", "🍳", "🟩", "🧱", "🧱", "🍳", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪹", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🍳", "🧱", "🟩", "🍳", "🧱", "🧱", "🟩", "🟩", "🍳", "🧱", "🍳", "🟩", "🪹", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
            ]
        cleared_grid_sacrifice = [
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🟩", "🧱", "🟩", "🍳", "🧱", "🍳", "🟩", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🟩", "🪺", "🟩", "🟩", "🟩", "🟩", "🟩", "🪺", "🟩", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🪹", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🟩", "🧱", "🟩", "🧱", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
            ]

        for grid, cleared_grid in zip(
            [
                self.grid1, self.grid2, self.grid3, self.grid4, self.grid5,
                self.grid_cs11, self.grid_labyrinth, self.grid_sacrifice, self.empty_grid
            ],
            [
                cleared_grid1, cleared_grid2, cleared_grid3, cleared_grid4, cleared_grid5,
                cleared_grid_cs11, cleared_grid_labyrinth, cleared_grid_sacrifice, []
            ]
        ):
            grid._clear_eggs()
            self.assertFalse(grid.is_present('🥚'))
            self.assertEqual(grid.level_state, cleared_grid)
    
        grid_all_eggs = [
            '🥚'*2**15,
        ]*2**5
        grid = game_utils.Grid(grid_data=(grid_all_eggs, 2**10))
        grid._clear_eggs()
        self.assertFalse(grid.is_present('🥚'))

        # Create random levels (does not need to be valid) and see if the function `clear_eggs` works
        blocks = ['🧱', '🟩', '🥚', '🍳', '🪹', '🪺']
        for _ in range(10):
            rows = choice(range(4, 21)) # Random grid dimensions: 4x4 (smallest) to 20x20 (largest)
            cols = choice(range(4, 21))
            grid_data = []
            for _ in range(rows):
                row = ""
                for _ in range(cols):
                    row += choice(blocks)
                grid_data.append(row)
            grid = game_utils.Grid(grid_data=(grid_data, 5))
            grid._clear_eggs()
            self.assertFalse(grid.is_present('🥚'))


    def test_apply_move(self) -> None:
        """
        Tests the `_apply_move` method of the `Grid` class.

        This method tests that the snapshots (game frames) are correctly generated
        and tracked. It also verifies that the points earned (per frame) are correctly
        calculated.

        The difference between the `_apply_move` method and the `roll` method is that
        `_apply_move` checks the grid by frame, while the `roll` method makes use of `_apply_move`
        to simulate the complete movement of the eggs in the grid after a move is made.
        """

        max_moves = 1
        moves = [game_utils.Move('l')]
        grid1 = [
            '🧱🧱🧱🧱🧱',
            '🧱🟩🟩🟩🧱',
            '🧱🪹🥚🍳🧱',
            '🧱🧱🧱🧱🧱'
        ]
        grid1_obj = game_utils.Grid(grid_data=(grid1, max_moves))
        points, moved = grid1_obj._apply_move(moves[-1])
        # Verify that points were earned and movement occurred
        self.assertEqual(points, 11)  # Egg reached nest
        self.assertTrue(moved)

        max_moves = 314
        moves = [game_utils.Move('b')]
        grid2 = [
            '🧱🧱🧱🧱🧱',
            '🧱🥚🟩🥚🧱',
            '🧱🪹🍳🍳🧱',
            '🧱🪺🟩🍳🧱',
            '🧱🧱🧱🧱🧱'
        ]
        grid2_obj = game_utils.Grid(grid_data=(grid2, max_moves))
        points, moved = grid2_obj._apply_move(moves[-1])
        self.assertEqual(points, 319)  # One egg reached nest, another got cooked
        self.assertTrue(moved)
  
        max_moves = 15
        moves = [game_utils.Move('b'), game_utils.Move('b')]
        grid_cs11 = self.grid_cs11
        points, moved = grid_cs11._apply_move(moves[-1])
        self.assertEqual(points, 25) # 10 + 15 bonus points
        self.assertTrue(moved)

        moves = [game_utils.Move('l'), game_utils.Move('l')]
        grid_labyrinth_obj = self.grid_labyrinth
        points, moved = grid_labyrinth_obj._apply_move(moves[-1])
        self.assertEqual(points, 0)
        self.assertFalse(moved)

        # tilt the same grid rightwards
        moves = [game_utils.Move('l'), game_utils.Move('r')]
        points, moved = grid_labyrinth_obj._apply_move(moves[-1])
        self.assertEqual(points, 0)
        self.assertTrue(moved)

        # process next snapshot
        moves = [game_utils.Move('l'), game_utils.Move('r')]
        points, moved = grid_labyrinth_obj._apply_move(moves[-1])
        self.assertEqual(points, 0)
        self.assertTrue(moved)

        # process next snapshot
        moves = [game_utils.Move('l'), game_utils.Move('r')]
        points, moved = grid_labyrinth_obj._apply_move(moves[-1])
        self.assertEqual(points, 0)
        self.assertTrue(moved)

        max_moves = 15
        moves = [game_utils.Move('l'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('f')]
        grid_sacrifice = [
                '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱',
                '🧱🧱🧱🧱🟩🟩🟩🟩🟩🟩🟩🧱🧱🧱🧱',
                '🧱🧱🧱🟩🧱🟩🍳🧱🍳🟩🧱🥚🧱🧱🧱',
                '🧱🧱🧱🟩🟩🟩🟩🟩🟩🟩🟩🥚🧱🧱🧱',
                '🧱🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱🧱',
                '🧱🟩🟩🟩🟩🧱🧱🟩🧱🧱🟩🟩🟩🟩🧱',
                '🧱🟩🧱🟩🪺🟩🟩🟩🟩🟩🪺🟩🧱🟩🧱',
                '🧱🟩🟩🟩🟩🟩🟩🍳🪹🟩🟩🟩🟩🟩🧱',
                '🧱🟩🍳🟩🟩🟩🟩🟩🟩🟩🟩🟩🍳🟩🧱',
                '🧱🟩🧱🧱🟩🟩🧱🟩🧱🟩🟩🧱🧱🟩🧱',
                '🧱🟩🧱🟩🟩🟩🟩🧱🟩🟩🟩🟩🧱🟩🧱',
                '🧱🟩🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱🟩🧱',
                '🧱🟩🧱🟩🟩🧱🟩🟩🟩🧱🟩🟩🧱🟩🧱',
                '🧱🟩🟩🟩🟩🟩🍳🧱🍳🟩🟩🟩🟩🟩🧱',
                '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱'
        ]
        grid_sacrifice_obj = game_utils.Grid(grid_data=(grid_sacrifice, max_moves))
        points, moved = grid_sacrifice_obj._apply_move(moves[-1])
        self.assertEqual(points, 0)
        self.assertFalse(moved)

        # tilt the same grid backwards
        moves = [game_utils.Move('l'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('f'), game_utils.Move('r'), game_utils.Move('f'), game_utils.Move('b')]
        points, moved = grid_sacrifice_obj._apply_move(moves[-1])
        self.assertEqual(points, 0)
        self.assertTrue(moved)


    def test_calculate_new_position(self) -> None:
        """
        Tests the `_calculate_new_position` method of the `Grid` class.

        This method tests various scenarios for calculating the new position of an egg
        on the grid based on different moves. It checks the outcomes and new positions
        for different initial positions and moves, including edge cases where the egg
        moves outside the grid or encounters barriers.
        """

        # Note that like 'apply_move,' this function tests for egg movements in between snapshots.

        grid1_data = [
            '🧱🧱🧱🧱🧱',
            '🧱🟩🟩🟩🧱',
            '🧱🪹🥚🍳🧱',
            '🧱🧱🧱🧱🧱'
        ]
        grid1_obj = game_utils.Grid(grid_data=(grid1_data, 5))
   
        pos = (2, 2)
        move = game_utils.Move('r')
        outcome, new_pos = grid1_obj._calculate_new_position(pos, move)
        self.assertEqual(outcome, "fry")
        self.assertEqual(new_pos, pos) # new_pos is not updated when an egg moves to a frying pan

        pos = (2, 2)
        move = game_utils.Move('f')
        outcome, new_pos = grid1_obj._calculate_new_position(pos, move)
        self.assertEqual(outcome, "move")
        self.assertEqual(new_pos, (1, 2))

        pos = (2, 2)
        move = game_utils.Move('b')
        outcome, new_pos = grid1_obj._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos) # new_pos is not updated when an egg encounters a barrier (such as a wall)

        # Edge case: Egg moves outside the grid
        pos = (0, 0) # Suppose there is an egg at (0, 0)
        move = game_utils.Move('b')
        outcome, new_pos = grid1_obj._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos) # new_pos is not updated when an egg goes out of bounds
   
        move = game_utils.Move('l') # Tilt the grid leftward
        pos = (1, 1)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (1, 2)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos) # new_pos is not updated when an egg moves to another egg

        pos = (2, 1)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (11, 4)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        # Also test for random non-initial egg positions in the grid
        move = game_utils.Move('r') # Tilt the grid rightward
        pos = (1, 10)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (5, 12)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "fill_nest")
        self.assertEqual(new_pos, (5, 13))

        move = game_utils.Move('l') # Tilt the grid leftward
        pos = (1, 4)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "move")
        self.assertEqual(new_pos, (1, 3))

        pos = (7, 7)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "move")
        self.assertEqual(new_pos, (7, 6))

        # Edge case: Egg moves outside the grid
        move = game_utils.Move('f') # Tilt the grid forward
        pos = (0, 10)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (0, 3)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (0, 1)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (0, 4)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        # Also check for non-negative out of bound cell positions
        move = game_utils.Move('r') # Tilt the grid rightward
        pos = (3, 15)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (1, 15)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (4, 15)
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (1, 20) # Should not be possible
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (5, 2**10) # Should not be possible
        outcome, new_pos = self.grid_labyrinth._calculate_new_position(pos, move)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)
     

    def test_calculate_points(self) -> None:
        """
        Tests the `calculate_points` function of the game_utils module.

        This test method verifies that the calculate_points function correctly calculates
        the points based on the number of moves left. Adhering to the required game specifications,
        the points are calculated as follows:
        - The player is granted a base score of 10 points for each egg that reaches a nest.
        - The player is granted a bonus of 1 point for each move remaining (this includes the last move).
        """
        test_cases = [
            (1, 1, 11), (5, 5, 11), (10, 10, 11), (100000, 100000, 11),
            (15, 5, 21), (15, 7, 19), (15, 1, 25), (15, 10, 16),
            (50, 1, 60), (50, 25, 36), (50, 12, 49),
            (20, 5, 26), (30, 10, 31), (40, 20, 31),
            (100, 50, 61), (100, 75, 36), (999, 999, 11), (999, 1, 1009),
            (2**10, 2**5, 1003), (10**3, 10**2, 911), (2**15, 2**10, 31755),
            (10**4, 10**3, 9011), (10**6, 10**3, 999011), (2**20, 2**15, 1015819)
        ]
        moveset = [game_utils.Move('f'), game_utils.Move('b'), game_utils.Move('l'), game_utils.Move('r')]
        for max_moves, movecount, res in test_cases:
            moves = []
            for _ in range(movecount):
                moves.append(choice(moveset))
            self.assertEqual(game_utils.calculate_points(max_moves, moves), res)


if __name__ == "__main__":
    unittest.main()
