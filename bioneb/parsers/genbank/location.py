# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import re
import types

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

class Join(Location):
    def __init__(self, arg1, arg2, *args):
        Location.__init__(self)
        self["locations"] = [arg1, arg2] + list(args)

    def __str__(self):
        ret = "%s(%s)" % (self.type, ','.join(map(str, self["locations"])))
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret

class Order(Location):
    def __init__(self, arg1, arg2, *args):
        Location.__init__(self)
        self["locations"] = [arg1, arg2] + list(args)

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

class Reference(Location):
    def __init__(self, acc, arg):
        self["type"] = "reference"
        self["accession"] = acc
        self["location"] = arg

    def __str__(self):
        ret = "%s:%s" % (self["accession"], self["location"])
        if not self["forward"]:
            ret = "complement(%s)" % ret
        return ret

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

