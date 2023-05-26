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

import pyexcel_ods
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
        # load data from ODS file
        self.load_ods_data()
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
        data = self.ods_data["aircrafts"]
        for i in range(1, len(data)):
            if len(data[i]) != 10:
                continue

            (bgalias, box, service, name, year_in, year_out, cost_s,
                cost_m, cost_l, role) = data[i]
            bg = self.boardgame(bgalias)
            if bg is None:
                log.error(f'boardgame {bgalias} not found')
            else:
                aircraft = Aircraft(bg, box, service, name, year_in,
                                    year_out, cost_s, cost_m, cost_l, role)
                log.debug(f'- found aircraft {aircraft}')
                bg.add_aircraft(aircraft)

        for bg in self.boardgames:
            log.info(f"{bg}: found {len(bg.aircrafts)} aircrafts")

    def load_allowed(self):
        log.info("loading allowed aircrafts")
        data = self.ods_data["allowed"]
        for i in range(1, len(data)):
            if len(data[i]) == 0:
                continue

            # no mandatory number of aircrafts: pad with None
            if len(data[i]) == 6:
                data[i].append(None)

            (bgalias, box, campaign_name, year, service, aircraft, nb) = data[i]
            bg = self.boardgame(bgalias)
            if bg is None:
                log.error(f'boardgame {bgalias} not found')
            else:
                campaign = bg.campaign(campaign_name, int(year), service)
                if campaign is None:
                    log.error(f'campaign [{campaign_name}][{year}][{service}] not found for {bg}')
                else:
                    campaign.allowed.append([aircraft, nb])

    def load_boardgames(self):
        log.info("loading boardgames") 
        data = self.ods_data["boardgames"]
        self.boardgames = []
        for i in range(1, len(data)):
            alias, name = data[i]
            if alias != '':
                boardgame = Boardgame(name, alias)
                log.debug(f"- found boardgame {boardgame}")
                self.boardgames.append(boardgame)
        log.info(f"found {len(self.boardgames)} boardgames")

    def load_campaigns(self):
        log.info("loading campaigns")
        data = self.ods_data["campaigns"]
        for i in range(1, len(data)):
            if len(data[i]) == 0:
                continue

            # only short campaign: padd medium
            if len(data[i]) == 9:
                data[i].extend(['']*3)
            # no long: padd long
            if len(data[i]) == 12:
                data[i].extend(['']*3)

            (bgalias, box, name, year, service, level, sdays, sso,
                ssquad, mdays, mso, msquad, ldays, lso, lsquad) = data[i]
            bg = self.boardgame(bgalias)
            if bg is None:
                log.error(f'boardgame {bgalias} not found')
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
        data = self.ods_data["campaign costs"]
        for i in range(1, len(data)):
            if len(data[i]) == 0:
                continue

            bgalias, box, name, year, service, aircraft, cost = data[i]
            bg = self.boardgame(bgalias)
            if bg is None:
                log.error(f'boardgame {bgalias} not found')
            else:
                campaign = bg.campaign(name, int(year), service)
                if campaign is None:
                    log.error(f'boardgame {bgalias} has no campaign {name}-{year}-{service}')
                else:
                    log.debug(f"- found campaign {campaign}")
                    campaign.special_costs.append([aircraft, float(cost)])

    def load_forbidden(self):
        log.info("loading forbidden aircrafts")
        data = self.ods_data["forbidden"]
        for i in range(1, len(data)):
            if len(data[i]) == 0:
                continue

            (bgalias, box, campaign_name, year, service, aircraft) = data[i]
            bg = self.boardgame(bgalias)
            if bg is None:
                log.error(f'boardgame {bgalias} not found')
            else:
                campaign = bg.campaign(campaign_name, int(year), service)
                if campaign is None:
                    log.error(f'campaign [{campaign_name}][{year}][{service}] not found for {bg}')
                else:
                    campaign.forbidden.append(aircraft)

    def load_ods_data(self):
        ods_file = Path(Path(__file__).parent, 'dvg.ods').as_posix()
        log.info(f"loading ODS data from {ods_file}")
        self.ods_data = pyexcel_ods.get_data(ods_file)


    def load_pilots(self):
        log.info("loading pilots")
        data = self.ods_data["pilots"]
        for i in range(1, len(data)):
            if len(data[i]) == 0:
                continue

            # default no elite
            if len(data[i]) == 5:
                data[i].extend([None]*3)
            (bgalias, box, service, name, aircraft_name, elite_s,
                elite_m, elite_l) = data[i]
            bg = self.boardgame(bgalias)
            if bg is None:
                log.error(f'boardgame {bgalias} not found')
            else:
                aircraft = bg.aircraft(service, aircraft_name)
                if aircraft is None:
                    log.error(f"could not find an aircraft matching {bg.alias}-{service}-{aircraft_name}")
                else:
                    pilot = Pilot(bg, box, service, name, aircraft,
                                    elite_s, elite_m, elite_l)
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


