# -*- coding: utf-8 -*-
import random


class OrcRace(object):
    def __init__(self):
        pass

    def __str__(self):
        return "OrcRace"


class ElfRace(object):
    def __init__(self):
        pass

    def __str__(self):
        return "ElfRace"


class World(object):
    def __init__(self):
        self.orc_race = OrcRace()
        self.elf_race = ElfRace()
        self.race_list = []

    def init_map(self):
        race_map = {1: self.orc_race, 2: self.elf_race}
        for i in xrange(10):
            race = random.randint(1, 2)
            self.race_list.append(race_map[race])

    def __str__(self):
        return " ".join([str(race) for race in self.race_list])
if __name__ == '__main__':
    world = World()
    world.init_map()
    print world