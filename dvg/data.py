
import csv
import pkg_resources

#

from dvg.aircraft  import Aircraft
from dvg.boardgame import Boardgame
from dvg.logger    import log

print(__name__)


# ----

class Data:
    def __init__(self):
        self.load_boardgames()
        self.load_aircrafts()

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
