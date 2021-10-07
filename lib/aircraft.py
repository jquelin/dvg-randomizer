
import json
import logging
import pkg_resources


def load_aircrafts(filepath):
    logging.info(f"reading {filepath}")
    aircrafts = []
    with open(filepath) as ifp:
        data = json.load(ifp)
    for a in data:
        (code, name, role, ystart, yend, costs) = list(a)
        logging.debug(f"- found aircraft: {code} {name} ({role}) [{ystart}-{yend}] {costs}")
        newa = Aircraft(code=code, name=name, role=role,
                        year_start=ystart, year_end=yend, costs=costs)
        aircrafts.append(newa)
    logging.info(f"found {len(aircrafts)} aircrafts")
    return aircrafts

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
