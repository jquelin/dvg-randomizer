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

import argparse

def run():
    parser = argparse.ArgumentParser(
        prog='dvg-randomizer',
        description='What the program does',
        epilog='---')
    parser.add_argument('-c', '--console', action='store_true')
    args = parser.parse_args()

    if args.console:
        from dvg_randomizer.ui.console import ConsoleUI
        ui = ConsoleUI()
        ui.cmdloop()

    else:
        from dvg_randomizer.ui.graphical import GraphicalUI
        ui = GraphicalUI()
        ui.mainloop()


if __name__ == '__main__':
    run()
