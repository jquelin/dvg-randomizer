
import csv
import pkg_resources

#

from dvg.aircraft  import Aircraft
from dvg.boardgame import Boardgame
from dvg.campaign  import Campaign
from dvg.pilot     import Pilot
from dvg.logger    import log

# ----

class Data:
    def __init__(self):
        self.load_boardgames()
        self.load_aircrafts()
        self.load_pilots()
        self.load_campaigns()

    # -- data loading

    def load_aircrafts(self):
        log.info("loading aircrafts") 
        filepath = self.get_csv_path('aircrafts.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, service, name, year_in, year_out, cost, role in reader:
                bg = self.boardgame(bgname)
                # FIXME check bg
                aircraft = Aircraft(bg, box, service, name, year_in,
                                    year_out, cost, role)
                log.debug(f'- found aircraft {aircraft}')
                bg.add_aircraft(aircraft)

            for bg in self.boardgames:
                log.info(f"{bg}: found {len(bg.aircrafts)} aircrafts")



    def load_boardgames(self):
        log.info("loading boardgames") 
        filepath = self.get_csv_path('boardgames.csv')
        log.info(f"reading {filepath}")
        self.boardgames = []
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for alias, name in reader:
                boardgame = Boardgame(name, alias)
                log.debug(f"- found boardgame {boardgame}")
                self.boardgames.append(boardgame)
            log.info(f"found {len(self.boardgames)} boardgames")

    def load_campaigns(self):
        log.info("loading campaigns")
        filepath = self.get_csv_path('campaigns.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, name, year, service, level, \
                    sdays, sso, ssquad, mdays, mso, msquad, ldays, lso, lsquad in reader:
                bg = self.boardgame(bgname)
                # FIXME check bg
                campaign = Campaign(bg, box, name, year, service, level,
                                    sdays, sso, ssquad,
                                    mdays, mso, msquad,
                                    ldays, lso, lsquad)
                # FIXME: check if campaign has at least one length
                log.debug(f"- found campaign {campaign}")
                bg.add_campaign(campaign)

            for bg in self.boardgames:
                log.info(f"{bg}: found {len(bg.campaigns)} campaigns")


    def load_pilots(self):
        log.info("loading pilots")
        filepath = self.get_csv_path('pilots.csv')
        log.info(f"reading {filepath}")
        with open(filepath) as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            for bgname, box, service, name, aircraft_name, elite in reader:
                bg = self.boardgame(bgname)
                # FIXME check bg
                aircraft = bg.aircraft(service, aircraft_name)
                if aircraft is None:
                    log.error(f"could not find an aircraft matching {bg.alias}-{service}-{aircraft_name}")
                else:
                    pilot = Pilot(bg, box, service, name, aircraft)
                    log.debug(f'- found pilot {pilot}')
                    bg.add_pilot(pilot)

            for bg in self.boardgames:
                log.info(f"{bg}: found {len(bg.pilots)} pilots")


    # -- finder methods

    def boardgame(self, name:str):
        return next(
            filter(lambda bg: bg.name == name or bg.alias == name, self.boardgames),
            None
        )


    # -- methods

    def get_csv_path(self, file:str):
        return pkg_resources.resource_filename('dvg.csv', file)


data = Data()    # global var used to access DVG data
