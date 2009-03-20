# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import datetime
import re
import time

import gbobj

def parse(stream):
    ret = gbobj.GBObj()

    # Skip leading blank lines.
    for line in stream:
        if line.strip():
            stream.undo(line)
            break

    line = stream.next()
    if not line.startswith("LOCUS"):
        stream.throw("Failed to parse LOCUS line: %s" % line)

    tokens = line[5:].split()

    ret["name"] = tokens[0];
    ret["date"] = datetime.datetime(
        *time.strptime(tokens[-1], "%d-%b-%Y")[0:6]
    )

    if ret["date"] is None:
        stream.throw("Failed to parse locus date: '%s'" % tokens[-1])

    patterns = {
        "length": LENGTH,
        "type": TYPE,
        "molecule_type": MOL_TYPE,
        "strand_type": STRAND_TYPE,
        "division": DIVISION
    }

    for token in tokens[1:-1]:
        curr_name = None
        curr_match = None
        for name, lre in patterns.iteritems():
            match = lre.match(token)
            if curr_match and match:
                stream.throw(
                    "Multiple matches for LOCUS attribute '%s'" % name
                )
            elif match:
                curr_name, curr_match = name, match
        if not curr_match:
            stream.throw("Failed to parse LOCUS token: '%s'" % token)
        if curr_name == "length":
            ret[curr_name] = int(curr_match.group("value"))
        else:
            ret[curr_name] = curr_match.group("value")

    return ret

# Locus Section
LENGTH      = re.compile(r"^(?P<value>\d+)$")
TYPE        = re.compile(r"^(?P<value>(aa|bp))$")
MOL_TYPE    = re.compile(r"""
            ^
            (?P<value>(ss-|ds-|ms-)?
                (
                        NA |  DNA |    RNA |  tRNA | rRNA
                    | mRNA | uRNA |  scRNA | snRNA | snoRNA
                )
            )
            $""", re.VERBOSE)
STRAND_TYPE = re.compile(r"^(?P<value>(linear|circular))$")
DIVISION    = re.compile(r"""
                ^
                (?P<value>
                    (
                          PRI | ROD | MAM | VRT | INV
                        | PLN | BCT | VRL | PHG | SYN
                        | UNA | EST | PAT | STS | GSS
                        | HTG | HTC | ENV | CON
                      )
                )
                $""", re.VERBOSE)
