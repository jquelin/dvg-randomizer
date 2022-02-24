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


import random

from dvg.logger import log


class Game:
    def __init__(self, bg):
        self.boardgame = bg
        self.boxes = set(bg.boxes())
        self.campaign = None

    def campaigns(self):
        campaigns = [c for c in self.boardgame.campaigns if c.box in self.boxes]
        return campaigns

    def set_campaign(self, campaign, clength):
        self.campaign  = campaign
        self.clength   = clength
        self.pilots    = []

        # fetch squad composition
        squad = clength.pilots
        log.debug(f'generating squad for {clength.label}: {squad}')

        # draw new set of pilots
        available = [p for p in campaign.pilots if p.box in self.boxes]
        selected  = []
        log.debug(f'{len(available)} pilots available in pool')

        # check if wanting a fixed number of given airplanes
        for allowed, nb in campaign.allowed:
            if nb != '':
                nb = int(nb)
                subset = [a for a in available if a.aircraft.name == allowed]
                random.shuffle(subset)
                log.debug(f'wanting {nb} {allowed} - {len(subset)} available')
                picked = subset[:nb]
                selected.extend(picked)
                for p in picked: log.info(f'adding pilot {p}')

        remaining = [p for p in available if p not in selected]

        # complete with other airplanes
        nbtotal    = sum(squad)
        nbselected = len(selected)
        log.debug(f'wanting {nbtotal}, already having {nbselected} - {len(remaining)} available')
        random.shuffle(remaining)
        nb = nbtotal-nbselected
        picked = remaining[:nb]
        others = remaining[nb:]
        selected.extend(picked)
        for p in picked: log.info(f'adding pilot {p}')
        random.shuffle(selected)
        self.remaining_pilots = others

        # assign ranks
        ranks = ['newbie', 'green', 'average', 'skilled', 'veteran', 'legendary']
        for rank, nb in zip(ranks, squad):
            i = nb
            while i>0:
                p = selected.pop(0)
                p.rank = rank
                log.info(f'assigning rank {rank} to {p}')
                self.pilots.append(p)
                i -= 1
