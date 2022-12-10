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

from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from tkinter import font
import types

from dvg_randomizer.logger   import log

class SquadComposition(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.wm_title('Squad composition')
        self.grab_set()

        self.game = parent.game

        aircrafts = self.game.get_aircraft_possibilities()
        self.possibilities = aircrafts
        self.vars = {}

        l = Label(
            self, font='TkHeadingFont',
            text=f'Choose your squad composition (max {self.game.get_squad_size()}):'
        )
        l.grid(row=0, column=0, columnspan=5, sticky=E+W)
        Label(self).grid(row=1)

        row = 2
        ipad = 2
        self.spinboxes   = {}
        self.label_range = {}
        for aircraft, nbmin, nbmax in aircrafts:
            spinvar = IntVar()
            self.vars[aircraft] = spinvar
            ls = Label(self, text=aircraft.service)
            ln = Label(self, text=aircraft.name, anchor=W)
            lr = Label(self, text=aircraft.role)
            ls.grid(row=row, column=0)
            ln.grid(row=row, column=1, sticky=E+W)
            lr.grid(row=row, column=2)
            spinvar.set(nbmin)
            command = lambda a=aircraft: self.var_changed(a)
            sb = Spinbox(self, from_=nbmin, to=nbmax, width=3,
                        justify=CENTER, textvariable=spinvar,
                         state='readonly', command=command)
            self.spinboxes[aircraft] = sb


            callback = lambda ev, a=aircraft: self.mouse_wheel(ev, a)
            sb.bind("<MouseWheel>", callback)     # windows
            sb.bind("<Button-4>",   callback)       # linux
            sb.bind("<Button-5>",   callback)       # linux

            lrange = Label(self, text=f'[{nbmin}-{nbmax}]', state=DISABLED) # DISABLED for the look :-)
            sb.grid(column=3, row=row, sticky=E+W, padx=ipad, pady=ipad)
            lrange.grid(column=4, row=row, sticky=E+W, padx=ipad, pady=ipad)
            self.label_range[aircraft] = lrange
            row += 1


        Label(self).grid(row=row)

        self.var_random = StringVar()
        l = Label(self, textvariable=self.var_random)
        l.grid(row=row+1, column=0, columnspan=5, sticky=E+W)
        self.label_random = l
        self.update_random_label()

        l = Label(self, text='Unassigned slots will be filled randomly')
        l.grid(row=row+2, column=0, columnspan=5, sticky=E+W)
        Label(self).grid(row=row+3)
        butval = Button(self, text='Validate', command=self.but_validate)
        butval.grid(row=row+4, columnspan=5, sticky=W+E)

        self.resizable(height=False, width=False)
        self.bind('<Return>', self.but_validate)

        # center window
        self.withdraw()
        self.update()
        self.update_idletasks()
        x = parent.winfo_x()
        y = parent.winfo_y()
        dx = int( (parent.winfo_width() - self.winfo_reqwidth())/2 )
        dy = int( (parent.winfo_height() - self.winfo_reqheight())/2 )
        self.geometry(f'+{x+dx}+{y+dy}')
        self.deiconify()


    def flash(self, widget, nb):
        bg = widget.cget("background")
        fg = widget.cget("foreground")
        widget.configure(background=fg, foreground=bg)
        if nb:
            self.after(100, lambda n=nb-1: self.flash(widget, n))

    def but_validate(self):
        self.game.composition = []
        for aircraft, nbmin, nbmax in self.possibilities:
            nb = self.vars[aircraft].get()
            log.debug(f'composition: number of {aircraft}: {nb}')
            self.game.composition.append([aircraft, nb])
        self.destroy()
        self.parent.composition_window_return()

    def mouse_wheel(self, event, aircraft):
        spinvar = self.vars[aircraft]
        curval  = spinvar.get()
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            spinvar.set(curval-1)
        if event.num == 4 or event.delta == 120:
            spinvar.set( spinvar.get()+1 )
        self.var_changed(aircraft)

    def var_changed(self, aircraft):
        curval = self.vars[aircraft].get()
        nbtotal = sum([x.get() for x in self.vars.values()])
        unassigned = self.game.get_squad_size() - nbtotal 
        curmin = self.spinboxes[aircraft].cget('from')
        curmax = self.spinboxes[aircraft].cget('to')
        if unassigned < 0:
            self.vars[aircraft].set(curval-1)
            self.flash(self.label_random, 1)
        elif curval < 0:
            self.vars[aircraft].set(curval+1)
            self.flash(self.label_range[aircraft], 1)
        elif curval < curmin:
            self.vars[aircraft].set(curval+1)
            self.flash(self.label_range[aircraft], 1)
        elif curval > curmax:
            self.vars[aircraft].set(curval-1)
            self.flash(self.label_range[aircraft], 1)

        self.update_random_label()

    def update_random_label(self):
        nbtotal = sum([x.get() for x in self.vars.values()])
        unassigned = self.game.get_squad_size() - nbtotal 
        self.var_random.set( f'total={nbtotal} unassigned={unassigned}')

