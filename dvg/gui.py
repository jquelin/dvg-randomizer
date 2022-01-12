
import random
from tkinter.ttk import *
from tkinter import *
from tkinter import font
#import tkinter.font as tkFont
import types


from dvg.logger   import log
from dvg.data     import data
from dvg.game     import Game
from dvg.logsheet import generate_pdf

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
        self._create_boardgames()
        self._create_campaigns()
        self._create_campaign_length()
        self._create_pilots()

        # set minimum window size
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        # initialize gui with the first boardgame, and update gui
        # accordingly
        self.vars.boardgame.set(data.boardgames[0].name)
        self.select_boardgame()

    # -- gui creation

    def _create_boardgames(self):
        lf = LabelFrame(self, text=' Board game ', labelanchor=N)
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
        f = Frame(self)
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

        lf = LabelFrame(self, text=' Campaign ', labelanchor=N)

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
    
    def refresh_roaster(self):
        game = self.cur_game

        tv = self.widgets.tv_pilots
        tv.delete(*tv.get_children())

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

    def click_add_replacement_pilot(self):
        newp = self.cur_remaining_pilots.pop(0)
        log.debug(f'adding pilot {newp}')
        if len(self.cur_remaining_pilots) == 0:
            self.widgets.but_add_pilot.configure(state=DISABLED)
        newp.rank = 'replacement'
        self.cur_game.pilots.append(newp)
        self.refresh_roaster()
        log.debug(f'remaining pilots: {len(self.cur_remaining_pilots)}')


    def click_campaign_length(self, length):
        campaign = self.cur_campaign
        clength  = getattr(campaign, length)
        self.cur_clength = clength
        game = Game(self.cur_boardgame, self.cur_campaign, self.cur_clength)
        self.cur_game = game

        squad = clength.pilots
        log.debug(f'generating squad for {length}: {squad}')

        # draw new set of pilots
        available = random.sample(campaign.pilots, len(campaign.pilots))
        selected  = []

        # check if wanting a fixed number of given airplanes
        for allowed, nb in campaign.allowed:
            if nb != '':
                nb = int(nb)
                subset = [a for a in available if a.aircraft.name == allowed]
                random.shuffle(subset)
                log.debug(f'wanting {nb} {allowed} - {len(subset)} available')
                picked = subset[:nb]
                selected.extend(picked)

        remaining = [p for p in available if p not in selected]

        # complete with other airplanes
        nbtotal    = sum(squad)
        nbselected = len(selected)
        log.debug(f'wanting {nbtotal}, already having {nbselected} - {len(remaining)} available')
        random.shuffle(remaining)
        nb = nbtotal-nbselected
        picked = remaining[:nb]
        others = remaining[nb:]
        selected.extend(picked)
        random.shuffle(selected)
        self.cur_remaining_pilots = others

        # assign ranks
        ranks = ['newbie', 'green', 'average', 'skilled', 'veteran', 'legendary']
        for rank, nb in zip(ranks, squad):
            i = nb
            while i>0:
                p = selected.pop(0)
                p.rank = rank
                game.pilots.append(p)
                i -= 1

        self.widgets.but_generate.configure(state=NORMAL)
        self.widgets.but_add_pilot.configure(
            state=NORMAL if len(others)>0 else DISABLED)
        self.refresh_roaster()

    def click_generate_logsheet(self):
        generate_pdf(self.cur_game)

    def close(self, event):
        self.destroy()

    def select_boardgame(self):
        log.debug(f"new boardgame selected: {self.vars.boardgame.get()}")
        self.cur_boardgame = next(bg for bg in data.boardgames if
                                  bg.name == self.vars.boardgame.get())

        tv = self.widgets.tv_campaigns
        tv.delete(*tv.get_children())
        line = 1
        for c in self.cur_boardgame.campaigns:
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


    def select_campaign(self, ev):
        tv = self.widgets.tv_campaigns
        curitem = tv.focus()
        if curitem == "":
            # no item selected - we get there if campaign is selected
            # then a new boardgame is selected
            self.cur_campaign = None
            return
        (box, name, service, year, diff) = tv.item(curitem)['values']
        log.debug(f"campaign {box} - {name} - {service} - {year} selected")

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
