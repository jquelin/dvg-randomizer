
from dvg.logger import log

class Aircraft:
    def __init__(self, bg, box, service, name, year_in:int,
                 year_out:int, cost, role):
        self.boardgame = bg
        self.box = box
        self.service = service
        self.name = name
        self.year_in = year_in
        self.year_out = year_out
        self.cost = cost
        self.role = role

    def id(self):
        id = self.boardgame.alias
        for attribute in ['box', 'service', 'name']:
            id = id + '-' + getattr(self, attribute)
        return id

    def __repr__(self):
        return f'{self.id()} ({self.role}) [{self.year_in}-{self.year_out}]'


