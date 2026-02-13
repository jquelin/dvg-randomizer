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

import platform
import tkinter as tk
from tkinter import ttk

class ScrolledFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        # Create a canvas and place a frame on it, then use the canvas to
        # scroll the frame when needed.
        # The frame will hold the child widgets, and the canvas will provide a
        # scrollable view of it.
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.inner = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window(
            (4,4), window=self.inner, anchor="nw")

        # Bind events to make sure the scrollable region is always large enough
        # to encompass the inner frame
        self.inner.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind mouse wheel events to scroll the canvas when the cursor is over
        # the inner frame.
        self.inner.bind('<Enter>', self.on_enter)
        self.inner.bind('<Leave>', self.on_leave)

        # Perform an initial stretch on render, otherwise the scroll region has
        # a tiny border until the first resize.
        self.on_frame_configure(None)


    def on_frame_configure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        # When the inner frame changes size, alter the scroll region
        # respectively.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def on_canvas_configure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        # Whenever the size of the canvas changes, alter the window region
        # respectively.
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)

    def on_mouse_wheel(self, event):
        # cross platform scroll wheel event
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )


    def on_enter(self, event):
        # Bind wheel events when the cursor enters the control.
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)


    def on_leave(self, event):
        # Unbind wheel events when the cursor leaves the control.
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
