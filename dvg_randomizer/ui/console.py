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
from cmd2.table_creator import HorizontalAlignment
import random
#import tkinter.font as tkFont
import types


from dvg_randomizer.common   import log
from dvg_randomizer.game     import Game
from dvg_randomizer.logsheet import generate_pdf
from dvg_randomizer.ui.base  import UI


class ConsoleUI(cmd2.Cmd, UI):

    # --- constructor

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

        UI.__init__(self)

        # initialize gui with the first boardgame, and update gui
        # accordingly
        self._select_boardgame(self.game.data.boardgames[0])
        self._set_prompt()


    # --- cmd2 actions

    def do_boardgame(self, statement):
        if len(statement.argv) == 1:
            # no argument passed, just list supported boardgames
            self._display_table(
                ('Name', 'Alias'),
                [(bg.name, bg.alias) for bg in self.game.data.boardgames],
                (HorizontalAlignment.LEFT, HorizontalAlignment.CENTER)
            )

        else:
            # argument passed, try to select specified boardgame
            wanted = statement.argv[1]
            bg = next((bg for bg in self.game.data.boardgames
                      if bg.name == wanted or bg.alias == wanted), None)
            if bg is None:
                self.perror(f"Boardgame {wanted} not found.")
            else:
                self.poutput(f"Found {bg.name} ({bg.alias}).")
                self._select_boardgame(bg)

    def complete_boardgame(self, text, line, begidx, endidx):
        all_bg_names = [bg.name for bg in self.game.data.boardgames]
        return self.basic_complete(text, line, begidx, endidx,
                sorted(all_bg_names))

    # --- helper methods

    def _display_table(self, headers, data, alignment=None):
        columns = []
        for i in range(0, len(headers)):
            widths = [len(el[i]) for el in data]
            widths.append(len(headers[i]))
            align = HorizontalAlignment.LEFT if alignment is None else alignment[i]
            newcol = cmd2.table_creator.Column(
                headers[i],
                width=max(widths),
                header_horiz_align=align,
                data_horiz_align=align
            )
            columns.append(newcol)
        table = cmd2.table_creator.AlternatingTable(columns,
                                                    column_borders=False)
        self.poutput(table.generate_table(data))

    def _display_campaigns(self):
        left   = HorizontalAlignment.LEFT
        right  = HorizontalAlignment.RIGHT
        center = HorizontalAlignment.CENTER
        self._display_table(
            ('Box', 'Name', 'Service', 'Year', 'Difficulty'),
            [(c.box, c.name, c.service, str(c.year), '*'*c.level) for c in
             self.game.campaigns()],
            (center, left, left, center, left)
        )

    def _select_boardgame(self, bg):
        self.game.do_boardgame(bg)
        self._set_prompt()
        self._display_campaigns()


    def _set_prompt(self):
        prompt = ''
        if self.game.boardgame is not None:
            prompt = f'[{self.game.boardgame.name}]'

        prompt +=  'dvg: '
        self.prompt = cmd2.ansi.style(prompt,
                fg=cmd2.Fg.LIGHT_GREEN)
