# -*- coding: utf-8 -*-


class Subject(object):
    def __init__(self):
        self.observer_ = []

    def notify(self, entity, event):
        for observer in self.observer_:
            observer.on_notify(entity, event)

    def add_observer(self, observer):
        if observer not in self.observer_:
            self.observer_.append(observer)

    def remove_observer(self, observer):
        if observer in self.observer_:
            self.observer_.remove(observer)


class Observer(object):
    def __init__(self):
        pass

    def on_notify(self, entity, event):
        print "entity:{0}, event:{1}".format(entity, event)


class Achievement(Observer):
    def __init__(self):
        super(Achievement, self).__init__()

    def on_notify(self, entity, event):
        print "Achievement,entity:{0}, event:{1}".format(entity, event)


class Physics(Subject):
    def __init__(self, entity):
        super(Physics, self).__init__()
        self.entity = entity

    def update_entity(self):
        self.notify(self.entity, 1)

if __name__ == '__main__':
    from entity.player import Player
    player = Player()
    physics = Physics(player)
    physics.add_observer(Achievement())
    physics.update_entity()
