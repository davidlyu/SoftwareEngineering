# encoding=utf-8

from PyQt4 import QtCore


__author__ = 'davidlyu'


class Clock(QtCore.QObject):
    def __init__(self, interval):
        """
        initialize a clock
        :param
            interval: int, unit is millisecond.
        """
        QtCore.QObject.__init__(self)
        self.game = None
        self._interval = interval
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'),
                     self.update)

    def update(self):
        self.game.update()

    def start(self):
        self.timer.start(self._interval)

    def set_game(self, game):
        """
        设置一个游戏，时钟每隔指定的时间间隔，调用游戏的 update 方法更新游戏状态。
        :param
            game: Game 类的实例。
        :return: None
        """
        self.game = game
