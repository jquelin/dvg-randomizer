#!/usr/bin/env python

import argparse
import os
import sys

bindir = os.path.dirname(__file__)
sys.path.append(bindir)

parser = argparse.ArgumentParser(
    prog='randomizer',
    description='What the program does',
    epilog='---')

parser.add_argument('-c', '--console', action='store_true')
args = parser.parse_args()

if args.console:
    from dvg_randomizer.ui.console import UI
    ui = UI()
    ui.cmdloop()

else:
    from dvg_randomizer.ui.graphical import GUI
    ui = GUI()
    ui.mainloop()
