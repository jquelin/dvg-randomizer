
from dvg.logger import log


class Boardgame:
    def __init__(self, name:str, alias:str):
        self.name  = name
        self.alias = alias
        self.aircrafts = []
        self.campaigns = []
        self.pilots    = []

    def __repr__(self):
        return f'{self.name} ({self.alias})'

    # -- methods

    def add_aircraft(self, aircraft):
        # FIXME check if overlap
        self.aircrafts.append(aircraft)

    def add_campaign(self, campaign):
        self.campaigns.append(campaign)

    def add_pilot(self, pilot):
        # FIXME check if overlap
        self.pilots.append(pilot)

    # -- finders

    def aircraft(self, service, name):
        id = "-".join([self.alias, service, name])
        return next(
            filter(lambda a: a.id() == id, self.aircrafts),
            None
        )


#
#def all_boardgames():
#    boardgames = []
#    filepath = resource_filename('data', 'games.csv')
#    logger.info(f"reading {filepath}")
#    with open(filepath) as fp:
#        reader = csv.reader(fp)
#        next(reader, None)  # skip the headers
#        for alias, name in reader:
#            logger.debug(f"- found boardgame {name} ({alias})")
#            boardgames.append(Boardgame(alias=alias, name=name))
#        logger.info(f"found {len(boardgames)} boardgames")
#        return boardgames
#
#class Boardgame:
#    def __init__(self, alias:str, name:str):
#        self.alias = alias
#        self.name  = name
#        self.load_aircrafts()
#        self.load_pilots()
#        self.load_campaigns()
#
#     -- loading data
#
#    def load_aircrafts(self):
#        filepath = resource_filename(f'data.{self.alias}', 'aircrafts.csv')
#        logger.info(f"reading {filepath}")
#        all_aircrafts = []
#        with open(filepath) as ifp:
#            reader = csv.reader(ifp)
#            next(reader, None)  # skip the headers
#            for model, name, role, y_in, y_out, so1, so2, so3 in reader:
#                logger.debug(f"- found aircraft {model} {name} ({role}) [{y_in}-{y_out}] [{so1},{so2},{so3}]")
#                aircraft = Aircraft(model=model, name=name, role=role,
#                                    year_in=y_in, year_out=y_out,
#                                    costs=[int(so1), int(so2), int(so3)])
#                all_aircrafts.append(aircraft)
#        logger.info(f"found {len(all_aircrafts)} aircrafts")
#        self.aircrafts = all_aircrafts
#
#    def load_campaigns(self):
#        filepath = resource_filename(f'data.{self.alias}', 'campaigns.json')
#        logger.info(f"reading {filepath}")
#        campaigns = []
#        with open(filepath) as ifp:
#            data = json.load(ifp)
#        for c in data:
#            name = c['name']
#            year = c['year']
#            ac_codes = c['aircrafts']
#            level    = c['level']
#            lengths  = c['lengths']
#            logger.debug(f"- found campaign: {name} - ({year})")
#            newc = Campaign(name=name, year=year, level=level, lengths=lengths)
#            available_pilots = []
#            for pilot in self.pilots:
#                print(f"{self.name} {pilot.name} {pilot.aircraft}")
#                if pilot.aircraft.code is None:
#                    print("FOO")
#                    exit
#                if pilot.aircraft.code in ac_codes:
#                    print(pilot.name)
#
#            print(self.pilots)
#            pilots = [p for p in self.pilots if p.aircraft.code in ac_codes]
#            campaigns.append(newc)
#        logger.info(f"found {len(campaigns)} campaigns")
#        self.campaigns = campaigns
#
#    def load_pilots(self):
#        filepath = resource_filename(f'data.{self.alias}', 'pilots.csv')
#        logger.info(f"reading {filepath}")
#        all_pilots = []
#        with open(filepath) as ifp:
#            reader = csv.reader(ifp)
#            next(reader, None)  # skip the headers
#            for box, name, model in reader:
#                logger.debug(f"- found pilot {name} {model} [{box}]")
#                aircraft = self.find_aircraft(model)
#                if aircraft == None:
#                    logger.error(f"non-existing aircraft {model} for pilot {name}")
#                else:
#                    pilot = Pilot(name=name, aircraft=aircraft, box=box)
#                    all_pilots.append(pilot)
#        logger.info(f"found {len(all_pilots)} pilots")
#        self.pilots = all_pilots
#
#     -- methods
#
#    def find_campaign(self, name, year):
#        for c in self.campaigns:
#            if c.name == name and c.year == year:
#                return c
#
#    def find_aircraft(self, model):
#        for aircraft in self.aircrafts:
#            if aircraft.model == model:
#                return aircraft
#        return None
