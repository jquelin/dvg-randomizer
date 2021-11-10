
from tkinter.ttk import *
from tkinter import *
from tkinter import font
#import tkinter.font as tkFont
import types


from dvg.logger import log
from dvg.data   import data

class GUI(Tk):
    def __init__(self):
        # load boardgames data
#        self.boardgames = boardgame.all_boardgames()

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
        lf = LabelFrame(self, text='Board game', labelanchor=N)
        self.vars.boardgame = StringVar()

        for bg in data.boardgames:
            rb = Radiobutton(
                lf, text=bg.name, value=bg.name,
                variable=self.vars.boardgame,
                command=self.select_boardgame
            )
            rb.pack(side=LEFT)
        lf.pack(padx=20, pady=20)

    def _create_campaign_length(self):
        f = Frame(self)
        self.widgets.f_right = f

        lf = LabelFrame(f, text='Campaign length', labelanchor=N)
        self.widgets.but_length ={}
        for length in ['short', 'medium', 'long']:
            text = f'{length}\nnot available'
            b = Button(lf, text=text, state=DISABLED)
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

        f = Frame(self)
        Label(f, text="Select your campaign", anchor=CENTER).pack(fill=X)

        tv = Treeview(f, columns=headers, height=20, show='headings',
                      selectmode=BROWSE)
        tv.bind('<<TreeviewSelect>>', self.select_campaign)
        tv.tag_configure("odd", background='#EEEEEE')

        for col, longest, anchor in zip(headers, longest, aligns):
            tv.heading(col, text=col, command=lambda c=col:
                       self.sort_campaigns(c, 0))
            # adjust the column's width to the header string
            width = font.nametofont('TkHeadingFont').measure(longest)+10
            tv.column(col, width=width, anchor=anchor)
        tv.pack(side=LEFT, fill=Y)
        vsb = Scrollbar(f, orient="vertical", command=tv.yview)
        vsb.pack(side=LEFT, fill=Y)
        tv.configure(yscrollcommand=vsb.set)

        self.widgets.f_left = f
        self.widgets.tv_campaigns = tv
        f.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

    def _create_pilots(self):
        headers = ['Rank', 'Pilot', 'Aircraft', 'Service', 'Role']
        longest = [
            *list(
                [data.longest[k] for k in ['ranks', 'pilots', 'aircrafts', 'services', 'roles']]
            ), '0000', '****'
        ]

        f = self.widgets.f_right
        style = ttk.Style()
        style.layout("custom.Treeview", [('custom.Treeview.treearea', {'sticky': 'nswe'})])
        style.configure("custom.Treeview.Heading", relief=FLAT)
        tv = Treeview(f, columns=headers, height=20, show='headings',
                      selectmode=NONE, style='custom.Treeview')
        tv.pack(side=TOP, fill=BOTH, expand=True)

        for col, longest in zip(headers, longest):
            tv.heading(col, text=col)
            # adjust the column's width to the header string
            width = font.nametofont('TkHeadingFont').measure(longest)+10
            tv.column(col, width=width)


    # -- private methods
    
        
    # -- events

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
                state=DISABLED, text=text)

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
