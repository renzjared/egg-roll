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

import unittest
from copy import deepcopy
from random import choice

import egg_roll
import game_utils
from egg_roll import GameState

class TestEggRoll(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.initial_grids = {
            "grid1": [
                ['🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🟩', '🥚', '🟩', '🧱'],
                ['🧱', '🪹', '🟩', '🍳', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱']
            ],
            "grid2": [
                ['🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🥚', '🟩', '🟩', '🧱'],
                ['🧱', '🪹', '🍳', '🧱', '🧱'],
                ['🧱', '🪺', '🟩', '🍳', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱']
            ],
            "grid3": [
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🍳', '🟩', '🟩', '🍳', '🧱'],
                ['🧱', '🟩', '🟩', '🥚', '🪹', '🧱'],
                ['🧱', '🪺', '🧱', '🥚', '🪹', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱']
            ],
            "grid4": [
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🍳', '🟩', '🟩', '🍳', '🧱'],
                ['🧱', '🟩', '🪹', '🟩', '🟩', '🧱'],
                ['🧱', '🪺', '🟩', '🟩', '🪹', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱']
            ],
            "grid5": [
                ['🍳', '🧱', '🟩'],
                ['🧱', '🟩', '🟩'],
                ['🟩', '🍳', '🧱']
            ],
            "grid_cs11": [
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🪹", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🥚", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🥚", "🟩", "🧱", "🧱", "🪹", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪹", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🥚", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🪺", "🟩", "🟩", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🪺", "🧱"],
                ["🧱", "🪺", "🪺", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪺", "🪺", "🧱"],
                ["🧱", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🍳", "🧱"]
            ],
            "grid_labyrinth": [
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🥚", "🥚", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱"],
                ["🧱", "🥚", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱"],
                ["🧱", "🟩", "🧱", "🍳", "🟩", "🧱", "🧱", "🍳", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪹", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🥚", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🍳", "🧱", "🟩", "🍳", "🧱", "🧱", "🟩", "🟩", "🍳", "🧱", "🍳", "🟩", "🪹", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
            ],
            "grid_sacrifice": [
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🟩", "🧱", "🟩", "🍳", "🧱", "🍳", "🟩", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🥚", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🟩", "🪺", "🟩", "🟩", "🟩", "🟩", "🟩", "🪺", "🟩", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🥚", "🍳", "🪹", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🟩", "🧱", "🟩", "🧱", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
            ],
            "empty_grid": [] # Edge case
        }


    def setUp(self):
        self.grid1 = deepcopy(self.initial_grids["grid1"])
        self.grid2 = deepcopy(self.initial_grids["grid2"])
        self.grid3 = deepcopy(self.initial_grids["grid3"])
        self.grid4 = deepcopy(self.initial_grids["grid4"])
        self.grid5 = deepcopy(self.initial_grids["grid5"])
        self.grid_cs11 = deepcopy(self.initial_grids["grid_cs11"])
        self.grid_labyrinth = deepcopy(self.initial_grids["grid_labyrinth"])
        self.grid_sacrifice = deepcopy(self.initial_grids["grid_sacrifice"])
        self.empty_grid = deepcopy(self.initial_grids["empty_grid"])

    def test_validate_moves(self):
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


    def test_validate_moves_invalid_characters(self):
        """Tests that invalid characters are filtered out."""
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


    def test_update_game_states(self):
        """Tests for when a user intends to restart the game"""
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
    def test_move_to_arrow(self):
        """Tests that all of the possible inputs return correct arrow symbol"""
        self.assertEqual(game_utils.move_to_arrow('f'), '↑')
        self.assertEqual(game_utils.move_to_arrow('F'), '↑')
        self.assertEqual(game_utils.move_to_arrow('b'), '↓')
        self.assertEqual(game_utils.move_to_arrow('B'), '↓')
        self.assertEqual(game_utils.move_to_arrow('l'), '←')
        self.assertEqual(game_utils.move_to_arrow('L'), '←')
        self.assertEqual(game_utils.move_to_arrow('r'), '→')
        self.assertEqual(game_utils.move_to_arrow('R'), '→')


    # We can guarantee that this function would not take invalid inputs.
    # We only test the four possible inputs.
    def test_directions(self):
        """Tests that all of the possible inputs return correct positional change values"""
        self.assertEqual(game_utils.directions('↑'), (-1, 0))
        self.assertEqual(game_utils.directions('↓'), (1, 0))
        self.assertEqual(game_utils.directions('←'), (0, -1))
        self.assertEqual(game_utils.directions('→'), (0, 1))


    def test_is_present(self):
        """Tests if an element is present in a grid"""
        # Just for assurance, we also test for characters that are not part of the game. (Example: 🍅)

        # Tests for grid1
        self.assertTrue(game_utils.is_present(self.grid1, '🥚'))
        self.assertTrue(game_utils.is_present(self.grid1, '🍳'))
        self.assertTrue(game_utils.is_present(self.grid1, '🪹'))
        self.assertTrue(game_utils.is_present(self.grid1, '🧱'))
        self.assertFalse(game_utils.is_present(self.grid1, '🪺'))
        self.assertFalse(game_utils.is_present(self.grid1, '🍅'))
        self.assertFalse(game_utils.is_present(self.grid1, '.'))
        self.assertFalse(game_utils.is_present(self.grid1, 'A'))
        self.assertFalse(game_utils.is_present(self.grid1, '5'))
        self.assertFalse(game_utils.is_present(self.grid1, '/'))


        # Tests for grid2
        self.assertTrue(game_utils.is_present(self.grid2, '🥚'))
        self.assertTrue(game_utils.is_present(self.grid2, '🍳'))
        self.assertTrue(game_utils.is_present(self.grid2, '🪹'))
        self.assertTrue(game_utils.is_present(self.grid2, '🪺'))
        self.assertTrue(game_utils.is_present(self.grid2, '🧱'))
        self.assertFalse(game_utils.is_present(self.grid2, '🟦'))
        self.assertFalse(game_utils.is_present(self.grid2, '🍅'))
        self.assertFalse(game_utils.is_present(self.grid2, '.'))
        self.assertFalse(game_utils.is_present(self.grid2, 'A'))
        self.assertFalse(game_utils.is_present(self.grid2, '5'))
        self.assertFalse(game_utils.is_present(self.grid2, '/'))

        # Tests for grid3
        self.assertTrue(game_utils.is_present(self.grid3, '🍳'))
        self.assertTrue(game_utils.is_present(self.grid3, '🪹'))
        self.assertTrue(game_utils.is_present(self.grid3, '🪺'))
        self.assertTrue(game_utils.is_present(self.grid3, '🥚'))
        self.assertTrue(game_utils.is_present(self.grid3, '🧱'))
        self.assertFalse(game_utils.is_present(self.grid3, '🟦'))
        self.assertFalse(game_utils.is_present(self.grid3, '🍅'))
        self.assertFalse(game_utils.is_present(self.grid3, '🟩🟩'))
        self.assertFalse(game_utils.is_present(self.grid3, '.'))
        self.assertFalse(game_utils.is_present(self.grid3, 'A'))
        self.assertFalse(game_utils.is_present(self.grid3, '5'))
        self.assertFalse(game_utils.is_present(self.grid3, '/'))

        # Tests for grid4
        self.assertTrue(game_utils.is_present(self.grid4, '🍳'))
        self.assertTrue(game_utils.is_present(self.grid4, '🪹'))
        self.assertTrue(game_utils.is_present(self.grid4, '🪺'))
        self.assertFalse(game_utils.is_present(self.grid4, '🥚'))
        self.assertFalse(game_utils.is_present(self.grid4, '🟦'))
        self.assertFalse(game_utils.is_present(self.grid4, '🍅'))
        self.assertFalse(game_utils.is_present(self.grid4, '🟩🟩'))
        self.assertFalse(game_utils.is_present(self.grid4, '.'))
        self.assertFalse(game_utils.is_present(self.grid4, 'A'))
        self.assertFalse(game_utils.is_present(self.grid4, '5'))
        self.assertFalse(game_utils.is_present(self.grid4, '/'))

        # Tests for grid5
        self.assertTrue(game_utils.is_present(self.grid5, '🍳'))
        self.assertTrue(game_utils.is_present(self.grid5, '🧱'))
        self.assertFalse(game_utils.is_present(self.grid5, '🥚'))
        self.assertFalse(game_utils.is_present(self.grid5, '🪹'))
        self.assertFalse(game_utils.is_present(self.grid5, '🪺'))
        self.assertFalse(game_utils.is_present(self.grid5, '🍅'))
        self.assertFalse(game_utils.is_present(self.grid5, '🟩🟩'))
        self.assertFalse(game_utils.is_present(self.grid5, '.'))
        self.assertFalse(game_utils.is_present(self.grid5, 'A'))
        self.assertFalse(game_utils.is_present(self.grid5, '5'))
        self.assertFalse(game_utils.is_present(self.grid5, '/'))

        # Tests for bonus level: CS 11
        self.assertTrue(game_utils.is_present(self.grid_cs11, '🍳'))
        self.assertTrue(game_utils.is_present(self.grid_cs11, '🧱'))
        self.assertTrue(game_utils.is_present(self.grid_cs11, '🥚'))
        self.assertTrue(game_utils.is_present(self.grid_cs11, '🪹'))
        self.assertTrue(game_utils.is_present(self.grid_cs11, '🪺'))
        self.assertFalse(game_utils.is_present(self.grid_cs11, '🍅'))
        self.assertFalse(game_utils.is_present(self.grid_cs11, '🟩🟩'))
        self.assertFalse(game_utils.is_present(self.grid_cs11, '.'))
        self.assertFalse(game_utils.is_present(self.grid_cs11, 'A'))
        self.assertFalse(game_utils.is_present(self.grid_cs11, '5'))
        self.assertFalse(game_utils.is_present(self.grid_cs11, '/'))

        # Tests for bonus level: Labyrinth
        self.assertTrue(game_utils.is_present(self.grid_labyrinth, '🍳'))
        self.assertTrue(game_utils.is_present(self.grid_labyrinth, '🧱'))
        self.assertTrue(game_utils.is_present(self.grid_labyrinth, '🥚'))
        self.assertTrue(game_utils.is_present(self.grid_labyrinth, '🪹'))
        self.assertFalse(game_utils.is_present(self.grid_labyrinth, '🪺'))
        self.assertFalse(game_utils.is_present(self.grid_labyrinth, '🍅'))
        self.assertFalse(game_utils.is_present(self.grid_labyrinth, '🟩🟩'))
        self.assertFalse(game_utils.is_present(self.grid_labyrinth, '.'))
        self.assertFalse(game_utils.is_present(self.grid_labyrinth, 'A'))
        self.assertFalse(game_utils.is_present(self.grid_labyrinth, '_labyrinth'))
        self.assertFalse(game_utils.is_present(self.grid_labyrinth, '/'))

        # Tests for bonus level: Sacrifice
        self.assertTrue(game_utils.is_present(self.grid_sacrifice, '🍳'))
        self.assertTrue(game_utils.is_present(self.grid_sacrifice, '🧱'))
        self.assertTrue(game_utils.is_present(self.grid_sacrifice, '🥚'))
        self.assertTrue(game_utils.is_present(self.grid_sacrifice, '🪹'))
        self.assertTrue(game_utils.is_present(self.grid_sacrifice, '🪺'))
        self.assertFalse(game_utils.is_present(self.grid_sacrifice, '🍅'))
        self.assertFalse(game_utils.is_present(self.grid_sacrifice, '🟩🟩'))
        self.assertFalse(game_utils.is_present(self.grid_sacrifice, '.'))
        self.assertFalse(game_utils.is_present(self.grid_sacrifice, 'A'))
        self.assertFalse(game_utils.is_present(self.grid_sacrifice, '5'))
        self.assertFalse(game_utils.is_present(self.grid_sacrifice, '/'))

        # Tests for an empty grid
        self.assertFalse(game_utils.is_present(self.empty_grid, '🧱'))
        self.assertFalse(game_utils.is_present(self.empty_grid, '🥚'))
        self.assertFalse(game_utils.is_present(self.empty_grid, '🟩'))
        self.assertFalse(game_utils.is_present(self.empty_grid, '🪹'))
        self.assertFalse(game_utils.is_present(self.empty_grid, '🪺'))
        self.assertFalse(game_utils.is_present(self.empty_grid, '🍅'))
        self.assertFalse(game_utils.is_present(self.empty_grid, '.'))
        self.assertFalse(game_utils.is_present(self.empty_grid, 'A'))
        self.assertFalse(game_utils.is_present(self.empty_grid, '5'))
        self.assertFalse(game_utils.is_present(self.empty_grid, '/'))


    def test_roll(self):
        # Test roll with grid configurations and moves
        # Only one move is tested (the move at the end of the tuple `moves`)
        moves = ['→']
        snapshots, points_earned = game_utils.roll(self.grid1, moves, 5)
        self.assertEqual(len(snapshots), 2)
        self.assertEqual(snapshots[0][1][3], '🟩')
        self.assertEqual(snapshots[1][1][3], '🥚')
        self.assertEqual(points_earned, 0)
 
        moves = ['←', '←', '←', '↓']
        snapshots, points_earned = game_utils.roll(self.grid2, moves, 5)
        self.assertEqual(len(snapshots), 2)
        self.assertEqual(snapshots[0][1][1], '🥚')
        self.assertEqual(snapshots[0][2][1], '🪹')
        self.assertEqual(snapshots[1][2][1], '🪺')
        self.assertEqual(snapshots[1][1][3], '🟩')
        self.assertEqual(snapshots[1][2][2], '🍳')
        self.assertEqual(points_earned, 12)

        moves = ['↓']
        snapshots, points_earned = game_utils.roll(self.grid_cs11, moves, 15)
        last = len(snapshots)-1
        self.assertEqual(len(snapshots), 7)
        self.assertEqual(snapshots[last][0][7], '🧱')
        self.assertEqual(snapshots[last][1][7], '🟩')
        self.assertEqual(snapshots[last][4][7], '🟩')
        self.assertEqual(snapshots[last][5][7], '🟩')
        self.assertEqual(snapshots[last][6][7], '🥚')
        self.assertEqual(snapshots[last][7][7], '🪺')
        self.assertEqual(snapshots[last][8][7], '🟩')
        self.assertEqual(snapshots[last][13][7], '🟩')
        self.assertEqual(snapshots[last][14][7], '🍳')
        self.assertEqual(points_earned, 20)
        self.assertTrue(game_utils.is_present(snapshots[last], '🥚'))

        grid_sacrifice = [
            ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
            ["🧱", "🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱", "🧱"],
            ["🧱", "🧱", "🧱", "🟩", "🧱", "🟩", "🍳", "🧱", "🍳", "🟩", "🧱", "🥚", "🧱", "🧱", "🧱"],
            ["🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🥚", "🧱", "🧱", "🧱"],
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
        # Test for when all eggs are unable to move
        moves = ['←', '↑', '→', '↑', '→', '↑']
        snapshots, points_earned = game_utils.roll(grid_sacrifice, moves, 15)
        last = len(snapshots)-1
        self.assertEqual(len(snapshots), 1)
        self.assertEqual(snapshots[last][2][11], '🥚') # Eggs stay in their current positions
        self.assertEqual(snapshots[last][3][11], '🥚')
        self.assertEqual(points_earned, 0)
        self.assertTrue(game_utils.is_present(snapshots[last], '🥚'))

        # Test if eggs do not merge into each other when colliding after being in motion
        moves = ['←', '↑', '→', '↑', '→', '↓']
        snapshots, points_earned = game_utils.roll(grid_sacrifice, moves, 15)
        last = len(snapshots)-1
        self.assertEqual(snapshots[last][2][11], '🟩')
        self.assertEqual(snapshots[last][3][11], '🟩')
        self.assertEqual(snapshots[last][7][11], '🥚')
        self.assertEqual(snapshots[last][8][11], '🥚')
        self.assertEqual(points_earned, 0)
        self.assertTrue(game_utils.is_present(snapshots[last], '🥚'))

        moves = ['←', '↑', '→', '↑', '→', '↓', '←']
        snapshots, points_earned = game_utils.roll(grid_sacrifice, moves, 15)
        last = len(snapshots)-1
        self.assertEqual(snapshots[last][7][11], '🟩')
        self.assertEqual(snapshots[last][8][11], '🟩')
        self.assertEqual(snapshots[last][7][8], '🪺')
        self.assertEqual(points_earned, 14)
        self.assertFalse(game_utils.is_present(snapshots[last], '🥚'))


    def test_apply_move(self):
        # Test applying moves to a grid
        max_moves = 1
        moves = []
        direction = (0, -1)
        grid1 = [
            ['🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🟩', '🟩', '🟩', '🧱'],
            ['🧱', '🪹', '🥚', '🍳', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱']
        ]
        points, moved = game_utils.apply_move(grid1, direction, max_moves, moves)
        # Verify that points were earned and movement occurred
        self.assertEqual(points, 11)  # Egg reached nest
        self.assertTrue(moved)

        max_moves = 314
        moves = []
        direction = (1, 0)
        grid2 = [
            ['🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🥚', '🟩', '🥚', '🧱'],
            ['🧱', '🪹', '🍳', '🍳', '🧱'],
            ['🧱', '🪺', '🟩', '🍳', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱']
        ]
        points, moved = game_utils.apply_move(grid2, direction, max_moves, moves)
        self.assertEqual(points, 319)  # One egg reached nest, another got cooked
        self.assertTrue(moved)

        max_moves = 15
        moves = ['↓']
        direction = (1, 0)
        points, moved = game_utils.apply_move(self.grid_cs11, direction, max_moves, moves)
        self.assertEqual(points, 25) # 10 + 15 bonus points (note that 'apply_move' only tracks changes per snapshot)
        self.assertTrue(moved)

        max_moves = 15
        moves = ['←']
        direction = (0, -1)
        grid_labyrinth = [
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
                ["🧱", "🥚", "🥚", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱"],
                ["🧱", "🥚", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱"],
                ["🧱", "🟩", "🧱", "🍳", "🟩", "🧱", "🧱", "🍳", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪹", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
                ["🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🧱", "🟩", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🧱", "🟩", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🥚", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🧱", "🧱", "🧱"],
                ["🧱", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
                ["🧱", "🍳", "🧱", "🟩", "🍳", "🧱", "🧱", "🟩", "🟩", "🍳", "🧱", "🍳", "🟩", "🪹", "🧱"],
                ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
            ]
        points, moved = game_utils.apply_move(grid_labyrinth, direction, max_moves, moves)
        self.assertEqual(points, 0)
        self.assertFalse(moved)

        # tilt the same grid rightwards
        moves = ['←', '→']
        direction = (0, 1)
        points, moved = game_utils.apply_move(grid_labyrinth, direction, max_moves, moves)
        self.assertEqual(points, 0)
        self.assertTrue(moved)

        # process next snapshot
        moves = ['←', '→']
        direction = (0, 1)
        points, moved = game_utils.apply_move(grid_labyrinth, direction, max_moves, moves)
        self.assertEqual(points, 0)
        self.assertTrue(moved)

        # process next snapshot
        moves = ['←', '→']
        direction = (0, 1)
        points, moved = game_utils.apply_move(grid_labyrinth, direction, max_moves, moves)
        self.assertEqual(points, 0)
        self.assertTrue(moved)

        max_moves = 15
        moves = ['←', '↑', '→', '↑', '→', '↑']
        direction = (-1, 0)
        grid_sacrifice = [
            ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
            ["🧱", "🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱", "🧱"],
            ["🧱", "🧱", "🧱", "🟩", "🧱", "🟩", "🍳", "🧱", "🍳", "🟩", "🧱", "🥚", "🧱", "🧱", "🧱"],
            ["🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🥚", "🧱", "🧱", "🧱"],
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
        points, moved = game_utils.apply_move(grid_sacrifice, direction, max_moves, moves)
        self.assertEqual(points, 0)
        self.assertFalse(moved)

        # tilt the same grid backwards
        moves = ['←', '↑', '→', '↑', '→', '↑', '↓']
        direction = (1, 0)
        points, moved = game_utils.apply_move(grid_sacrifice, direction, max_moves, moves)
        self.assertEqual(points, 0)
        self.assertTrue(moved)


    def test_find_eggs(self):
        # Test finding eggs in the grid
        eggs = game_utils.find_eggs(self.grid1)
        self.assertEqual(eggs, [(1, 2)])
        eggs = game_utils.find_eggs(self.grid2)
        self.assertEqual(eggs, [(1, 1)])
        eggs = game_utils.find_eggs(self.grid3)
        self.assertEqual(eggs, [(2, 3), (3, 3)])
        eggs = game_utils.find_eggs(self.grid4)
        self.assertEqual(eggs, [])
        eggs = game_utils.find_eggs(self.grid5)
        self.assertEqual(eggs, [])
        eggs = game_utils.find_eggs(self.grid_cs11)
        self.assertEqual(eggs, [(5, 7), (6, 7), (8, 7)])
        eggs = game_utils.find_eggs(self.grid_labyrinth)
        self.assertEqual(eggs, [(1, 1), (1, 2), (2, 1), (11, 4)])
        eggs = game_utils.find_eggs(self.grid_sacrifice)
        self.assertEqual(eggs, [(5, 7), (7, 6)])
        eggs = game_utils.find_eggs(self.empty_grid)
        self.assertEqual(eggs, [])

        # Eggs in corners
        grid1 = [
            ['🥚', '🧱', '🧱', '🧱', '🥚'],
            ['🧱', '🟩', '🟩', '🟩', '🧱'],
            ['🧱', '🪹', '🥚', '🍳', '🧱'],
            ['🥚', '🧱', '🧱', '🧱', '🥚']
        ]
        eggs = game_utils.find_eggs(grid1)
        self.assertEqual(eggs, [(0, 0), (0, 4), (2, 2), (3, 0), (3, 4)])

        grid2 = [
            ['🥚', '🧱', '🧱', '🧱', '🥚'],
            ['🧱', '🟩', '🟩', '🟩', '🧱'],
            ['🧱', '🪹', '🟩', '🍳', '🧱'],
            ['🥚', '🧱', '🧱', '🧱', '🥚']
        ]
        eggs = game_utils.find_eggs(grid2)
        self.assertEqual(eggs, [(0, 0), (0, 4), (3, 0), (3, 4)])

        # All eggs
        grid3 = [
            ['🥚', '🥚'],
            ['🥚', '🥚'],
        ]
        eggs = game_utils.find_eggs(grid3)
        self.assertEqual(eggs, [(0, 0), (0, 1), (1, 0), (1, 1)])

        grid4 = [
            ['🥚']*2**15,
        ]
        eggs = game_utils.find_eggs(grid4)
        assertion_res = [(0, n) for n in range(2**15)]
        self.assertEqual(eggs, assertion_res)

    def test_clear_eggs(self):
        # Test clearing eggs from the grid
        # Level design should not matter much for these tests as the objective
        # is to show that the function works.

        cleared_grid1 = [
                ['🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🟩', '🟩', '🟩', '🧱'],
                ['🧱', '🪹', '🟩', '🍳', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱']
            ]
        game_utils.clear_eggs(self.grid1)
        self.assertFalse(game_utils.is_present(self.grid1, '🥚'))
        self.assertEqual(self.grid1, cleared_grid1)

        cleared_grid2 = [
                ['🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🟩', '🟩', '🟩', '🧱'],
                ['🧱', '🪹', '🍳', '🧱', '🧱'],
                ['🧱', '🪺', '🟩', '🍳', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱']
            ]
        game_utils.clear_eggs(self.grid2)
        self.assertFalse(game_utils.is_present(self.grid2, '🥚'))
        self.assertEqual(self.grid2, cleared_grid2)

        cleared_grid3 = [
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🍳', '🟩', '🟩', '🍳', '🧱'],
                ['🧱', '🟩', '🟩', '🟩', '🪹', '🧱'],
                ['🧱', '🪺', '🧱', '🟩', '🪹', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱']
            ]
        game_utils.clear_eggs(self.grid3)
        self.assertFalse(game_utils.is_present(self.grid3, '🥚'))
        self.assertEqual(self.grid3, cleared_grid3)

        cleared_grid4 = [
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🍳', '🟩', '🟩', '🍳', '🧱'],
                ['🧱', '🟩', '🪹', '🟩', '🟩', '🧱'],
                ['🧱', '🪺', '🟩', '🟩', '🪹', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱']
            ]
        game_utils.clear_eggs(self.grid4)
        self.assertFalse(game_utils.is_present(self.grid4, '🥚'))
        self.assertEqual(self.grid4, cleared_grid4)

        cleared_grid5 = [
                ['🍳', '🧱', '🟩'],
                ['🧱', '🟩', '🟩'],
                ['🟩', '🍳', '🧱']
            ]
        game_utils.clear_eggs(self.grid5)
        self.assertFalse(game_utils.is_present(self.grid5, '🥚'))
        self.assertEqual(self.grid5, cleared_grid5)

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
        game_utils.clear_eggs(self.grid_cs11)
        self.assertFalse(game_utils.is_present(self.grid_cs11, '🥚'))
        self.assertEqual(self.grid_cs11, cleared_grid_cs11)

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
        game_utils.clear_eggs(self.grid_labyrinth)
        self.assertFalse(game_utils.is_present(self.grid_labyrinth, '🥚'))
        self.assertEqual(self.grid_labyrinth, cleared_grid_labyrinth)

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
        game_utils.clear_eggs(self.grid_sacrifice)
        self.assertFalse(game_utils.is_present(self.grid_sacrifice, '🥚'))
        self.assertEqual(self.grid_sacrifice, cleared_grid_sacrifice)

        empty_grid = []
        game_utils.clear_eggs(empty_grid)
        self.assertFalse(game_utils.is_present(empty_grid, '🥚'))
        self.assertEqual(empty_grid, [])

        grid_all_eggs = [
            ['🥚']*2**15,
        ]*2**5
        game_utils.clear_eggs(grid_all_eggs)
        self.assertFalse(game_utils.is_present(grid_all_eggs, '🥚'))

        # Create random levels (does not need to be valid) and see if the function `clear_eggs` works
        blocks = ['🧱', '🟩', '🥚', '🍳', '🪹', '🪺']
        for _ in range(10):
            rows = choice(range(4, 21)) # Random grid dimensions: 4x4 (smallest) to 20x20 (largest)
            cols = choice(range(4, 21))
            grid = []
            for _ in range(rows):
                row = []
                for _ in range(cols):
                    row.append(choice(blocks))
                grid.append(row)
            game_utils.clear_eggs(grid)
            self.assertFalse(game_utils.is_present(grid, '🥚'))


    def test_calculate_new_position(self):
        # Note that like 'apply_move,' this function tests for egg movements in between snapshots.

        grid1 = [
            ['🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🟩', '🟩', '🟩', '🧱'],
            ['🧱', '🪹', '🥚', '🍳', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱']
        ]
        pos = (2, 2)
        direction = (0, 1) # Tilt the grid rightward
        outcome, new_pos = game_utils.calculate_new_position(grid1, pos, direction)
        self.assertEqual(outcome, "fry")
        self.assertEqual(new_pos, pos) # new_pos is not updated when an egg moves to a frying pan

        pos = (2, 2)
        direction = (-1, 0) # Tilt the grid forward
        outcome, new_pos = game_utils.calculate_new_position(grid1, pos, direction)
        self.assertEqual(outcome, "move")
        self.assertEqual(new_pos, (1, 2))

        pos = (2, 2)
        direction = (1, 0) # Tilt the grid backward
        outcome, new_pos = game_utils.calculate_new_position(grid1, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos) # new_pos is not updated when an egg encounters a barrier (such as a wall)

        # Edge case: Egg moves outside the grid
        pos = (0, 0) # Suppose there is an egg in (0, 0)
        direction = (1, 0) # Tilt the grid backward
        outcome, new_pos = game_utils.calculate_new_position(grid1, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos) # new_pos is not updated when an egg goes out of bounds

        direction = (0, -1) # Tilt the grid leftward
        pos = (1, 1)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (1, 2)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos) # new_pos is not updated when an egg moves to another egg

        pos = (2, 1)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (11, 4)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        # Also test for random non-initial egg positions in the grid
        direction = (0, 1) # Tilt the grid rightward
        pos = (1, 10)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (5, 12)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "fill_nest")
        self.assertEqual(new_pos, (5, 13))

        direction = (0, -1) # Tilt the grid leftward
        pos = (1, 4)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "move")
        self.assertEqual(new_pos, (1, 3))

        pos = (7, 7)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "move")
        self.assertEqual(new_pos, (7, 6))

        # Edge case: Egg moves outside the grid
        direction = (-1, 0) # Tilt the grid forward
        pos = (0, 10)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (0, 3)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (0, 1)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (0, 4)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        # Also check for non-negative out of bound cell positions
        direction = (0, 1) # Tilt the grid rightward
        pos = (3, 15)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (1, 15)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (4, 15)
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (1, 20) # Should not be possible
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)

        pos = (5, 2**10) # Should not be possible
        outcome, new_pos = game_utils.calculate_new_position(self.grid_labyrinth, pos, direction)
        self.assertEqual(outcome, "reset")
        self.assertEqual(new_pos, pos)
        

    def test_calculate_points(self):
        test_cases = [
            (1, 1, 11), (5, 5, 11), (10, 10, 11), (100000, 100000, 11),
            (15, 5, 21), (15, 7, 19), (15, 1, 25), (15, 10, 16),
            (50, 1, 60), (50, 25, 36), (50, 12, 49),
            (20, 5, 26), (30, 10, 31), (40, 20, 31),
            (100, 50, 61), (100, 75, 36), (999, 999, 11), (999, 1, 1009),
            (2**10, 2**5, 1003), (10**3, 10**2, 911), (2**15, 2**10, 31755),
            (10**4, 10**3, 9011), (10**6, 10**3, 999011), (2**20, 2**15, 1015819)
        ]
        arrows = ['↑', '↓', '←', '→']
        for max_moves, movecount, res in test_cases:
            moves = []
            for _ in range(movecount):
                moves.append(choice(arrows))
            self.assertEqual(game_utils.calculate_points(max_moves, moves), res)


    def test_set_position(self):
        """Test setting each cell as an egg and a filled nest"""
        grids = [self.grid1, self.grid2, self.grid3, self.grid4, self.grid5, self.grid_cs11, self.grid_labyrinth, self.grid_sacrifice]

        # This is actually not possible when playing a game level. (Eggs cannot pass through 'solid' objects such as walls)
        # The objective of this test is to verify that the function
        # is able to properly change the value of a particular cell in the grid.
        for grid in grids:
            for r, row in enumerate(grid):
                for c, _ in enumerate(row):
                    game_utils.set_position(grid, (r, c), '🥚')
                    self.assertEqual(grid[r][c], '🥚')
                    game_utils.set_position(grid, (r, c), '🪺')
                    self.assertEqual(grid[r][c], '🪺')


if __name__ == "__main__":
    unittest.main()
