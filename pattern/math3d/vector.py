# -*- coding: utf-8 -*-


class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iadd__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        self.z = self.z + other.z
        return self

    def __isub__(self, other):
        self.x = self.x - other.x
        self.y = self.y - other.y
        self.z = self.z - other.z
        return self

    @staticmethod
    def copy(vec):
        return Vector(vec.x, vec.y, vec.z)

    def __str__(self):
        return ",".join([str(self.x), str(self.y), str(self.z)])

    def __repr__(self):
        return ",".join([str(self.x), str(self.y), str(self.z)])