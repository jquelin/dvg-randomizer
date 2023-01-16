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



from pathlib import Path
import sys
from json import dumps as j
sys.path.append(Path(__file__).resolve().parent.parent.parent.as_posix())


from dvg_randomizer.data   import Data

def pp(fh, lvl, s):
    indent = ' ' * 4 * lvl
    fh.write(indent + s + '\n')

data = Data()
for bg in data.boardgames:
    first = bg.name.split(' ')[0].lower()
    with open(f'{first}.json', 'w') as fh:
        services = set()
        for a in bg.aircrafts:
            for s in a.services:
                services.add(s)
        pp(fh, 0,  '{')
        pp(fh, 1, f'"name": {j(bg.name)},')
        pp(fh, 1, f'"alias": {j(bg.alias)},')
        pp(fh, 1, f'"random": "full",')
        pp(fh, 1, f'"services": {j(sorted(services))},')
        pp(fh, 1, f'"aircrafts": [')
        for i in range(0, len(bg.aircrafts)):
            a = bg.aircrafts[i]
            pp(fh, 2,  '{')
            pp(fh, 3, f'"name": {j(a.name)},')
            pp(fh, 3, f'"box": {j(a.box)},')
            pp(fh, 3, f'"service": {j(a.services)},')
            pp(fh, 3, f'"year_in": {a.year_in},')
            pp(fh, 3, f'"year_out": {a.year_out},')
            pp(fh, 3, f'"cost": {a.cost},')
            pp(fh, 3, f'"role": {j(a.role)}')
            if i == len(bg.aircrafts)-1: pp(fh, 2,  '}')
            else: pp(fh, 2,  '},')
        pp(fh, 1, f'],')
        pp(fh, 1, f'"pilots": [')
        for i in range(0, len(bg.pilots)):
            p = bg.pilots[i]
            pp(fh, 2,  '{')
            pp(fh, 3, f'"name": {j(p.name)},')
            pp(fh, 3, f'"box": {j(p.box)},')
            pp(fh, 3, f'"service": {j(p.services)},')
            if p.is_elite:
                pp(fh, 3, f'"elite": {j(p.elite)},')
            pp(fh, 3, f'"aircraft": {j(p.aircraft.name)}')
            if i == len(bg.pilots)-1: pp(fh, 2,  '}')
            else: pp(fh, 2,  '},')
        pp(fh, 1, f'],')
        pp(fh, 1, f'"campaigns": [')
        for i in range(0, len(bg.campaigns)):
            c = bg.campaigns[i]
            pp(fh, 2,  '{')
            pp(fh, 3, f'"name": {j(c.name)},')
            pp(fh, 3, f'"box": {j(c.box)},')
            pp(fh, 3, f'"year": {c.year},')
            pp(fh, 3, f'"service": {j(c.service)},')
            pp(fh, 3, f'"duration": [')
            for k in range(0, len(c.lengths)):
                d = c.lengths[k]
                pp(fh, 4,  '{')
                pp(fh, 5, f'"label": {j(d.label)},')
                pp(fh, 5, f'"level": {d.level},')
                pp(fh, 5, f'"length": {d.days},')
                pp(fh, 5, f'"starting_so": {d.so},')
                pp(fh, 5, f'"pilots": {j(d.pilots)}')
                if k == len(c.lengths)-1: pp(fh, 4,  '}')
                else: pp(fh, 4,  '},')
            pp(fh, 3, f'],')
            allowed = [a[0] for a in c.allowed if not a[1]]
            forced  = [(a[0], a[1]) for a in c.allowed if a[1]]
            if len(allowed) > 0:
                pp(fh, 3, f'"allowed": {j(allowed)},')
            if len(forced) > 0:
                pp(fh, 3,  '"forced": {')
                for k in range(0, len(forced)):
                    f = forced[k]
                    out = f'{j(f[0])}: {f[1]}'
                    if k != len(forced)-1:
                        out += ','
                    pp(fh, 4, out)
                pp(fh, 3,  '},')
            if len(c.forbidden) > 0:
                pp(fh, 3, f'"forbidden": {j(c.forbidden)},')
            if len(c.special_costs) > 0:
                pp(fh, 3,  '"special_costs": {')
                for k in range(0, len(c.special_costs)):
                    sc = c.special_costs[k]
                    out = f'{j(sc[0])}: {sc[1]}'
                    if k != len(c.special_costs)-1:
                        out += ','
                    pp(fh, 4, out)
                pp(fh, 3,  '},')
            pp(fh, 3, f'"level": {c.level}')
            if i == len(bg.campaigns)-1: pp(fh, 2,  '}')
            else: pp(fh, 2,  '},')
        pp(fh, 1, f']')
        pp(fh, 0, '}')


