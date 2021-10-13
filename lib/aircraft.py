
from log import logger

class Aircraft:
    def __init__(self, code:str, name:str, role:str, year_start:int, year_end:int, costs:list):
        self.code  = code
        self.name  = name
        self.role  = role
        self.costs  = costs
        self.year_start = year_start
        self.year_end   = year_end

    def cost(self, length:str):
        labels = { 'short': 0, 'medium': 1, 'long': 2 }
        return self.costs[ labels[length] ]
