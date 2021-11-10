
from dvg.logger import log

class Pilot:
    def __init__(self, bg, box, service, name, aircraft):
        self.boardgame = bg
        self.box       = box
        self.service   = service
        self.services  = service.split('+')
        self.name      = name
        self.aircraft  = aircraft

    def id(self):
        id = self.boardgame.alias
        for attribute in ['service', 'name']:
            id = id + '-' + getattr(self, attribute)
        return id


    def __repr__(self):
        return f'{self.id()} ({self.aircraft})'
