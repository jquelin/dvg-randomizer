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


import random
from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from tkinter import font
#import tkinter.font as tkFont
import types


from dvg.logger   import log
from dvg.data     import data
from dvg.game     import Game
from dvg.logsheet import generate_pdf
import gui.composition

class GUI(Tk):
    def __init__(self):
        # a convenient way to store our vars
        self.vars    = types.SimpleNamespace() # gui vars (StringVar)
        self.widgets = types.SimpleNamespace() # widgets

        # gui creation
        log.debug("create root window")
        Tk.__init__(self)
        self.title('DVG air leader')
        self.bind('<Escape>', self.close)

        f = types.SimpleNamespace()
        self.widgets.frames = f
        f.top   = Frame(self)
        f.left  = Frame(self)
        f.right = Frame(self)

        self._create_boardgames()
        self._create_expansions()
        self._create_campaigns()
        self._create_campaign_length()
        self._create_pilots()

        self.cur_game = Game()

        f.top.pack(side=TOP)
        f.left.pack(side=LEFT,  fill=Y)
        f.right.pack(side=LEFT, expand=True, fill=BOTH)

        # set minimum window size
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        # initialize gui with the first boardgame, and update gui
        # accordingly
        self.vars.boardgame.set(data.boardgames[0].name)
        self.select_boardgame()

    # -- gui creation

    def _create_boardgames(self):
        lf = LabelFrame(self.widgets.frames.top, text=' Board game ', labelanchor=N)
        self.vars.boardgame = StringVar()

        for bg in data.boardgames:
            rb = Radiobutton(
                lf, text=bg.name, value=bg.name,
                variable=self.vars.boardgame,
                command=self.select_boardgame
            )
            rb.pack(side=LEFT)
        lf.pack(padx=15, pady=15, ipadx=15, ipady=15)

    def _create_campaign_length(self):
        f = Frame(self.widgets.frames.right)
        self.widgets.f_right = f

        lf = LabelFrame(f, text=' Campaign length ', labelanchor=N)
        self.widgets.but_length ={}
        for length in ['short', 'medium', 'long']:
            text = f'{length}\nnot available'
            b = Button(lf, text=text, state=DISABLED,
                       command=lambda l=length: self.click_campaign_length(l))
            b.pack(side=LEFT, padx=5, pady=5, expand=True, fill=BOTH)
            self.widgets.but_length[length] = b

        lf.pack(side=TOP, fill=X, padx=5, pady=5)
        self.widgets.lf_campaign_length = lf
        f.pack(side=LEFT, expand=True, fill=BOTH)


    def _create_campaigns(self):
        headers = ['Box', 'Name', 'Service', 'Year', 'Difficulty']
        longest = [
            *list(
                [data.longest[k] for k in ['boxes', 'campaigns', 'services']]
            ), '0000', '****'
        ]
        aligns  = [CENTER, W, CENTER, CENTER, CENTER]

        lf = LabelFrame(self.widgets.frames.left, text=' Campaign ', labelanchor=N)

        tv = Treeview(lf, columns=headers, height=20, show='headings',
                      selectmode=BROWSE)
        tv.bind('<<TreeviewSelect>>', self.select_campaign)
        tv.bind('<Button-1>', self.tv_campaigns_click)

        tv.tag_configure("odd", background='#EEEEEE')

        for col, longest, anchor in zip(headers, longest, aligns):
            tv.heading(col, text=col, command=lambda c=col:
                       self.sort_campaigns(c, 0))
            # adjust the column's width to the header string
            width = font.nametofont('TkHeadingFont').measure(longest)+10
            tv.column(col, width=width, anchor=anchor)
        tv.pack(side=LEFT, fill=Y)
        vsb = Scrollbar(lf, orient="vertical", command=tv.yview)
        vsb.pack(side=LEFT, fill=Y)
        tv.configure(yscrollcommand=vsb.set)

        lf.pack(side=LEFT, fill=BOTH, padx=5, pady=5, ipadx=5, ipady=5)
        self.widgets.tv_campaigns = tv

    def _create_expansions(self):
        f = Frame(self.widgets.frames.left)
        f.pack(side=TOP, fill=X)
        self.widgets.frames.expansions = f

    def _create_pilots(self):
        headers = ['Rank', 'Pilot', 'Aircraft', 'Service', 'Role', 'SO']
        anchors = [CENTER, W, CENTER, CENTER, CENTER, CENTER]
        longest = [
            *list(
                [data.longest[k] for k in ['ranks', 'pilots', 'aircrafts', 'services', 'roles']]
            ), 'Cost'
        ]

        f = self.widgets.f_right

        # change pilots treeview style
        style = ttk.Style()
        grey = self.cget('bg')
        style.layout("custom.Treeview", [('custom.Treeview.treearea', {'sticky': 'nswe'})])
        style.configure(
            "custom.Treeview.Heading",
            relief=FLAT,
        )
        style.configure(
            "custom.Treeview",
            highlightthickness=0,
            bd=0,
            fieldbackground=grey,
            background=grey
        )
        style.map(
            "custom.Treeview.Heading",
            background=[('pressed', grey), ('!pressed', grey)]
        )


        tv = Treeview(f, columns=headers, height=20, show='headings',
                      selectmode=NONE, style='custom.Treeview')
        tv.bind('<Button-1>', self.tv_pilots_click)

        tv.tag_configure('newbie',    background='#fff3cd', foreground='#665d03')
        tv.tag_configure('green',     background='#d1e7dd', foreground='#055160')
        tv.tag_configure('average',   background='#cfe2ff', foreground='#084298')
        tv.tag_configure('skilled',   background='#f8d7da', foreground='#842029')
