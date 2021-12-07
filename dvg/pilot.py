
from dvg.logger import log

class Pilot:
    def __init__(self, bg, box, service, name, aircraft, elite):
        self.boardgame = bg
        self.box       = box
        self.service   = service
        self.services  = service.split('+')
        self.name      = name
        self.aircraft  = aircraft
        if elite != '':
            self.is_elite    = True
            self.elite_name  = f'\u2606 {name} \u2606'
            if '+' in elite:
                self.elite   = [int(s) for s in elite.split('+')]
            else:
                self.elite   = [0, int(elite)]
        else:
            self.is_elite    = False
            self.elite       = None
            self.elite_name  = name

    def id(self):
        id = self.boardgame.alias
        for attribute in ['service', 'name']:
            id = id + '-' + getattr(self, attribute)
        return id


    def __repr__(self):
        return f'{self.id()} ({self.aircraft})'

    def so_bonus(self, game):
        cl_level = game.clength.level
        if self.is_elite:
            so_cost = self.elite[0] + self.elite[1]*cl_level
        else:
            so_cost = self.aircraft.cost * cl_level

        # so_bonus = - so_cost
        return -so_cost

