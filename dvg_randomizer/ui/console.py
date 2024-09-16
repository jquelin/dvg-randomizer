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


    def do_boardgame(self, statement):
#        fg_choices = [c.name.lower() for c in cmd2.Fg]
#        bg_choices = [c.name.lower() for c in cmd2.Bg]
#        self.poutput(fg_choices)
#        self.poutput(bg_choices)
        if len(statement.argv) == 1:
            all_outputs = [f"{bg.name} ({bg.alias})" for bg in self.game.data.boardgames]
            max_width = max([len(s) for s in all_outputs])
#            self.poutput('Supported boardgames')
#            self.poutput('-' * max_width)
            title = 'Supported boardgames' + ' ' * max_width
            title = title[0:max_width]
            self.poutput(cmd2.ansi.style(title,
                                         underline=True))
            for output in all_outputs:
                self.poutput(output)
            self.poutput()

#            bg_color = cmd2.ansi.RgbBg(174,161,200)
#            fg_color = cmd2.ansi.RgbFg(97,48,101)
#            output_str = cmd2.ansi.style(
#                    "Supported boardgames",
#                    bold=True)
#            self.poutput(output_str)
#            self.poutput("List of supported boardgames: ")
#            self.poutput()
            # no argument, just print existing boardgames
#            for bg in self.game.data.boardgames:
#                self.poutput(f"{bg.name} ({bg.alias})")
#            self.poutput()

        else:
            # argument passed, try to select specified boardgame
            wanted = statement.argv[1]
            log.debug(f'looking for >{wanted}<')
            bg = next(bg for bg in self.game.data.boardgames
                      if (bg.name == wanted or bg.alias == wanted))
            self.poutput(f"found {bg.name} ({bg.alias})")

    def complete_boardgame(self, text, line, begidx, endidx):
        all_bg_names = [bg.name for bg in self.game.data.boardgames]
        return self.basic_complete(text, line, begidx, endidx,
                sorted(all_bg_names))

