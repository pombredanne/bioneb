# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import re
import types

import bioneb.sequence.transforms as trans
import gbobj

class LocationError(ValueError):
    pass

def parse(stream, initial):
    loc = ''.join([initial] + parse_continuation(stream))
    try:
        return parse_str(loc)
    except LocationError, inst:
        stream.throw("Failed to parse location: %s\n%s" % (loc, str(inst)))

def parse_continuation(stream):
    ret = []
    for line in stream:
        match = LOC_CONT.match(line)
        if not match:
            stream.undo(line)
            return ret
        ret.append(match.group("value"))
    return ret

def parse_str(loc):
    for re in LOC_FUNCS:
        if not isinstance(loc, str):
            print loc
        match = re[1].match(loc)
        if not match:
            continue
        if re[0] == "single":
            return Single(*match.groups())
        elif re[0] == "accession":
            return loc
        elif "vals" in match.groupdict():
            return __loc_classes__[re[0]](*location_split(match.group("vals")))
        elif "args" in match.groupdict():
            args = []
            if "acc" in match.groupdict():
                args.append(match.group("acc"))
            args.extend(map(parse_str, location_split(match.group("args"))))
            return __loc_classes__[re[0]](*args)
        elif "start" in match.groupdict():
            start, end = match.group("start"), match.group("end")
            return __loc_classes__[re[0]](start, end)
        else:
            fr, to = match.group("from"), match.group("to")
            return __loc_classes__[re[0]](parse_str(fr), parse_str(to))
    raise LocationError("Unable to parse location: '%s'" % loc)

def complement(arg):
    arg["forward"] = False
    return arg

class Location(gbobj.GBObj):
    def __init__(self):
        self["forward"] = True
        self["type"] = self.__class__.__name__.lower()

    def __str__(self):
        raise NotImplementedError()

    def extract(self, seq):
        raise NotImplementedError()

    def fuzzy(self):
        raise NotImplementedError()

    def offset(self, loc):
        raise NotImplementedError()

    def length(self):
        raise NotImplementedError()

class Join(Location):
    def __init__(self, arg1, arg2, *args):
        Location.__init__(self)
        self["locations"] = [arg1, arg2] + list(args)

    def __str__(self):
        ret = "%s(%s)" % (self.type, ','.join(map(str, self["locations"])))
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret
    
    def extract(self, seq):
        ret = ''.join(map(lambda x: x.extract(seq), self.locations))
        if not self.forward:
            return trans.revcomp(ret)
        return ret

    def fuzzy(self):
        start = self.locations[0].fuzzy()[0]
        end = self.locations[-1].fuzzy()[1]
        if not self.forward:
            return (end, start)
        return (start, end)

    def offset(self, loc):
        positions = []
        currlength = 0
        for l in self.locations:
            ret = l.offset(loc)
            for p in ret:
                positions.append((p[0] + currlength, p[1] + currlength))
            currlength += l.length()
        if self.forward:
            return positions
        # Need to reverse everything
        ret = []
        for p in positions[::-1]:
            ret.append((currlength - p[1], currlength - p[0]))
        return ret

class Order(Location):
    def __init__(self, arg1, arg2, *args):
        Location.__init__(self)
        self["locations"] = [arg1, arg2] + list(args)

    def fuzzy(self):
        start = self.locations[0].fuzzy()[0]
        end = self.locations[-1].fuzzy()[1]
        if not self.forward:
            return (end, start)
        return (start, end)

    def __str__(self):
        ret = "%s(%s)" % (self.type, ','.join(map(str, self["locations"])))
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret

class Bond(Location):
    def __init__(self, arg1, arg2):
        Location.__init__(self)
        self["sites"] = [int(arg1)-1, int(arg2)-1]

    def __str__(self):
        ret = "%s(%s)" % (self.type, ','.join(map(str, self["sites"])))
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret

class Gap(Location):
    def __init__(self, arg):
        Location.__init__(self)
        self["length"] = int(arg)-1

    def __str__(self):
        ret = "%s(%s)" % (self.type, self["length"])
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret

    def extract(self, seq):
        return "N" * self.length

    def length(self):
        return self["length"]

class Reference(Location):
    def __init__(self, acc, arg):
        Location.__init__(self)
        self["accession"] = acc
        self["location"] = arg

    def __str__(self):
        ret = "%s:%s" % (self["accession"], self["location"])
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret
    
    def fuzzy(self):
        return self.location.fuzzy()
    
    def offset(self, loc):
        return self.location.offset(loc)
    
    def length(self):
        return self.location.length()

