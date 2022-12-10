#
# This file is part of dvg-randomizer.
#
# dvg-randomizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# dvg-randomizer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dvg-randomizer. If not, see
# <https://www.gnu.org/licenses/>.
#

import csv
from pathlib import Path

#

from dvg_randomizer.aircraft  import Aircraft
from dvg_randomizer.boardgame import Boardgame
from dvg_randomizer.campaign  import Campaign
from dvg_randomizer.pilot     import Pilot
from dvg_randomizer.logger    import log

#  ----

class Data:
    def __init__(self):
        # load csv files
        self.load_boardgames()
        self.load_aircrafts()
        self.load_pilots()
        self.load_campaigns()
        self.load_campaign_costs()
        self.load_allowed()
        self.load_forbidden()

        # find campaign pilots
        log.info('find campaign pilots')
        for bg in self.boardgames:
            for cmpgn in bg.campaigns:
                cmpgn.compute_pilots()
                log.info(f'{cmpgn}: found {len(cmpgn.pilots)} pilots')

        # compute lengths for gui
        self.find_longest()

    # -- data loading

    def load_aircrafts(self):
        log.info("loading aircrafts") 
        filepath = self.get_csv_path('aircrafts.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, service, name, year_in, year_out, cost, role in reader:
                bg = self.boardgame(bgname)
                if bg is None:
                    log.error(f'boardgame {bgname} not found')
                else:
                    aircraft = Aircraft(bg, box, service, name, year_in,
                                        year_out, cost, role)
                    log.debug(f'- found aircraft {aircraft}')
                    bg.add_aircraft(aircraft)

            for bg in self.boardgames:
                log.info(f"{bg}: found {len(bg.aircrafts)} aircrafts")

    def load_allowed(self):
        log.info("loading allowed aircrafts")
        filepath = self.get_csv_path('allowed.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, campaign_name, year, service, aircraft, nb in reader:
                bg = self.boardgame(bgname)
                if bg is None:
                    log.error(f'boardgame {bgname} not found')
                else:
                    campaign = bg.campaign(campaign_name, int(year), service)
                    if campaign is None:
                        log.error(f'campaign [{campaign_name}][{year}][{service}] not found for {bg}')
                    else:
                        campaign.allowed.append([aircraft, nb])

    def load_boardgames(self):
        log.info("loading boardgames") 
        filepath = self.get_csv_path('boardgames.csv')
        log.info(f"reading {filepath}")
        self.boardgames = []
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for alias, name in reader:
                boardgame = Boardgame(name, alias)
                log.debug(f"- found boardgame {boardgame}")
                self.boardgames.append(boardgame)
            log.info(f"found {len(self.boardgames)} boardgames")

    def load_campaigns(self):
        log.info("loading campaigns")
        filepath = self.get_csv_path('campaigns.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, name, year, service, level, \
                    sdays, sso, ssquad, mdays, mso, msquad, ldays, lso, lsquad in reader:
                bg = self.boardgame(bgname)
                if bg is None:
                    log.error(f'boardgame {bgname} not found')
                else:
                    for single_service in service.split('|'):
                        campaign = Campaign(bg, box, name, year, single_service, level,
                                            sdays, sso, ssquad,
                                            mdays, mso, msquad,
                                            ldays, lso, lsquad)
                        # FIXME: check if campaign has at least one length
                        # FIXME: check if campaign is a duplicate
                        log.debug(f"- found campaign {campaign}")
                        bg.add_campaign(campaign)

            for bg in self.boardgames:
                log.info(f"{bg}: found {len(bg.campaigns)} campaigns")

    def load_campaign_costs(self):
        log.info("loading campaign costs")
        filepath = self.get_csv_path('campaign_costs.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, name, year, service, aircraft, cost in reader:
                bg = self.boardgame(bgname)
                if bg is None:
                    log.error(f'boardgame {bgname} not found')
                else:
                    campaign = bg.campaign(name, int(year), service)
                    if campaign is None:
                        log.error(f'boardgame {bgname} has no campaign {name}-{year}-{service}')
                    else:
                        log.debug(f"- found campaign {campaign}")
                        campaign.special_costs.append([aircraft, float(cost)])

    def load_forbidden(self):
        log.info("loading forbidden aircrafts")
        filepath = self.get_csv_path('forbidden.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, campaign_name, year, service, aircraft in reader:
                bg = self.boardgame(bgname)
                if bg is None:
                    log.error(f'boardgame {bgname} not found')
                else:
                    campaign = bg.campaign(campaign_name, int(year), service)
                    if campaign is None:
                        log.error(f'campaign [{campaign_name}][{year}][{service}] not found for {bg}')
                    else:
                        campaign.forbidden.append(aircraft)

    def load_pilots(self):
        log.info("loading pilots")
        filepath = self.get_csv_path('pilots.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, service, name, aircraft_name, elite in reader:
                bg = self.boardgame(bgname)
                if bg is None:
                    log.error(f'boardgame {bgname} not found')
                else:
                    aircraft = bg.aircraft(service, aircraft_name)
                    if aircraft is None:
                        log.error(f"could not find an aircraft matching {bg.alias}-{service}-{aircraft_name}")
                    else:
                        pilot = Pilot(bg, box, service, name, aircraft, elite)
                        log.debug(f'- found pilot {pilot}')
                        bg.add_pilot(pilot)

            for bg in self.boardgames:
                log.info(f"{bg}: found {len(bg.pilots)} pilots")


    # -- finder methods

    def boardgame(self, name:str):
        return next(
            filter(lambda bg: bg.name == name or bg.alias == name, self.boardgames),
            None
        )


    # -- methods

    def find_longest(self):
        lists = {
            'ranks'     : ['Newbie', 'Green', 'Average', 'Skilled', 'Veteran', 'Legendary'] ,
            'boxes'     : [],
            'pilots'    : [],
            'services'  : [],
            'aircrafts' : [],
            'roles'     : [],
            'campaigns' : [],
        }

        for bg in self.boardgames:
            lists['pilots'].extend([p.name for p in bg.pilots])
            lists['services'].extend([p.service for p in bg.pilots])
            lists['aircrafts'].extend([a.name for a in bg.aircrafts])
            lists['roles'].extend([a.role for a in bg.aircrafts])
            lists['campaigns'].extend([c.name for c in bg.campaigns])
            lists['boxes'].extend([c.box for c in bg.campaigns])

        self.longest = {}
        for k, v in lists.items():
            self.longest[k] = max(v, key=len)
            log.debug(f'longest string for {k}: {self.longest[k]}')


    def get_csv_path(self, file:str):
#        curfpath = Path(__file__).parent()
#        wanted = Path(curfpath, 'csv', file)
#        log.debug(f'looking file: {wanted}')
        return Path(Path(__file__).parent, 'csv', file).as_posix()

