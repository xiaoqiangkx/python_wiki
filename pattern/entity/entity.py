# -*- coding: utf-8 -*-

from math3d.vector import Vector


class Entity(object):
    def __init__(self):
        self.position = Vector(0, 0, 0)

    def get_position(self):
        return self.position

    def jump(self):
        self.position += Vector(1, 0, 0)

    def undo(self):
        self.position -= Vector(1, 0, 0)
