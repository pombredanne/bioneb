#  Copyright 2008 New England Biolabs <paul.joseph.davis@gmail.com>

import re

import gbobj
import location

def parse(stream):
    line = iter(stream).next()
    if not FEATURES.match(line):
        stream.throw("Invalid Features header: %s" % line.strip())
    
    ret = []
    for line in stream:
        # Initialize Feature Key Data
        if line[:1] != " ":
            stream.undo(line)
            return ret

        match = KEY.match(line)
        if not match:
            stream.throw("Failed to parse KEY from: '%s'" % line.strip())

        key = gbobj.GBObj({
            "type": match.group("type").lower(),
            "location": location.parse(stream, match.group("location"))
        })

        for q in parse_qualifiers(stream):
            if q["name"] in ["type", "location"]:
                stream.throw("Invalid qualifier name: '%s'" % q["name"])
            curr = key.get(q["name"], None)
            if curr is None:
                key[q["name"]] = q["value"]
            elif isinstance(curr, list):
                key[q["name"]].append(q["value"])
            else:
                key[q["name"]] = [curr, q["value"]]
        ret.append(key)
    return ret
    
def parse_qualifiers(stream):
    ret = []
    for line in stream:
        match = QUALIFIER.match(line)
        if not match:
            stream.undo(line)
            return ret
        name = match.group("name").lower()
        value = match.group("value")
        if value is None or not value[:1] == '"' or \
                        (value[:1] == '"' and value[-1:] == '"'):
            if isinstance(value, basestring):
                value = value.strip('"')
            elif value is None:
                value = True
            ret.append({"name": name, "value": value})
        else:
            q = gbobj.GBObj({
                "name": name,
                "value": [match.group("value") or ""]
            })
            q["value"].extend(parse_continuation(stream))
            q["value"] = ' '.join(q["value"]).strip('"')
            # Hackish as all hell
            if q["name"].lower() == "translation":
                q["value"] = ''.join(q["value"].split()).upper()
            ret.append(q)

def parse_continuation(stream):
    ret = []
    for line in stream:
        match = QUAL_CONT.match(line)
        if not match:
            stream.undo(line)
            return ret
        ret.append(match.group("value"))
        if ret[-1].endswith('"'):
            break
    return ret

FEATURES    = re.compile(r"^FEATURES\s+Location/Qualifiers$")
KEY         = re.compile(r"^\s{5}(?P<type>\S+)\s+(?P<location>\S.*)$")
QUALIFIER   = re.compile(r"^\s{21}/(?P<name>[^\s=]+)(=(?P<value>.+))?$")
QUAL_CONT   = re.compile(r"^\s{21}(?P<value>.*)$")
