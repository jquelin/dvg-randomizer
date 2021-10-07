
import csv
import json
import logging
import os
from pkg_resources import resource_filename

from aircraft import Aircraft
from campaign import Campaign
from pilot    import Pilot


def all_boardgames():
    boardgames = []
    filepath = resource_filename('data', 'games.csv')
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
        self.load_aircrafts()
        self.load_pilots()
        self.load_campaigns()

    # -- loading data

    def load_aircrafts(self):
        filepath = resource_filename(f'data.{self.alias}', 'aircrafts.json')
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
        filepath = resource_filename(f'data.{self.alias}', 'campaigns.json')
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

    def load_pilots(self):
        filepath = resource_filename(f'data.{self.alias}', 'pilots.json')
        logging.info(f"reading {filepath}")
        all_pilots = []
        with open(filepath) as ifp:
            data = json.load(ifp)
        for pilot in data:
            (name, ac_name) = pilot
            logging.debug(f"- found pilot: {name} ({ac_name})")
            aircraft = self.find_aircraft(ac_name)
            if aircraft == None:
                logging.error(f"non-existing aircraft {ac_name} for pilot {name}")
            newp = Pilot(name=name, aircraft=aircraft)
            all_pilots.append(newp)
        logging.info(f"found {len(all_pilots)} pilots")
        self.pilots = all_pilots


    # -- methods

    def find_campaign(self, name, year):
        for c in self.campaigns:
            if c.name == name and c.year == year:
                return c

    def find_aircraft(self, name):
        for aircraft in self.aircrafts:
            if aircraft.code == name:
                return aircraft
        return None
