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


import cmd2
import random
#import tkinter.font as tkFont
import types


from dvg_randomizer.common   import log
from dvg_randomizer.game     import Game
from dvg_randomizer.logsheet import generate_pdf
from dvg_randomizer.ui.base  import UI


class ConsoleUI(cmd2.Cmd, UI):
    def __init__(self, *args, **kwargs):
        # remove unwanted shortcuts *before* calling parent __init__
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        for shortcut in ['!', '@', '@@']:
            del shortcuts[shortcut]
        cmd2.Cmd.__init__(self, shortcuts=shortcuts,
                          allow_cli_args=False)

        # remove unwanted commands
        for cmd in ['do_edit', 'do_macro', 'do_run_pyscript',
                'do_run_script', 'do_shell']:
            delattr(cmd2.Cmd, cmd)

        # remove unwanted settings
        for setting in ['allow_style', 'always_show_hint', 'debug',
                'echo', 'editor', 'feedback_to_output',
                'max_completion_items', 'quiet', 'timing']:
            self.remove_settable(setting)

        # customizing cmd2
        self.prompt = 'dvg: '

        UI.__init__(self)

        # initialize gui with the first boardgame, and update gui
        # accordingly
#        self.vars.boardgame.set(self.game.data.boardgames[0].name)
#        self.select_boardgame()


    def do_boardgame(self, *args):
        if len(args) == 0:
            print("List of supported boardgames: ")
            print()
            # no argument, just print existing boardgames
            for bg in self.game.data.boardgames:
                print(f"{bg.name} ({bg.alias})")
            print()

        else:
            # argument passed, try to select specified boardgame
            wanted = args[0]
            log.debug(f'looking for >{wanted}<')
            bg = next(bg for bg in self.game.data.boardgames
                      if (bg.name == wanted or bg.alias == wanted))
            print(f"found {bg.name} ({bg.alias})")
