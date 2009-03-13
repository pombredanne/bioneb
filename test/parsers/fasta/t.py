# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#

import os
import bioneb.parsers.fasta as fa
from test.t import *

class seq(object):
    def __init__(self, fname, num=None, **kwargs):
        self.fname = fname
        self.num = num
        self.kwargs = kwargs
    def __call__(self, func):
        fname = os.path.join(os.path.dirname(__file__), "data", self.fname)
        def run():
            rec = fa.parse(fname, **self.kwargs)
            if self.num is not None:
                rec = list(rec)[self.num]
            func(rec)
        run.func_name = func.func_name
        return run
