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

import re

from dvg_randomizer.logger import log

class CampaignLength:
    def __init__(self, level, days, so, squad):
        self.level  = level
        self.days   = days
        self.so     = int(so)

        # squad composition
        self.squad  = squad
        self.pilots = [int(i) for i in squad.split('+')]

        # campaign length label
        labels      = ['short', 'medium', 'long']
        self.label  = labels[self.level-1]

class Campaign:
    def __init__(self, bg, box, name, year, service, level,
                 sdays, sso, ssquad,
                 mdays, mso, msquad,
                 ldays, lso, lsquad):
        self.boardgame = bg
        self.box       = box
        self.name      = name
        self.year      = int(year)
        if service == '*':
            self.service = '*'
            self.services = { service for aircraft in bg.aircrafts for
                             service in aircraft.services }
        else:
            self.service   = service
            self.services  = service.split('+')
        self.level     = int(level)

        # campaign lengths
        self.short  = CampaignLength(1, sdays, sso, ssquad) if sdays!='' else None
        self.medium = CampaignLength(2, mdays, mso, msquad) if mdays!='' else None
        self.long   = CampaignLength(3, ldays, lso, lsquad) if ldays!='' else None
        self.lengths = [cl for cl in [self.short, self.medium, self.long] if cl is not None]

        # Some campaigns allow only some planes or forbid some.
        # Some even fix the number of a given aircraft.
        # Some have special costs for airplanes.
        self.allowed   = []     # allowed planes
        self.forbidden = []     # forbidden planes
        self.special_costs = [] # special aircraft costs


    def id(self):
        return f'{self.boardgame.alias}-{self.name}-{self.service}-{self.year}'

    def __repr__(self):
        out = '[' + ",".join([l.label for l in self.lengths]) + ']'
        return f'{self.id()} level={self.level} {out}'

    def compute_pilots(self):
        """Compute the list of pilots matching the campaign criteria.
        The criteria are:
            - aircraft year in/out
            - campaign service
            - allowed aircrafts
            - forbidden aircrafts

        Once computed, the list of matching pilots is stored in
        self.pilots. Bonus pilots (those with bonus aircraft) are stored
        in self.bonuses. Those bonus pilots cannot be selected in the
        random squadron, but one will be added for free to the roaster.

        No return value.
        """
        # first, find all pilots whose aircraft match the campaign year
        pilots = list( filter(
            lambda p: (
                p.aircraft.year_in <= self.year
                and self.year <= p.aircraft.year_out
            ),
            self.boardgame.pilots
        ) )
        log.debug(f'{self.id()}: found {len(pilots)} pilots matching year')

        # then, check the pilot service
        matching = []
        for srv in self.services:
            matching.extend(list(filter(lambda p: srv in p.services, pilots)))
        pilots = matching
        log.debug(f'{self.id()}: found {len(pilots)} pilots matching service')

        # split pilots into regular and bonus.
        bonuses = list(filter(lambda p: p.aircraft.bonus, pilots))
        pilots  = list(filter(lambda p: not p.aircraft.bonus, pilots))
        log.debug(f'{self.id()}: found {len(pilots)} pilots')
        log.debug(f'{self.id()}: found {len(bonuses)} bonuses')
        self.bonuses = bonuses

        # then, check if aircraft is allowed
        if len(self.allowed) > 0:
            allowed = [x[0] for x in self.allowed]
            allowed_regex = '|'.join(allowed)
            log.debug(f'pruning all but {allowed}')
            pilots = list(
                filter(
                    lambda p: p.aircraft.name in allowed or
                        re.match(allowed_regex, p.aircraft.name, re.I),
                    pilots)
            )
        log.debug(f'{self.id()}: found {len(pilots)} pilots after checking allowed')

        # finally, check if aircraft is forbidden
        if len(self.forbidden) > 0:
            log.debug(f'pruning all {self.forbidden}')
            pilots = list(filter(lambda p: p.aircraft.name not in self.forbidden, pilots))
        log.debug(f'{self.id()}: found {len(pilots)} pilots after checking forbidden')

        # store the result
        self.pilots = pilots

