import unittest

import gamemap
import game


class TestGameMap(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.map = None

    def display(self):
        print('\n'.join(map(str, self.map._map)))

    def test_gamemap_get_around(self):
        self.assertEqual(self.map.get_around(0, 0), 1)
        self.assertEqual(self.map.get_around(0, 1), 2)
        self.assertEqual(self.map.get_around(0, 2), 2)
        self.assertEqual(self.map.get_around(1, 0), 2)
        self.assertEqual(self.map.get_around(1, 1), 4)
        self.assertEqual(self.map.get_around(1, 2), 3)
        self.assertEqual(self.map.get_around(2, 0), 1)
        self.assertEqual(self.map.get_around(2, 1), 1)
        self.assertEqual(self.map.get_around(2, 2), 2)

    def test_check_position_param(self):
        self.assertRaises(ValueError, self.map.check_position_param, 3, 1)

    def test_gamemap_set(self):
        self.map.set(1, 1, 1)
        self.assertEqual(self.map.get(1, 1), 1)

    def test_gamemap_all(self):
        pass


class TestGame(unittest.TestCase):
    def test(self):
        life_game = game.Game()
        for i in range(life_game._gamemap.row):
            print(' '.join(map(str, life_game._gamemap._map[i])))
        print('*' * 10)
        print('(%d, %d) = %d' % (1, 2, life_game._gamemap.get_around(1, 2)))
        life_game.update()


        for i in range(life_game._gamemap.row):
            print(' '.join(map(str, life_game._gamemap._map[i])))

if __name__ == '__main__':
    test = TestGame()
    test.test()