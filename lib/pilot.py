
import logging
from aircraft import Aircraft

class Pilot:
    def __init__(self, name:str, aircraft:Aircraft):
        self.name     = name
        self.aircraft = aircraft
