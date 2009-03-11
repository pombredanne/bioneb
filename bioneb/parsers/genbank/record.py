
import bioneb.parsers.utils as utils

import locus
import info
import features
import sequence

def parse(stream):
    loc = locus.parse(stream)
    info = info.parse(stream)
    features = features.parse(stream)
    if loc.division == "CON":
        return GBContigRecord(loc)
    else:
        return GBSequenceRecord(loc)

class GBRecord(object):
    def __init__(self, locus):
        self.locus = locus
    
    def parse(self, stream):
        pass


class GBSequenceRecord(object):
    def __init__(self, locus):
        super(GBSequenceRecord, self).__init__(locus)

class GBContigRecord(object):
    def __init__(self, locus):
        super(GBContigRecord, self).__init__(locus)

