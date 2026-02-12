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

class Pilot:
    def __init__(self, bg, box, service, name, aircraft, elite_s,
                 elite_m, elite_l):
        self.boardgame = bg
        self.box       = box
        self.service   = service
        self.services  = service.split('+')
        self.name      = name
        self.aircraft  = aircraft
        if elite_s is not None:
            self.is_elite    = True
            self.elite_name  = f'\u2606 {name} \u2606'
            self.elite = [elite_s, elite_m, elite_l]
        else:
            self.is_elite    = False
            self.elite       = None
            self.elite_name  = name

    def id(self):
        id = self.boardgame.alias
        for attribute in ['service', 'name']:
            id = id + '-' + getattr(self, attribute)
        return id


    def __repr__(self):
        return f'{self.id()} ({self.aircraft})'

    def so_bonus(self, game):
        special = game.campaign.special_costs
        cl_level = game.clength.level
        if self.is_elite:
            so_cost = self.elite[cl_level-1]
        else:
            if cl_level == 1:
                so_cost = self.aircraft.cost_s
            elif cl_level == 2:
                so_cost = self.aircraft.cost_m
            else:
                so_cost = self.aircraft.cost_l
            if special:
                for aircraft, cost in special:
                    if self.aircraft.name == aircraft:
                        sp_so_cost = int(cost * cl_level)
                        log.debug(f'aircraft {aircraft} has a special cost {sp_so_cost} (instead of {so_cost} for this campaign')
                        so_cost = sp_so_cost

        # so_bonus = - so_cost
        return -int(so_cost)

