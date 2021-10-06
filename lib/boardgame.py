
import csv
import logging
import os
import pkg_resources

import aircraft
import campaign


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
        filepath = pkg_resources.resource_filename(f'data.{self.alias}', 'campaigns.json')
        self.campaigns = campaign.load_campaigns(filepath)
        filepath = pkg_resources.resource_filename(f'data.{self.alias}', 'aircrafts.json')
        self.aircrafts = aircraft.load_aircrafts(filepath)

    def find_campaign(self, name, year):
        for c in self.campaigns:
            if c.name == name and c.year == year:
                return c
