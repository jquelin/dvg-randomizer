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

logger_name = 'dvg'

try:
    import colorlog
except:
    # no colorlog available
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(module)s.%(funcName)s:%(lineno)d %(levelname)s %(message)s',
            datefmt='%H:%M:%S'
        )
    )

    log = logging.getLogger(logger_name)

else:
    # colorlog available
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s %(module)s.%(funcName)s:%(lineno)d %(levelname)s %(message)s',
            datefmt='%H:%M:%S'
        )
    )
    log = colorlog.getLogger(logger_name)


log.setLevel(logging.DEBUG)
log.addHandler(handler)
