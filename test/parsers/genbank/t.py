# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import os
import bioneb.parsers.genbank as gb
from test.t import *

class rec(object):
    def __init__(self, fname, num=0):
        self.fname = fname
        self.num = num
    def __call__(self, func):
        fname = os.path.join(os.path.dirname(__file__), "data", self.fname)
        def run():
            rec = list(gb.parse(fname, stream_seq=False))[self.num]
            func(rec)
        run.func_name = func.func_name
        return run

class seq(object):
    def __init__(self, fname, stream=False):
        self.fname = fname
        self.stream = stream
    def __call__(self, func):
        fname = os.path.join(os.path.dirname(__file__), "data", self.fname)
        def run():
            func(gb.parse(fname, stream_seq=self.stream))
        run.func_name = func.func_name
        return run            

