
import json
import logging
import pkg_resources


def load_campaigns(filepath):
    logging.info(f"reading {filepath}")
    campaigns = []
    with open(filepath) as ifp:
        data = json.load(ifp)
    for c in data:
        logging.debug(f"- found {c['name']} - ({c['year']})")
        newc = Campaign(name=c['name'], year=c['year'], level=c['level'])
        campaigns.append(newc)
    logging.info(f"found {len(campaigns)} campaigns")
    return campaigns


class Campaign:
    def __init__(self, name:str, year:int, level:int):
        self.name  = name
        self.year  = year
        self.level = level
