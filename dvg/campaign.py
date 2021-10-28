
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
        self.level     = int(level)

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

    def id(self):
        return f'{self.boardgame.alias}-{self.name}-{self.service}-{self.year}'

    def __repr__(self):
        out = '[' + ",".join([l.label for l in self.lengths]) + ']'
        return f'{self.id()} level={self.level} {out}'
