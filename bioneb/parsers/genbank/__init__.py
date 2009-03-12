# Copyright 2008 New England Biolabs <davisp@neb.com>
"Genbank Parser"

import re

import bioneb.parsers.stream as stream
import locus
import info
import features
import gbobj

def parse(filename=None, handle=None, stream_seq=False):
    handle = stream.Stream(filename, handle)
    while True:
        loc = locus.parse(handle)
        if loc.division == "CON":
            yield GBContigRecord(handle, loc)
        else:
            yield GBSequenceRecord(handle, loc, stream_seq)

class GBRecord(gbobj.GBObj):
    def __init__(self, stream, locus):
        self["locus"] = locus
        self["info"] = info.parse(stream)
        self["features"] = features.parse(stream)

class GBSequenceRecord(GBRecord):
    def __init__(self, stream, locus, stream_seq):
        GBRecord.__init__(self, stream, locus)

        self["counts"] = {}        
        keywords = info.parse(stream)
        if len(keywords) == 1 and "base count" in keywords:
            self["counts"] = keywords["base count"]
        elif len(keywords) != 0:
            stream.throw("Invalid info parsed: %s" % keywords)

        line = iter(stream).next()
        if line.strip() != "ORIGIN":
            stream.throw("Invalid ORIGIN line: %s" % line.strip())
        
        self.stream = stream
        if not stream_seq:
            self["sequence"] = ''.join(list(iter(self)))

    def __iter__(self):
        if self.stream is None:
            raise ValueError("Stream has been exhausted.")
        return self
    
    def next(self):
        try:
            line = self.stream.next()
            if line[:1] == " ":
                return ''.join(line.split()[1:]).upper()
            elif line == "//\n":
                raise StopIteration()
            else:
                self.stream.throw("Invalid trailing line: %s" % line.strip())
        except StopIteration:
            self.stream = None
            raise

class GBContigRecord(GBRecord):
    def __init__(self, stream, locus):
        GBRecord.__init__(self, stream, locus)

        self["location"] = None
        keywords = info.parse(stream)
        if len(keywords) == 1 and "contig" in keywords:
            self["location"] = keywords["contig"]
        elif len(keywords) != 0:
            stream.throw("Invalid info parsed: %s" % keywords)
        
        line = stream.next().strip()
        if line != "//":
            stream.throw("Unexpected data after CONTIG: %s" % line)

