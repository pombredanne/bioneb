# Copyright 2008 New England Biolabs <davisp@neb.com>

import bioneb.parsers.utils as utils

from errors import *
from patterns import *

class Parser(utils.Parser):
    def parse(self):
        self.data = {}

        line = self.stream.next()
        match = KEYWORD.match(line)
        gb_assert(match, "Failed to parse LOCUS line: %s" % line)
        key = match.group("name")
        value = match.group("value")
        tokens = kw["value"].split()

        self.data["name"] = tokens[0];
        self.data["date"] = datetime.datetime(
            *time.strptime(tokens[-1], "%d-%b-%Y")[0:6]
        )

        gb_assert(
            self.data["date"] is not None,
            "Failed to parse locus date: '%s'" % tokens[-1]
        )

        for token in tokens[1:-1]:
            curr_name = None
            curr_match = None
            for name, lre in self.patterns.iteritems():
                match = lre.match(token)
                if curr_match and match:
                    gb_raise(
                        "Multiple matches for LOCUS attribute '%s'" % name
                    )
                elif match:
                    curr_name, curr_match = name, match
            self._assert(
                curr_match,
                "Failed to parse LOCUS token: '%s'" % token
            )
            if curr_name == "length":
                self.data[curr_name] = int(curr_match.group("value"))
            else:
                self.data[curr_name] = curr_match.group("value")

class GBLocus(dict):
    def __init__(self, *args, **kwargs):
        super(GBLocus, self).__init__(*args, **kwargs)

    length = property(
        lambda: self.data.get("length"),
        doc="Length of the molecule"
    )

    type = property(
        lambda: self.data.get("type"),
        doc="Basepair type."
    )

    molecule_type = property(
        lambda: self.data.get("molecule_type"),
        doc="Molecule type. DNA, RNA, mRNA, etc."
    )

    circular = property(
        lambda: self.data.get("strand_type") == "circular",
        doc="Return if this is a circular molecule."
    )

    division = property(
        lambda: self.data.get("division"),
        doc="Genbank division"
    )