#        tv.tag_configure('veteran',   background='#aea1c8', foreground='#8750cf')
        tv.tag_configure('veteran',   background='#aea1c8', foreground='#613065')
        tv.tag_configure('legendary', background='#c3c3c3', foreground='#333333')
        tv.tag_configure('ace',       background='#141619', foreground='#d3d3d4')

        for col, longest, anchor in zip(headers, longest, anchors):
            tv.heading(col, text=col)
            # adjust the column's width to the header string
            width = font.nametofont('TkHeadingFont').measure(longest)+10
            tv.column(col, width=width, anchor=anchor)


        self.widgets.tv_pilots = tv
        tv.pack(side=TOP, fill=BOTH, padx=5, expand=True)

        # create button to generate logsheet
        fb = Frame(f, bg='yellow')
        b = Button(fb, text='Generate campaign log sheet',
                   command=self.click_generate_logsheet,
                   state=DISABLED)
        b.pack(side=LEFT, fill=X, expand=True)
        self.widgets.but_generate = b
        b = Button(fb, text='Add replacement pilot',
                   command=self.click_add_replacement_pilot,
                   state=DISABLED)
        b.pack(side=LEFT, fill=X, expand=True)
        self.widgets.but_add_pilot = b
        fb.pack(side=TOP, fill=X)

    # -- private methods
    
    def refresh_campaigns(self):
        log.debug('refreshing campaigns')
        tv = self.widgets.tv_campaigns
        tv.delete(*tv.get_children())
        line = 1
        for c in self.cur_game.campaigns():
            if line % 2 == 0:
                tags = []
            else:
                tags = ['odd']
            tv.insert('', END, values=[c.box, c.name, c.service, c.year,
                                       "*"*c.level], tags=(tags))
            line += 1
