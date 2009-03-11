#  Copyright 2008 New England Biolabs <paul.joseph.davis@gmail.com>

from errors import *
from patterns import *

class GBFeatureParser(object):

    def keys(self):
        for line in self._source:
            # Initialize Feature Key Data
            if line[:1] != " ":
                self._source.undo()
                raise StopIteration
            match = KEY.match(line)
            self._assert(match,
                    "Failed to parse KEY from: '%s'" % line.strip())
            key = {"type": match.group("type").lower()}
        
            # Parse Location
            loc = [match.group("location")]
            loc.extend(self._location_continuation())
            key["location"] = self._location_parse(''.join(loc))
    
            # Add Qualifiers
            for q in self._feature_qualifiers():
                self._assert(q["name"] not in ["type", "location"],
                    "Broken assumption on qualifier names: '%s'" % q["name"])
                curr = key.get(q["name"], None)
                if curr is None:
                    key[q["name"]] = q["value"]
                elif isinstance(curr, list):
                    key[q["name"]].append(q["value"])
                else:
                    key[q["name"]] = [curr, q["value"]]

            yield key
    
    def qualifiers(self):
        for line in self._source:
            match = QUALIFIER.match(line)
            if not match:
                self._source.undo()
                raise StopIteration
            name = match.group("name").lower()
            value = match.group("value")
            if value is None or not value[:1] == '"' or \
                            (value[:1] == '"' and value[-1:] == '"'):
                if isinstance(value, basestring):
                    value = value.strip('"')
                elif value is None:
                    value = True
                yield {"name": name, "value": value}
            else:
                ret = {"name": name, "value": [match.group("value") or ""]}
                for cont in self._feature_continuation():
                    ret["value"].append(cont or "")
                    if cont.endswith('"'):
                        break
                ret["value"] = ' '.join(ret["value"]).strip('"')
                # Hackish as all hell
                if ret["name"].lower() == "translation":
                    ret["value"] = ''.join(ret["value"].split()).upper()
                yield ret

    def continuation(self):
        for line in self._source:
            match = QUAL_CONT.match(line)
            if not match:
                self._source.undo()
                raise StopIteration
            yield match.group("value")
