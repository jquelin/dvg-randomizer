
from dvg.logger import log

class Aircraft:
    def __init__(self, bg, box, service, name, year_in:int,
                 year_out:int, cost, role):
        self.boardgame = bg
        self.box       = box
        self.service   = service
        self.services  = service.split('+')
        self.name      = name
        self.year_in   = int(year_in)
        self.year_out  = int(year_out) if year_out else 9999
        self.cost      = int(cost)
        self.role      = role

    def id(self):
        # box should not be part of id, since a core aircraft can be
        # reused from other expansions.
        id = self.boardgame.alias
        for attribute in ['service', 'name']:
            id = id + '-' + getattr(self, attribute)
        return id

    def __repr__(self):
        return f'{self.id()} ({self.role}) [{self.year_in}-{self.year_out}]'


