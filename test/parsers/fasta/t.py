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
