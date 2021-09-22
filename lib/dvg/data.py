

#from importlib.resources import files
# Reads contents with UTF-8 encoding and returns str.
#eml = files('email.tests.data').joinpath('message.eml').read_text()

import pkg_resources

import pkgutil
data = pkgutil.get_data('data', 'games.csv')
print(data)


import os
import logging

bindir  = os.path.dirname(__file__)
datadir = os.path.join(bindir, "data")
logging.info(f"datadir={datadir}")

import data

class Data:
    def get(self):
#        filepath = pkg_resources.resource_filename('data.zl', 'games.csv')
#        print(open(filepath).readlines())
        filepath = pkg_resources.resource_filename('data', 'games.csv')
        print(open(filepath).readlines())
    def foo(self):
        print("foo")
