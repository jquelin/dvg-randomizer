
import csv
import json
import logging
import os
import pkg_resources

from aircraft import Aircraft
from campaign import Campaign


def all_boardgames():
    boardgames = []
    filepath = pkg_resources.resource_filename('data', 'games.csv')
    logging.info(f"reading {filepath}")
    with open(filepath) as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        for alias, name in reader:
            logging.debug(f"- found boardgame {name} ({alias})")
            boardgames.append(Boardgame(alias=alias, name=name))
        logging.info(f"found {len(boardgames)} boardgames")
        return boardgames

class Boardgame:
    def __init__(self, alias:str, name:str):
        self.alias = alias
        self.name  = name
        self.load_campaigns()
        self.load_aircrafts()

    # -- loading data

    def load_aircrafts(self):
        filepath = pkg_resources.resource_filename(f'data.{self.alias}', 'aircrafts.json')
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
        self.aircrafts = aircrafts

    def load_campaigns(self):
        filepath = pkg_resources.resource_filename(f'data.{self.alias}', 'campaigns.json')
        logging.info(f"reading {filepath}")
        campaigns = []
        with open(filepath) as ifp:
            data = json.load(ifp)
        for c in data:
            name = c['name']
            year = c['year']
            level   = c['level']
            lengths = c['lengths']
            logging.debug(f"- found campaign: {name} - ({year})")
            newc = Campaign(name=name, year=year,
                            level=level, lengths=lengths)
            campaigns.append(newc)
        logging.info(f"found {len(campaigns)} campaigns")
        self.campaigns = campaigns


    # -- methods

    def find_campaign(self, name, year):
        for c in self.campaigns:
            if c.name == name and c.year == year:
                return c
