
import logging

class CampaignLength:
    def __init__(self, days:int, so:int, label:str, squad:list):
        self.days = days
        self.so   = so
        self.label = label
        self.squad = squad

class Campaign:
    def __init__(self, name:str, year:int, level:int, lengths:list):
        self.name  = name
        self.year  = year
        self.level = level

        self.lengths = []
        for l in lengths:
            cl = CampaignLength(l['days'], l['so'], l['label'], l['squad'])
            self.lengths.append(cl)
