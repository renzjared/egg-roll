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
import egg_roll
import game_utils

from egg_roll import GameState

class TestEggRoll(unittest.TestCase):

    def test_validate_moves(self):
        """Tests that valid moves are accepted"""
        self.assertEqual(egg_roll.validate_moves('f', 5), 'f')
        self.assertEqual(egg_roll.validate_moves('Bl', 3), 'Bl')
        self.assertEqual(egg_roll.validate_moves('l', 5), 'l')
        self.assertEqual(egg_roll.validate_moves('R', 1), 'R')
        self.assertEqual(egg_roll.validate_moves('lllll', 5), 'lllll')


    def test_validate_moves_exactly_remaining_moves(self):
        """Tests that valid moves equal to remaining moves are accepted."""
        self.assertEqual(egg_roll.validate_moves('LRFB', 4), 'LRFB')
        self.assertEqual(egg_roll.validate_moves('lRrB', 4), 'lRrB')
        self.assertEqual(egg_roll.validate_moves('FB', 2), 'FB')
        self.assertEqual(egg_roll.validate_moves('Bb', 2), 'Bb')
        self.assertEqual(egg_roll.validate_moves('f', 1), 'f')


    def test_validate_moves_empty_moveset(self):
        """Tests sthat an empty moveset returns an empty string."""
        self.assertEqual(egg_roll.validate_moves('', 5), '')
        self.assertEqual(egg_roll.validate_moves('', 0), '')
        self.assertEqual(egg_roll.validate_moves('', 2048), '')
        self.assertEqual(egg_roll.validate_moves('', 31415926535), '')
        self.assertEqual(egg_roll.validate_moves('', -11235813), '')
        self.assertEqual(egg_roll.validate_moves('', -31415926535), '')


    def test_validate_moves_exceeds_remaining_moves(self):
        """Tests that moves exceeding remaining moves are truncated."""
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
        # Tests if an element is present in a grid
        grid1 = [
            ['🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🟩', '🥚', '🟩', '🧱'],
            ['🧱', '🪹', '🟩', '🍳', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱']
        ]

        grid2 = [
            ['🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🥚', '🟩', '🟩', '🧱'],
            ['🧱', '🪹', '🍳', '🧱', '🧱'],
            ['🧱', '🪺', '🟩', '🍳', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱']
        ]

        grid3 = [
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🍳', '🟩', '🟩', '🍳', '🧱'],
            ['🧱', '🟩', '🟩', '🥚', '🪹', '🧱'],
            ['🧱', '🪺', '🧱', '🥚', '🪹', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱']
        ]

        grid4 = [
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🍳', '🟩', '🟩', '🍳', '🧱'],
            ['🧱', '🟩', '🪹', '🟩', '🟩', '🧱'],
            ['🧱', '🪺', '🟩', '🟩', '🪹', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱']
        ]

        grid5 = [
            ['🍳', '🧱', '🟩'],
            ['🧱', '🟩', '🟩'],
            ['🟩', '🍳', '🧱']
        ]

        # Edge case: Empty grid
        empty_grid = []

        # Tests for grid1
        self.assertTrue(game_utils.is_present(grid1, '🥚'))
        self.assertTrue(game_utils.is_present(grid1, '🍳'))
        self.assertTrue(game_utils.is_present(grid1, '🪹'))
        self.assertTrue(game_utils.is_present(grid1, '🧱'))
        self.assertFalse(game_utils.is_present(grid1, '🪺'))
        self.assertFalse(game_utils.is_present(grid1, '🍅'))

        # Tests for grid2
        self.assertTrue(game_utils.is_present(grid2, '🥚'))
        self.assertTrue(game_utils.is_present(grid2, '🍳'))
        self.assertTrue(game_utils.is_present(grid2, '🪹'))
        self.assertTrue(game_utils.is_present(grid2, '🪺'))
        self.assertTrue(game_utils.is_present(grid2, '🧱'))
        self.assertFalse(game_utils.is_present(grid2, '🟦'))
        self.assertFalse(game_utils.is_present(grid2, '🍅'))

        # Tests for grid3
        self.assertTrue(game_utils.is_present(grid3, '🍳'))
        self.assertTrue(game_utils.is_present(grid3, '🪹'))
        self.assertTrue(game_utils.is_present(grid3, '🪺'))
        self.assertTrue(game_utils.is_present(grid3, '🥚'))
        self.assertTrue(game_utils.is_present(grid3, '🧱'))
        self.assertFalse(game_utils.is_present(grid3, '🟦'))
        self.assertFalse(game_utils.is_present(grid3, '🍅'))
        self.assertFalse(game_utils.is_present(grid3, '🟩🟩'))

        # Tests for grid4
        self.assertTrue(game_utils.is_present(grid4, '🍳'))
        self.assertTrue(game_utils.is_present(grid4, '🪹'))
        self.assertTrue(game_utils.is_present(grid4, '🪺'))
        self.assertFalse(game_utils.is_present(grid4, '🥚'))
        self.assertFalse(game_utils.is_present(grid4, '🟦'))
        self.assertFalse(game_utils.is_present(grid4, '🍅'))
        self.assertFalse(game_utils.is_present(grid4, '🟩🟩'))

        # Tests for grid5
        self.assertTrue(game_utils.is_present(grid5, '🍳'))
        self.assertTrue(game_utils.is_present(grid5, '🧱'))
        self.assertFalse(game_utils.is_present(grid5, '🥚'))
        self.assertFalse(game_utils.is_present(grid5, '🪹'))
        self.assertFalse(game_utils.is_present(grid5, '🪺'))
        self.assertFalse(game_utils.is_present(grid5, '🍅'))
        self.assertFalse(game_utils.is_present(grid5, '🟩🟩'))

        # Tests for an empty grid
        self.assertFalse(game_utils.is_present(empty_grid, '🥚'))
        self.assertFalse(game_utils.is_present(empty_grid, '🟩'))
        self.assertFalse(game_utils.is_present(empty_grid, '🍅'))


    def test_roll(self):
        # Test roll with grid configurations and moves
        grid = [['🥚', '🟩', '🪹'],
                ['🟩', '🍳', '🟩']]
        moves = ['↑', '→']
        snapshots, points = game_utils.roll(grid, moves, 5)

        self.assertEqual(len(snapshots), 3)
        self.assertEqual(snapshots[1][0][0], '🟩')  # Egg has moved
        self.assertEqual(points, 14)                # Egg reached nest, earned points (10 + 5 - 1)


    def test_apply_move(self):
        # Test applying moves to a grid
        grid = [['🟩', '🥚', '🪹'],
                ['🟩', '🍳', '🟩']]
        direction = (0, 1)
        points, moved = game_utils.apply_move(grid, direction, max_moves=1, moves=['f'])
       
        # Verify that points were earned and movement occurred
        self.assertEqual(points, 11)  # Egg reached nest
        self.assertTrue(moved)


    def test_find_eggs(self):
        # Test finding eggs in the grid
        grid = [['🥚', '🟩'],
                ['🪹', '🥚']]
        eggs = game_utils.find_eggs(grid)
        self.assertEqual(eggs, [(0, 0), (1, 1)])  # Egg positions


    def test_clear_eggs(self):
        # Test clearing eggs from the grid
        grid = [['🥚', '🟩'],
                ['🪹', '🥚']]
        game_utils.clear_eggs(grid)
        self.assertEqual(grid, [['🟩', '🟩'], ['🪹', '🟩']])  # Eggs removed

if __name__ == "__main__":
    unittest.main()