#        logger.debug(f"new boardgame selected: {self.cur_boardgame.name} - {self.cur_boardgame.year}")

        for c in self.widgets.lf_campaign_length.winfo_children():
            c.config(state=DISABLED)

        self.cur_game.campaign = None
        self.refresh_roaster()



    def refresh_roaster(self):
        game = self.cur_game

        tv = self.widgets.tv_pilots
        tv.delete(*tv.get_children())

        if game.campaign is None:
            self.widgets.but_add_pilot.configure(state=DISABLED)
            self.widgets.but_generate.configure(state=DISABLED)

        else:
            for p in game.pilots:
                so_bonus = p.so_bonus(game)
                if so_bonus == 0:
                    so_bonus = '-'
                else:
                    so_bonus = f'{so_bonus:+d}'
                tv.insert(
                    '', END, tags=(p.rank),
                    values=[p.rank, p.elite_name, p.aircraft.name, p.service,
                            p.aircraft.role, so_bonus]
                )

        
    # -- events

    def check_expansion(self, box):
        cbvars = self.vars.cbvars
        if box == 'core':
            cbvars[box].set(True)
        else:
            if cbvars[box].get():
                self.cur_game.boxes.add(box)
            else:
                self.cur_game.boxes.remove(box)
        log.debug(f'click on box {box} (selected={self.cur_game.boxes}')
        self.refresh_campaigns()


    def click_add_replacement_pilot(self):
        newp = self.cur_game.remaining_pilots.pop(0)
        log.info(f'adding pilot {newp}')
        if len(self.cur_game.remaining_pilots) == 0:
            self.widgets.but_add_pilot.configure(state=DISABLED)
        newp.rank = 'replacement'
        self.cur_game.pilots.append(newp)
        self.refresh_roaster()
        log.debug(f'remaining pilots: {len(self.cur_game.remaining_pilots)}')


    def click_campaign_length(self, length):
        log.debug(f'clicked on campaign length {length}')

        campaign = self.cur_campaign
        clength  = getattr(campaign, length)
        self.cur_clength = clength
        game = self.cur_game
        game.set_campaign(self.cur_campaign, self.cur_clength)
        if 1:
            gui.composition.SquadComposition(self)
        else:
            self.composition_window_return()

    def composition_window_return(self):
        game = self.cur_game
        game.draw_roaster()
        self.widgets.but_generate.configure(state=NORMAL)
        self.widgets.but_add_pilot.configure(
            state=NORMAL if len(game.remaining_pilots)>0 else DISABLED)
        self.refresh_roaster()

    def click_generate_logsheet(self):
        generate_pdf(self.cur_game)

    def close(self, event):
        self.destroy()

    def select_boardgame(self):
        bg_name = self.vars.boardgame.get()
        log.debug(f"new boardgame selected: {bg_name}")
        bg = next(bg for bg in data.boardgames if bg.name == self.vars.boardgame.get())
        self.cur_boardgame = bg
        log.debug(f'boardgame {bg} found')
        self.cur_game.do_boardgame(bg)

        fexp = self.widgets.frames.expansions
        for c in fexp.winfo_children(): c.destroy()
        Label(fexp, text='Expansions:', font='TkHeadingFont').pack(side=LEFT)
        cbvars = {}
        for box in self.cur_boardgame.boxes():
            cbvar = BooleanVar(value=True)
            cbvars[box] = cbvar
            cb = Checkbutton(
                fexp, text=box, variable=cbvar,
                command=lambda b=box: self.check_expansion(b)
            )
#            if box == 'core': cb.configure(state=DISABLED)
            cb.pack(side=LEFT)
        self.vars.cbvars = cbvars

        self.refresh_campaigns()



    def select_campaign(self, ev):
        tv = self.widgets.tv_campaigns
        curitem = tv.focus()
        if curitem == "":
            # no item selected - we get there if campaign is selected
            # then a new boardgame is selected
            self.cur_campaign = None
            return
        (box, name, service, year, diff) = tv.item(curitem)['values']
        log.info(f"campaign {box} - {name} - {service} - {year} selected")

        self.cur_campaign = self.cur_boardgame.campaign(name, year, service)

        lf = self.widgets.lf_campaign_length
        for length in ['short', 'medium', 'long']:
            text = f'{length}\nnot available'
            self.widgets.but_length[length].configure(
                state=DISABLED, text=text
            )

        for length in self.cur_campaign.lengths:
            days  = length.days
            so    = length.so
            label = length.label
            text  = f"{label}\n{days} days, {so} SO"
            self.widgets.but_length[label].configure(state=NORMAL, text=text)

        self.cur_game.campaign = None
        self.refresh_roaster()


    def sort_campaigns(self, col, descending):
        """Sort campaigns tree contents when a column header is clicked on."""
        log.debug(f"sorting campaigns by {col}")
        tv = self.widgets.tv_campaigns

        # grab values to sort
        data = [(tv.set(child, col), child) for child in tv.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tv.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tv.heading(col, command=lambda col=col: self.sort_campaigns(col, int(not descending)))

    def tv_campaigns_click(self, ev):
        # prevent column resizing
         if self.widgets.tv_campaigns.identify_region(ev.x, ev.y) == "separator":
             return "break"

    def tv_pilots_click(self, ev):
        # prevent column resizing
         if self.widgets.tv_pilots.identify_region(ev.x, ev.y) == "separator":
             return "break"
