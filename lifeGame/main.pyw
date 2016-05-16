# encoding=utf8

import sys

import clock
import game
from PyQt4 import QtGui

__author__ = 'davidlyu'


def main():
    qapp = QtGui.QApplication(sys.argv)

    life_game = game.Game()
    game_clock = clock.Clock(500)
    game_clock.set_game(life_game)
    game_clock.start()

    return qapp.exec_()


if __name__ == '__main__':
    sys.exit(main())
