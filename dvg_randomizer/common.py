#
# This file is part of dvg-randomizer.
#
# dvg-randomizer is free software: you can redistribute it and/or modify
# it under the # terms of the GNU General Public License as published by
# the Free Software # Foundation, either version 3 of the License, or
# (at your option) any later # version.
#
# dvg-randomizer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dvg-randomizer. If not, see <https://www.gnu.org/licenses/>.
#

from pathlib import Path
import appdirs
import contextlib
import yaml

class DVGConfig:
    def __init__(self):
        # create config directory if needed
        self.dir = Path(appdirs.user_config_dir('dvg-randomizer'))
        self.dir.mkdir(parents=True, exist_ok=True)

        # read & parse config file
        self.file = Path(self.dir, 'dvg-randomizer.yaml')
        try:
            with self.file.open() as ystream:
                try:
                    self.config = yaml.safe_load(ystream)
                except yaml.YAMLError as e:
                    print('error loading {yfile.as_posix()}: {e}')
        except FileNotFoundError:
            self.config = {}


    def get(self, key, default=None):
        if key in self.config:
            return self.config[key]
        return default

    def set(self, key, value):
        # store new value
        self.config[key] = value
        # overwrite config file
        with open(self.file, 'w') as outfile:
            yaml.dump(self.config, outfile)

config = DVGConfig()
