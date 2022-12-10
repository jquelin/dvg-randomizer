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

# create config directory if needed
_config_dir = Path(appdirs.user_config_dir('dvg-randomizer'))
_config_dir.mkdir(parents=True, exist_ok=True)

# read & parse config file
_config_file = Path(_config_dir, 'dvg-randomizer.yaml')
try:
    with _config_file.open() as ystream:
        try:
            _config = yaml.safe_load(ystream)
        except yaml.YAMLError as e:
            print('error loading {yfile.as_posix()}: {e}')
except FileNotFoundError:
    _config = {}


def get(key, default=None):
    if key in _config:
        return _config[key]
    return default

def set(key, value):
    # store new value
    _config[key] = value
    # overwrite config file
    with open(_config_file, 'w') as outfile:
        yaml.dump(_config, outfile)
