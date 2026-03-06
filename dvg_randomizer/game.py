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

if __name__ == '__main__':
    from os.path import basename, dirname
    import sys
    bindir = dirname(dirname(__file__))
    sys.path.append(bindir)
    if basename(sys.path[0]) == 'dvg':
        del sys.path[0]

import random

from dvg_randomizer.data   import Data
from dvg_randomizer.logger import log

class Game:
    """ Game class, main entry point for the randomizer. """

    def do_load(self, *stmt):
        self.data = Data()

    def do_boardgame(self, bg):
        self.boardgame = bg
        self.boxes = set(bg.boxes())
        self.campaign = None

    def campaigns(self):
        campaigns = [c for c in self.boardgame.campaigns if c.box in self.boxes]
        return campaigns

    def get_aircraft_possibilities(self):
        pilots  = [p for p in self.campaign.pilots if p.box in self.boxes]
        nbtotal = sum(self.clength.pilots)
        log.debug(f'campaign requires maximum {nbtotal} pilots')

        nb_aircrafts = {}
        for p in pilots:
            aircraft = p.aircraft
            if aircraft in nb_aircrafts:
                nb_aircrafts[aircraft] += 1
            else:
                nb_aircrafts[aircraft] = 0

        nb_mandatory = {t[0]:t[1] for t in self.campaign.allowed if t[1]}
        nb_maximum   = {t[0]:t[2] for t in self.campaign.allowed if t[2]}
        aircrafts = []
        nb_random = nbtotal
        for aircraft in sorted(nb_aircrafts):
            nb_available = len([p for p in pilots if p.aircraft == aircraft])
            if aircraft.name in nb_mandatory:
                nbfixed = nb_mandatory[aircraft.name]
                log.debug(
                    f'aircraft {aircraft} available: ' +
                    f'wanting {nbfixed} pilots ' +
                    f'({nb_available} available)'
                )
                aircrafts.append([aircraft, nbfixed, nbfixed])
                nb_random -= nbfixed
            elif aircraft.name in nb_maximum:
                nb_max = nb_maximum[aircraft.name]
                log.debug(
                    f'aircraft {aircraft} available: ' +
                    f'wanting [0-{nb_max}] pilots ' +
                    f'({nb_available} available)'
                )
                aircrafts.append([aircraft, 0, nb_max])
            else:
                nb_max = min(nb_available, nbtotal)
                log.debug(f'aircraft {aircraft} available: [0-{nb_max}]({nb_available} available)')
                aircrafts.append([aircraft, 0, nb_max])

        return aircrafts

    def get_squad_size(self):
        return sum(self.clength.pilots)

    def draw_roaster(self):
        # fetch squad composition
        campaign = self.campaign
        clength  = self.clength
        squad    = self.clength.pilots
        log.info(f'generating squad for {clength.label}: {squad}')

        # Draw new set of pilots
        available = [p for p in campaign.pilots if p.box in self.boxes]
        selected  = []
        self.pilots = []
        log.debug(f'{len(available)} pilots available in pool')

        # Then, compute the possibilities for each aircraft.
        possibilities = { pos[0].name : pos[2] for pos in
                          self.get_aircraft_possibilities() }

        # Now comes the part where we pick pilots for the squadron.
        # First, pick pilots for mandatory aircrafts.
        for aircraft, nb in self.composition:
            if nb == 0:
                # no pilot with this aircraft is mandatory, so we can
                # skip it during this step.
                continue

            # pick pilots for this aircraft, and add them to the
            # selected list.
            subset = [a for a in available if a.aircraft == aircraft]
            log.debug(f'wanting {nb} {aircraft} - {len(subset)} available')
            random.shuffle(subset)
            picked = subset[:nb]
            selected.extend(picked)
            for p in picked: log.debug(f'adding pilot {p}')
            # and remove this aircraft from the possibilities, since we
            # already picked the mandatory pilots for it.
            possibilities[aircraft.name] = 0

        # Now, remove the selected pilots from the available pool, and
        # shuffle the remaining pilots, so that we can pick random
        # pilots for the remaining slots.
        remaining = [p for p in available if p not in selected]
        random.shuffle(remaining)

        # complete with other airplanes
        nbtotal    = sum(squad)
        nbselected = len(selected)
        while nbselected < nbtotal:
            log.debug(f'wanting {nbtotal}, already having {nbselected} - {len(remaining)} available')
            pilot    = remaining.pop(0)
            aircraft = pilot.aircraft
            if possibilities[aircraft.name] > 0:
                selected.append(pilot)
                possibilities[aircraft.name] -= 1
                nbselected += 1
                log.debug(f'adding pilot {pilot}')
            else:
                log.debug(f'skipping pilot {pilot} - no more {aircraft} allowed')

        # randomize the order of selected pilots, so that ranks are not
        # assigned to pilots in a deterministic way.
        random.shuffle(selected)
        random.shuffle(remaining)
        self.remaining_pilots = remaining

        # assign ranks
        log.info('assigning ranks')
        ranks = ['newbie', 'green', 'average', 'skilled', 'veteran', 'legendary']
        for rank, nb in zip(ranks, squad):
            i = nb
            while i>0:
                p = selected.pop(0)
                p.rank = rank
                log.debug(f'assigning rank {rank} to {p}')
                self.pilots.append(p)
                i -= 1

        # finally, add bonus pilots if boardgame supports it.
        if self.boardgame.bonus > 0:
            bonus = random.choice(campaign.bonuses)
            bonus.rank = 'average'
            log.info(f'adding bonus pilot {bonus}')
            self.pilots.append(bonus)


    def set_campaign(self, campaign, clength):
        self.campaign    = campaign
        self.clength     = clength
        self.composition = []


