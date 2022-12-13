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
sys.path.append(Path(__file__).resolve().parent.parent.parent.as_posix())


from dvg_randomizer.data   import Data

data = Data()
for bg in data.boardgames:
    first = bg.name.split(' ')[0].lower()
    with open(f'{first}.yaml', 'w') as fh:
        services = set()
        for a in bg.aircrafts:
            for s in a.services:
                services.add(s)
#        fh.write(f'--- {bg.name}\n')
        if ':' in bg.name:
            fh.write(f"name: '{bg.name}'\n")
        else:
            fh.write(f'name: {bg.name}\n')
        fh.write(f'alias: {bg.alias}\n')
        fh.write(f'services: {sorted([s for s in services])}\n')
        fh.write('aircrafts:\n')
        for a in bg.aircrafts:
            fh.write(f'  - name: {a.name}\n')
            fh.write(f'    box: {a.box}\n')
            fh.write(f'    service: {a.services}\n')
            fh.write(f'    year_in: {a.year_in}\n')
            fh.write(f'    year_out: {a.year_out}\n')
            fh.write(f'    cost: {a.cost}\n')
            fh.write(f'    role: {a.role}\n')
        fh.write('pilots:\n')
        for p in bg.pilots:
            if '"' in p.name:
                fh.write(f"  - name: '{p.name}'\n")
            else:
                fh.write(f'  - name: {p.name}\n')
            fh.write(f'    box: {p.box}\n')
            fh.write(f'    service: {p.services}\n')
            fh.write(f'    aircraft: {p.aircraft.name}\n')
            if p.is_elite:
                fh.write(f'    elite: {p.elite}\n')
        fh.write('campaigns:\n')
        for c in bg.campaigns:
            if ':' in c.name:
                fh.write(f"  - name: '{c.name}'\n")
            else:
                fh.write(f'  - name: {c.name}\n')
            fh.write(f'    box: {c.box}\n')
            fh.write(f'    year: {c.year}\n')
            fh.write(f'    service: {c.service}\n')
            fh.write(f'    level: {c.level}\n')
            fh.write(f'    duration:\n')
            for d in c.lengths:
                fh.write(f'      - label: {d.label}\n')
                fh.write(f'        level: {d.level}\n')
                fh.write(f'        length: {d.days}\n')
                fh.write(f'        starting_so: {d.so}\n')
                fh.write(f'        pilots: {d.pilots}\n')
            allowed = [a[0] for a in c.allowed if not a[1]]
            forced  = [(a[0], a[1]) for a in c.allowed if a[1]]
            if len(allowed) > 0:
                fh.write(f'    allowed: {allowed}\n')
            if len(forced) > 0:
                fh.write(f'    forced:\n')
                for f in forced:
                    fh.write(f'      - {f[0]}: {f[1]}\n')
            if len(c.forbidden) > 0:
                fh.write(f'    forbidden: {c.forbidden}\n')
            if len(c.special_costs) > 0:
                fh.write(f'    special_costs:\n')
                for sc in c.special_costs:
                    fh.write(f'      - {sc[0]}: {sc[1]}\n')


