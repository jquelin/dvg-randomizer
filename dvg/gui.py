
from log import logger
from tkinter.ttk import *
from tkinter import *
from tkinter import font
#import tkinter.font as tkFont
import types


import boardgame

class GUI(Tk):
    def __init__(self):
        # load boardgames data
#        self.boardgames = boardgame.all_boardgames()

        # a convenient way to store our vars
        self.vars    = types.SimpleNamespace() # gui vars (StringVar)
        self.widgets = types.SimpleNamespace() # widgets

        # gui creation
        logger.debug("create root window")
        Tk.__init__(self)
        self.title('DVG air leader')
        self.bind('<Escape>', self.close)
        self._create_boardgames()
        self._create_campaigns()
        self._create_campaign_length()
        self._create_button()

        # set minimum window size
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        # initialize gui with the first boardgame, and update gui
        # accordingly
        self.vars.boardgame.set(self.boardgames[0].name)
        self.select_boardgame()

    # -- gui creation

    def _create_boardgames(self):
        lf = LabelFrame(self, text='Board game')
        self.vars.boardgame = StringVar()

        for bg in self.boardgames:
            rb = Radiobutton(
                lf, text=bg.name, value=bg.name,
                variable=self.vars.boardgame,
                command=self.select_boardgame
            )
            rb.pack(side=LEFT)
        lf.pack(padx=20, pady=20)

    def _create_button(self):
        f = self.widgets.f_campaigns
        b = Button(f, text="Create random squad")
        b.pack(side=TOP, fill=X)

    def _create_campaign_length(self):
        f = self.widgets.f_campaigns

        lf = LabelFrame(f, text='Campaign length')
        self.vars.campaign_length = StringVar()
        for length in ['short', 'medium', 'long']:
            rb = Radiobutton(
                lf, text=length, value=length,
                variable=self.vars.campaign_length,
                state=DISABLED
            )
            rb.pack(side=LEFT)

        lf.pack(side=TOP, fill=X, padx=5, pady=5)
        self.widgets.lf_campaign_length = lf
        self.vars.campaign_length.set('short')


    def _create_campaigns(self):
        headers = ['Name', 'Year', 'Difficulty']
        longestc = ''
        for bg in self.boardgames:
            for c in bg.campaigns:
                if len(c.name) > len(longestc):
                    longestc = c.name
        logger.debug(f"longest campaign name: {longestc}")
        longest = [longestc, '0000', '****']

        f = Frame(self)#, bg='red')
        Label(f, text="Select your campaign",
              anchor=W).pack(fill=X)
        tv = Treeview(f, columns=headers, height=20, show='headings',
                      selectmode=BROWSE)
        tv.bind('<<TreeviewSelect>>', self.select_campaign)
        for col, longest in zip(headers, longest):
            tv.heading(col, text=col, command=lambda c=col:
                       self.sort_campaigns(c, 0))
            # adjust the column's width to the header string
            width = font.nametofont('TkHeadingFont').measure(longest)+10
            tv.column(col, width=width)
        tv.pack(side=LEFT, fill=Y)
        vsb = Scrollbar(f, orient="vertical", command=tv.yview)
        vsb.pack(side=LEFT, fill=Y)
        tv.configure(yscrollcommand=vsb.set)

        self.widgets.f_campaigns = f
        self.widgets.tv_campaigns = tv

#        campaign = [g.name for g in self.boardgames]
#        vgames = StringVar(value=games)

#        maxlen = max( [len(g) for g in games] )
#        lb = Listbox(f, listvariable=vgames, height=5, width=maxlen)
#        lb.pack()
#        lb.select_set(0)

        f.pack(expand=True, fill=BOTH)

    # -- private methods
    
        
    # -- events

    def close(self, event):
        self.destroy()

    def select_boardgame(self):
        logger.debug(f"new boardgame selected: {self.vars.boardgame.get()}")
        self.cur_boardgame = next(bg for bg in self.boardgames if
                                  bg.name == self.vars.boardgame.get())

        tv = self.widgets.tv_campaigns
        tv.delete(*tv.get_children())
        for c in self.cur_boardgame.campaigns:
            tv.insert('', END, values=[c.name, c.year, "*"*c.level])
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
        (name, year, diff) = tv.item(curitem)['values']
        logger.debug(f"campaign {name} - {year} selected)")

        self.cur_campaign = self.cur_boardgame.find_campaign(name, year)

        lf = self.widgets.lf_campaign_length
        for child in lf.winfo_children():
            child.destroy()

        for length in self.cur_campaign.lengths:
            days  = length.days
            so    = length.so
            label = length.label
            rb = Radiobutton(
                lf, text=f"{label}\n{days} days, {so} SO", value=label,
                justify=LEFT,
                variable=self.vars.campaign_length,
            )
            rb.pack(side=LEFT)


    def select_campaign_length(self):
        if self.campaign is None:
            return
        pass

    def sort_campaigns(self, col, descending):
        """Sort campaigns tree contents when a column header is clicked on."""
        logger.debug(f"sorting campaigns by {col}")
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
