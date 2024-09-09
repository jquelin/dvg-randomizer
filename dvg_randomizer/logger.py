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

import logging
import colorlog

from dvg_randomizer.common import config

colors = colorlog.default_log_colors
colors['DEBUG'] = 'blue'
colors['INFO']  = 'white'
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    log_colors=colors
)
handler = colorlog.StreamHandler()
handler.setFormatter(formatter)
log = colorlog.getLogger('dvg_randomizer')
log.addHandler(handler)
_log_level = config.get('logging.level', logging.DEBUG)
log.setLevel(_log_level)

