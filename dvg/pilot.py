
from aircraft import Aircraft
from log      import logger

class Pilot:
    def __init__(self, name:str, aircraft:Aircraft, box:str):
        self.name     = name
        self.aircraft = aircraft
        self.box      = box
