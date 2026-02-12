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


from dvg_randomizer.logger import log

class Aircraft:
    def __init__(self, bg, box, service, name, year_in:int,
                 year_out:int, cost_s, cost_m, cost_l, role):
        self.boardgame = bg
        self.box       = box
        self.service   = service
        self.services  = service.split('+')
        self.name      = name
        self.year_in   = int(year_in)
        self.year_out  = int(year_out) if year_out else 9999
        self.cost_s    = int(cost_s)
        self.cost_m    = int(cost_m)
        self.cost_l    = int(cost_l)
        self.role      = role

    def __lt__(self, a):
        return self.name < a.name

    def id(self):
        # box should not be part of id, since a core aircraft can be
        # reused from other expansions.
        id = self.boardgame.alias
        for attribute in ['service', 'name']:
            id = id + '-' + getattr(self, attribute)
        return id

    def __repr__(self):
        return f'{self.id()} ({self.role}) [{self.year_in}-{self.year_out}]'


