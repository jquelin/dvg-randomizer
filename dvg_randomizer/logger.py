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

import colorlog
import logging

class Logger:
    def __init__(self):
        # create our logger
        log = colorlog.getLogger('dvg-randomizer')
        self.log = log

        # add the color console handler
        colors = colorlog.default_log_colors
        colors['DEBUG'] = 'blue'
        #colors['INFO']  = 'white'
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=colors
        )
        handler = colorlog.StreamHandler()
        handler.setFormatter(formatter)
        log.addHandler(handler)

        # set default log level
        log.setLevel(logging.INFO)


    def __getattr__(self, name):
        """Delegate attribute access to the underlying logger."""
        return getattr(self.log, name)

    # -- Public methods
    def increase_verbosity(self):
        """Increase the verbosity level (lower the log level)."""
        current_level = self.log.level
        if current_level > logging.DEBUG:
            new_level = current_level - 10
            self.log.setLevel(new_level)
            self.log.debug(f'Increased verbosity to {logging.getLevelName(new_level)}')

    def decrease_verbosity(self):
        """Decrease the verbosity level (raise the log level)."""
        current_level = self.log.level
        if current_level < logging.CRITICAL:
            new_level = current_level + 10
            self.log.setLevel(new_level)
            self.log.debug(f'Decreased verbosity to {logging.getLevelName(new_level)}')

log = Logger()

