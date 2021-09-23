
import logging
from tkinter.ttk import *
from tkinter import *
from tkinter import font
#import tkinter.font as tkFont


import boardgame

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        logging.debug("create root window")
        self.title('DVG air leader')
        self.bind('<Escape>', self.close)
        self.boardgames = boardgame.all_boardgames()

        self.w = {} # widgets
        self.v = {} # variables

        self._create_boardgames()
        self._create_campaigns()
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        self.v['boardgame'].set(self.boardgames[0].name)
        self.boardgame_selected()

    # -- gui creation

    def _create_boardgames(self):
        lf = LabelFrame(self, text='Board game')
        self.v['boardgame'] = StringVar()
		
        for bg in self.boardgames:
            rb = Radiobutton(
                lf, text=bg.name, value=bg.name,
                variable=self.v['boardgame'],
                command=self.boardgame_selected
            )
            rb.pack(side=LEFT)
        lf.pack(padx=20, pady=20)

    def _create_campaigns(self):
        headers = ['Name', 'Year', 'Difficulty']
        longestc = ''
        for bg in self.boardgames:
            for c in bg.campaigns:
                if len(c.name) > len(longestc):
                    longestc = c.name
        logging.debug(f"longest campaign name: {longestc}")
        longest = [longestc, '0000', '****']


        f = Frame(self, bg='red')
        Label(f, text="Select your campaign",
              anchor=W).pack(fill=X)
        tv = Treeview(f, columns=headers, height=20, show='headings')
        for col, longest in zip(headers, longest):
            tv.heading(col, text=col)
            # adjust the column's width to the header string
            width = font.nametofont('TkHeadingFont').measure(longest)+10
            tv.column(col, width=width)
        tv.pack(side=LEFT, fill=Y)
        vsb = Scrollbar(f, orient="vertical", command=tv.yview)
        vsb.pack(side=LEFT, fill=Y)
        tv.configure(yscrollcommand=vsb.set)

        self.w['campaigns'] = tv

#        campaign = [g.name for g in self.boardgames]
#        vgames = StringVar(value=games)

#        maxlen = max( [len(g) for g in games] )
#        lb = Listbox(f, listvariable=vgames, height=5, width=maxlen)
#        lb.pack()
#        lb.select_set(0)

        f.pack(expand=True, fill=BOTH)

    # -- private methods
    
        
    # -- events

    def boardgame_selected(self):
        logging.debug(f"new boardgame selected: {self.v['boardgame'].get()}")
        self.cur_boardgame = next(bg for bg in self.boardgames if
                                  bg.name == self.v['boardgame'].get())

        tv = self.w['campaigns']
        tv.delete(*tv.get_children())
        for c in self.cur_boardgame.campaigns:
            tv.insert('', END, values=[c.name, c.year, "*"*c.level])
#        logging.debug(f"new boardgame selected: {self.cur_boardgame.name} - {self.cur_boardgame.year}")

    def close(self, event):
        self.destroy()


