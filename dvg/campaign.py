
from dvg.logger import log

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

        # then, check if aircraft is allowed
        if len(self.allowed) > 0:
            allowed = [x[0] for x in self.allowed]
            log.debug(f'pruning all but {allowed}')
            pilots = list(filter(lambda p: p.aircraft.name in allowed, pilots))
        log.debug(f'{self.id()}: found {len(pilots)} pilots after checking allowed')

        # finally, check if aircraft is forbidden
        if len(self.forbidden) > 0:
            log.debug(f'pruning all {self.forbidden}')
            pilots = list(filter(lambda p: p.aircraft.name not in self.forbidden, pilots))
        log.debug(f'{self.id()}: found {len(pilots)} pilots after checking forbidden')

        self.pilots = pilots