class Site(Location):
    def __init__(self, start, end):
        Location.__init__(self)
        self["start"] = int(start)-1
        self["end"] = int(end)-1

    def __str__(self):
        ret = "%s^%s" % (self["start"], self["end"])
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret

class Choice(Location):
    def __init__(self, start, end):
        Location.__init__(self)
        self["choices"] = [int(start)-1, int(end)-1]

    def __str__(self):
        ret = "%s.%s" % (self["choices"][0], self["choices"][1])
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret

class Span(Location):
    def __init__(self, start, end):
        Location.__init__(self)
        self["start"] = start
        self["end"] = end

    def __str__(self):
        ret = "%s..%s" % (self["start"], self["end"])
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret

    def fuzzy(self):
        start = self.start.fuzzy()
        end = self.end.fuzzy()
        if not self.forward:
            return (end, start)
        return (start, end)        

    def extract(self, seq):
        # end+1 to account for python slice semantics
        ret = seq[self.start.coord:self.end.coord+1]
        if not self.forward:
            return trans.revcomp(ret)
        return ret

    def offset(self, loc):
        if self.type != loc.type:
            return []
        if self.forward != loc.forward:
            return []
        if self.start.coord > loc.start.coord:
            return []
        if self.end.coord < loc.end.coord:
            return []
        if loc.start.coord > loc.end.coord:
            return []
        if self.forward:
            start = loc.start.coord - self.start.coord
            end = loc.end.coord - self.start.coord
        else:
            start = self.end.coord - loc.end.coord
            end = self.end.coord - loc.start.coord
        return [(start, end)]

    def length(self):
        return 1 + (self.end.coord - self.start.coord)

class OneOf(Location):
    def __init__(self, arg1, *args):
        self["type"] = "one-of"
        self["choices"] = [arg1] + list(args)

    def __str__(self):
        return "%s(%s)" % (self["type"], ','.join(map(str, self["choices"])))

class Single(Location):
    def __init__(self, arg):
        self["type"] = "single"
        if arg[:1] in "<>":
            self["fuzzy"] = {"<": "before", ">": "after"}.get(arg[:1])
            self["coord"] = int(arg[1:])-1
        else:
            self["fuzzy"] = False
            self["coord"] = int(arg)-1

    def __str__(self):
        mod = {"before": "<", "after": ">", False: ""}.get(self["fuzzy"])
        return "%s%s" % (mod, self["coord"])

    def fuzzy(self):
        return self["fuzzy"] != False

def location_split(args):
    count = 0
    last = 0
    ret = []
    for i in range(0, len(args)):
        if args[i] == '(':
            count += 1
        elif args[i] == ')':
            count -= 1
        elif args[i] == ',':
            if count == 0:
                ret.append(args[last:i])
                last = i+1
    if count != 0:
        raise LocationError("Unbalanced parenthesis: '%s'" % args)
    ret.append(args[last:])
    return ret

__loc_classes__ = dict([
    (k.lower(), v)
    for (k, v) in globals().copy().iteritems()
    if type(v) == types.TypeType and issubclass(v, Location) and v != Location
])
__loc_classes__["complement"] = complement

LOC_CONT    = re.compile(r"^\s{21}(?!/[^\s=]+(=.+)?$)(?P<value>.+)$")

LOC_FUNCS = [
    ("complement",  re.compile(r"^complement\((?P<args>.*)\)$")),
    ("join",        re.compile(r"^join\((?P<args>.*)\)$")),
    ("order",       re.compile(r"^order\((?P<args>.*)\)$")),
    ("bond",        re.compile(r"^bond\((?P<vals>.*)\)$")),
    ("gap",         re.compile(r"^gap\((?P<vals>\d+)\)$")),
    ("reference",   re.compile(r"^(?P<acc>[^:]+):(?P<args>.*)$")),
    ("site",        re.compile(r"^(?P<start>[^.]*)\^(?P<end>[^.]*)$")),
    ("choice",      re.compile(r"^\(?(?P<start>\d+)\.(?P<end>\d+)\)?$")),
    ("span",        re.compile(r"^(?P<from>.*?)\.\.(?P<to>.*?)$")),
    ("oneof",       re.compile(r"^one-of\((?P<args>.*)\)$")),
    ("single",      re.compile(r"^(?P<single>[<>]?\d+)$")),
    ("accession",   re.compile(r"^[A-Z0-9_]+(\.\d+)?$")),
]

