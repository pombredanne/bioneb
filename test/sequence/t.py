# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import os
import bioneb.parsers.genbank as gb
import bioneb.sequence.transforms as trans
from test.t import *

class gbk(object):
    def __init__(self, fname):
        self.fname = fname
    def __call__(self, func):
        def run():
            fname = os.path.join(os.path.dirname(__file__), "data", self.fname)
            func(gb.parse(fname).next())
        run.func_name = func.func_name
        return run

def seqcmp(mine, ncbi):
    if mine == ncbi:
        return
    eq(len(mine), len(ncbi))
    for idx in range(len(mine)):
        if mine[idx] != ncbi[idx]:
            print "%d %s %s" % (idx, mine[idx], ncbi[idx])