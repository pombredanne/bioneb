# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import re

import gbobj
import location
import bioneb.sequence as bioseq

class Feature(gbobj.GBObj):
    def extract(self, sequence):
        try:
            return self.location.extract(sequence)
        except NotImplementedError:
            raise ValueError("Unable to extract location: %s" % self.location)

    def translate(self, sequence):
        if self.type != "cds":
            raise ValueError("Failed to translate type: %s" % self.type)
        try:
            dna = self.location.extract(sequence)
        except NotImplementedError:
            raise ValueError("Unable to extract location: %s" % self.location)
        mods = []
        try:
            if hasattr(self, "transl_except"):
                positions = [
                    (self.location.offset(m.location), m.modification)
                    for m in self.transl_except
                ]
                for pos in positions:
                    for p in pos[0]:
                        if ((p[1] - p[0]) + 1) != 3:
                            raise ValueError("Invalid modification length.")
                        mods.append((p[0], pos[1]))
        except NotImplementedError:
            mods = []
        return bioseq.translate(dna,
            table=self.transl_table,
            start=self.codon_start,
            modifications=mods,
            partial=self.location.fuzzy()
        )

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

        feat = Feature({
            "type": match.group("type").lower(),
            "location": location.parse(stream, match.group("location"))
        })

        for q in parse_qualifiers(stream):
            if q["name"] in ["type", "location"]:
                stream.throw("Invalid qualifier name: '%s'" % q["name"])
            curr = feat.get(q["name"], None)
            if curr is None:
                feat[q["name"]] = q["value"]
            elif isinstance(curr, list):
                feat[q["name"]].append(q["value"])
            else:
                feat[q["name"]] = [curr, q["value"]]
        for qual in feat:
            if qual not in __qual_modifiers__:
                continue
            feat[qual] = __qual_modifiers__[qual](feat, feat[qual])
        ret.append(feat)
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

def mod_codon_start(feat, value):
    return int(value)-1

def mod_transl_table(feat, value):
    return int(value)

def mod_transl_except(feat, value):
    ret = []
    mods = value
    if not isinstance(mods, list):
        mods = [mods]
    for value in mods:
        if value[:1] != "(" or value[-1:] != ")":
            raise ValueError("Invalidly formatted transl_except: %s" % value)
        parts = location.location_split(value[1:-1])
        if len(parts) != 2:
            raise ValueError("Failed to split transl_except: %s" % value)
        if parts[0][:4] != "pos:":
            raise ValueError("Invalid transl_except position: %s" % parts[0])
        if parts[1][:3] != "aa:":
            raise ValueError("Unknown transl_except modification: %s" % parts[1])
        loc = location.parse_str(parts[0][4:])
        acid = parts[1][3:].upper()
        if acid not in bioseq.data.AMINO_ACID_TLC:
            raise ValueError("Unknown Amino Acid code: %s" % acid)
        ret.append(gbobj.GBObj({
            "location": loc,
            "modification": bioseq.data.AMINO_ACID_TLC[acid]
        }))
    return ret

def mod_translation(feat, value):
    return ''.join(value.split()).upper()

__qual_modifiers__ = dict(
    [(k[4:], v) for k, v in globals().copy().iteritems() if k[:4] == "mod_"]
)

FEATURES    = re.compile(r"^FEATURES\s+Location/Qualifiers$")
KEY         = re.compile(r"^\s{5}(?P<type>\S+)\s+(?P<location>\S.*)$")
QUALIFIER   = re.compile(r"^\s{21}/(?P<name>[^\s=]+)(=(?P<value>.+))?$")
QUAL_CONT   = re.compile(r"^\s{21}(?P<value>.*)$")
