
from dvg.logger import log

class Pilot:
    def __init__(self, bg, box, service, name, aircraft, elite):
        self.boardgame = bg
        self.box       = box
        self.service   = service
        self.services  = service.split('+')
        self.name      = name
        self.aircraft  = aircraft
        if elite != '':
            self.is_elite    = True
            self.elite_name  = f'\u2606 {name} \u2606'
            if '+' in elite:
                self.elite   = [int(s) for s in elite.split('+')]
            else:
                self.elite   = [0, int(elite)]
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
            so_cost = self.elite[0] + self.elite[1]*cl_level
        else:
            so_cost = self.aircraft.cost * cl_level
            if special:
                for aircraft, cost in special:
                    if self.aircraft.name == aircraft:
                        sp_so_cost = int(cost * cl_level)
                        log.debug(f'aircraft {aircraft} has a special cost {sp_so_cost} (instead of {so_cost} for this campaign')
                        so_cost = sp_so_cost

        # so_bonus = - so_cost
        return -int(so_cost)

