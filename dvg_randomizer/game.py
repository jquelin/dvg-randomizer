#!/bin/python
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

import cmd2
import random

from dvg_randomizer.data   import Data
from dvg_randomizer.logger import log

class Game(cmd2.Cmd):
    def __init__(self, *args, **kwargs):
        # remove unwanted shortcuts *before* calling parent __init__
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        for shortcut in ['!', '@', '@@']:
            del shortcuts[shortcut]
        cmd2.Cmd.__init__(self, shortcuts=shortcuts)

        # remove unwanted commands
        for cmd in ['do_edit', 'do_macro', 'do_run_pyscript',
                'do_run_script', 'do_shell']:
            delattr(cmd2.Cmd, cmd)

        # remove unwanted settings
        for setting in ['allow_style', 'always_show_hint', 'debug',
                'echo', 'editor', 'feedback_to_output',
                'max_completion_items', 'quiet', 'timing']:
            self.remove_settable(setting)

        # customizing cmd2
        self.prompt = 'dvg: '
        self.runcmds_plus_hooks(['alias create bg boardgame >/dev/null'])


    def do_list(self, stmt):
        """List available choices"""
        # depending on the app status, command will list different
        # things.
        if len(stmt.argv) == 1:
            what = 'boardgames'
        else:
            what = stmt.argv[1]

        # check aliases
        aliases = {
            'bg': 'boardgames',
        }
        if what in aliases:
            what = aliases[what]

        print(what)

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
        aircrafts = []
        nb_random = nbtotal
        for aircraft in sorted(nb_aircrafts):
            nb_available = len([p for p in pilots if p.aircraft == aircraft])
            if aircraft.name in nb_mandatory:
                nb_fixed = int(nb_mandatory[aircraft.name])
                log.debug(
                    f'aircraft {aircraft} available: ' +
                    f'wanting {nb_fixed} pilots ' +
                    f'({nb_available} available)'
                )
                aircrafts.append([aircraft, nb_fixed, nb_fixed])
                nb_random -= nb_fixed
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
        log.debug(f'generating squad for {clength.label}: {squad}')

        # draw new set of pilots
        available = [p for p in campaign.pilots if p.box in self.boxes]
        selected  = []
        self.pilots = []
        log.debug(f'{len(available)} pilots available in pool')

        for aircraft, nb in self.composition:
            subset = [a for a in available if a.aircraft == aircraft]
            random.shuffle(subset)
            log.debug(f'wanting {nb} {aircraft} - {len(subset)} available')
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
        log.debug('assigning ranks')
        ranks = ['newbie', 'green', 'average', 'skilled', 'veteran', 'legendary']
        for rank, nb in zip(ranks, squad):
            i = nb
            while i>0:
                p = selected.pop(0)
                p.rank = rank
                log.info(f'assigning rank {rank} to {p}')
                self.pilots.append(p)
                i -= 1

    def set_campaign(self, campaign, clength):
        self.campaign    = campaign
        self.clength     = clength
        self.composition = []


if __name__ == '__main__':
    game = Game()
    sys.exit(game.cmdloop())

