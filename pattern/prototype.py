# -*- coding: utf-8 -*-


class Monster(object):
    def __init__(self):
        pass

    def clone(self):
        pass


class Ghost(Monster):
    def __init__(self):
        super(Ghost, self).__init__()

    def clone(self):
        return Ghost()

    def __str__(self):
        return "Ghost"


class Spawner(object):
    """
    如何传递一个原型，C++有模板，
    """
    def __init__(self, prototype):
        self.prototype = prototype

    def spawn_monster(self):
        return self.prototype.clone()

if __name__ == '__main__':
    ghost = Ghost()
    ghost_spawner = Spawner(ghost)
    new_ghost = ghost_spawner.spawn_monster()
    print "ghost:", new_ghost