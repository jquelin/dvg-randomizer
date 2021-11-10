
from dvg.logger import log

class CampaignLength:
    def __init__(self, level, days, so, squad):
        self.level = level
        self.days  = days
        self.so    = so
        self.squad = squad
        labels = ['short', 'medium', 'long']
        self.label = labels[self.level-1]

class Campaign:
    def __init__(self, bg, box, name, year, service, level,
                 sdays, sso, ssquad, mdays, mso, msquad,
                 ldays, lso, lsquad):
        self.boardgame = bg
        self.box       = box
        self.name      = name
        self.year      = int(year)
        self.service   = service
        self.services  = service.split('+')
        self.level     = int(level)

        # campaign lengths
        self.lengths = []
        lengths = [
            (sdays, sso, ssquad),
            (mdays, mso, msquad),
            (ldays, lso, lsquad),
        ]
        i = 0
        for l in lengths:
            i += 1
            days, so, squad = l
            if days != '':
                cl = CampaignLength(i, days, so, squad)
                self.lengths.append(cl)

        # Some campaigns allow only some planes or forbid some.
        # Some even fix the number of a given aircraft.
        self.allowed   = []     # allowed planes
        self.forbidden = []     # forbidden planes


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
