#!/usr/bin/env python

import os
import sys

bindir = os.path.dirname(__file__)
sys.path.append(bindir)

from dvg_randomizer.ui.graphical import GUI
ui = GUI()
ui.mainloop()
