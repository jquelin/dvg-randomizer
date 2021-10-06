
import json
import logging
import pkg_resources


def load_campaigns(filepath):
    logging.info(f"reading {filepath}")
    campaigns = []
    with open(filepath) as ifp:
        data = json.load(ifp)
    for c in data:
        name = c['name']
        year = c['year']
        level   = c['level']
        lengths = c['lengths']
        logging.debug(f"- found {name} - ({year})")
        newc = Campaign(name=name, year=year,
                        level=level, lengths=lengths)
        campaigns.append(newc)
    logging.info(f"found {len(campaigns)} campaigns")
    return campaigns

class CampaignLength:
    def __init__(self, days:int, so:int, label:str, squad:list):
        self.days = days
        self.so   = so
        self.label = label
        self.squad = squad

class Campaign:
    def __init__(self, name:str, year:int, level:int, lengths:list):
        self.name  = name
        self.year  = year
        self.level = level

        self.lengths = []
        for l in lengths:
            cl = CampaignLength(l['days'], l['so'], l['label'], l['squad'])
            self.lengths.append(cl)
