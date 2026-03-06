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
    """The Aircraft class represents a single aircraft, which can be
    used by pilots in campaigns. It is defined by its name, the service
    it belongs to, the years it was in service, and its cost for each
    campaign length. It also has a role, which can be used to categorize
    it (e.g. fighter, bomber, etc.). The Aircraft class also has a
    method to generate a unique id for the aircraft, which is based on
    the boardgame it belongs to, its service, and its name. The __repr__
    method provides a string representation of the aircraft, which
    includes its id, role, and years of service.
    """

    def __init__(self, bg, box:str, service:str, name:str,
                 year_in:int, year_out:int,
                 cost_s:int, cost_m:int, cost_l:int,
                 role: str, bonus: bool):
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
        self.bonus     = bonus

    def __lt__(self, a):
        return self.name < a.name

    def id(self) -> str:
        """Generate a unique id for the aircraft, which is based on the
        boardgame it belongs to, its service, and its name. The box is
        not included in the id, since a core aircraft can be reused from
        other expansions.

        Returns:
            str: A unique id for the aircraft.
        """
        # box should not be part of id, since a core aircraft can be
        # reused from other expansions.
        id = self.boardgame.alias
        for attribute in ['service', 'name']:
            id = id + '-' + getattr(self, attribute)
        return id

    def __repr__(self):
        return f'{self.id()} ({self.role}) [{self.year_in}-{self.year_out}]'


