
from dvg.logger import log


class Game:
    def __init__(self, bg, campaign, clength):
        self.bg       = bg
        self.campaign = campaign
        self.clength  = clength
        self.pilots   = []

