
import json
import logging
import pkg_resources


def load_aircrafts(filepath):
    logging.info(f"reading {filepath}")
    aircrafts = []
    with open(filepath) as ifp:
        data = json.load(ifp)
    for a in data:
        (code, name, role, ystart, yend) = list(a)
        logging.debug(f"- found aircraft: {code} {name} ({role}) [{ystart}-{yend}]")
        newa = Aircraft(code=code, name=name, role=role,
                        year_start=ystart, year_end=yend)
        aircrafts.append(newa)
    logging.info(f"found {len(aircrafts)} aircrafts")
    return aircrafts

class Aircraft:
    def __init__(self, code:str, name:str, role:str, year_start:int, year_end:int):
        self.code  = code
        self.name  = name
        self.role  = role
        self.year_start = year_start
        self.year_end   = year_end  
