# encoding = utf-8


import random


class GameMap(object):

    CELL_ALIVE = 1
    CELL_DEAD = 0

    def __init__(self):
        object.__init__(self)
        self.rows = 100
        self.cols = 100
        self._map = []
        for r in range(self.rows):
            self._map.append([0] * self.cols)

        for r in range(self.rows):
            for c in range(self.cols):
                self._map[r][c] = 1 if not random.randint(0, 2) else 0

        # self._map[1][2] = 1
        # self._map[1][3] = 1
        # self._map[2][3] = 1
        # self._map[2][4] = 1

    def check_position_param(self, row, col):
        if row >= self.rows or col >= self.cols:
            raise ValueError('({row}, {col}) out of range.'.format(row=row, col=col))

    def get(self, row, col):
        """
        获取 row, col 指定的细胞的状态。
        :param
            row: int, row position，start from 0。
            col: int, column position, start from 0.
        :return:
            0: 如果细胞的状态是死的。
            1：如果细胞的状态是活的。
        """
        self.check_position_param(row, col)
        return self._map[row][col]

    def set(self, row, col, state):
        """
        set the cell's state to "state" whose position is specified by "row" and "col"
        :param
            row: int, row position，start from 0。
            col: int, column position, start from 0.
            state: 0 or 1, 1 represent alive while 0 represent dead.
        :return: None
        """
        self.check_position_param(row, col)
        self._map[row][col] = 1 if state else 0

    def get_around(self, row, col):
        """
        获取 row, col 指定的细胞周围的8个细胞中活细胞的个数。
        :param
            row: int 行位置。
        :param
            col: int 列位置。
        :return:
            int 范围从0到8。
        """
        self.check_position_param(row, col)

        DIRECTION = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1),
            'up_left': (-1, -1),
            'up_right': (-1, 1),
            'down_left': (1, -1),
            'down_right': (1, 1),
        }

        counter = 0
        for direc in DIRECTION:
            trow = (DIRECTION[direc][0] + row) % self.rows
            tcol = (DIRECTION[direc][1] + col) % self.cols
            counter += self._map[trow][tcol]

        return counter
