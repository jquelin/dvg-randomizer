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


from dvg.logger import log


class Game:
    def __init__(self, bg):
        self.boardgame = bg
        self.boxes = set(bg.boxes())
        self.campaign = None

    def campaigns(self):
        campaigns = [c for c in self.boardgame.campaigns if c.box in self.boxes]
        return campaigns

    def set_campaign(self, campaign, clength):
        self.campaign  = campaign
        self.clength   = clength
        self.pilots    = []

