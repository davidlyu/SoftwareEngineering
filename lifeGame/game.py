# encoding = utf-8

import gamemap
import gui

__author__ = 'davidlyu'


class Game(object):
    def __init__(self):
        object.__init__(self)
        self._gamemap = gamemap.GameMap()
        self.gui = gui.Window(self._gamemap._map)
        self.gui.show()
        self.born = 3
        self.live = 2

    def update(self):
        """
        update the map state, called by clock
        :return: None
        """
        new_map = []
        for i in range(self._gamemap.rows):
            new_map.append([0] * self._gamemap.cols)

        for r in range(self._gamemap.rows):
            for c in range(self._gamemap.cols):
                if self._gamemap.get_around(r, c) == self.born:
                    new_map[r][c] = 1
                elif self._gamemap.get_around(r, c) == self.live:
                    new_map[r][c] = self._gamemap.get(r, c)
                else:
                    new_map[r][c] = 0
        self._gamemap._map = new_map
        self.gui.draw(self._gamemap._map)
