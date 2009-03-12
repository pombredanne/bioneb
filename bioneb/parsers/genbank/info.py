# Copyright 2008 New England Biolabs <davisp@neb.com>

import re

import gbobj
import location
import stream

KWNAMES = {"reference": "references", "dbsource": "db_source"}

def parse(stream):
    ret = gbobj.GBObj()
    keywords = parse_keywords(stream)
    for kw in keywords:
        func = __kw_parsers__.get("kw_%s" % kw.lower())
        if not func:
            stream.throw("Unknown keyword: '%s'" % kw)
        name = KWNAMES.get(kw.lower(), kw.lower())
        ret[name] = func(stream, keywords[kw])
    return ret

def parse_keywords(stream):
    ret = {}
    for line in stream:
        match = KEYWORD.match(line)
        if not match or match.group("name") in ["FEATURES", "ORIGIN"]:
            stream.undo(line)
            return ret
        key = match.group("name")
        value = [match.group("value")] + parse_continuation(stream)
        if key in ret and not isinstance(ret[key], list):
            ret[key] = [ret[key]]
        if key in ret:
            ret[key].append({
                "value": '\n'.join(value),
                "subkeys": parse_subkeywords(stream)
            })
        else:
            ret[key] = {
                "value": '\n'.join(value),
                "subkeys": parse_subkeywords(stream)
            }

def parse_subkeywords(stream):
    ret = []
    for line in stream:
        match = SUBKW.match(line)
        if not match:
            stream.undo(line)
            return ret
        key = match.group("name")
        value = [match.group("value")] + parse_continuation(stream)
        ret.append({"name": key, "value": '\n'.join(value)})

def parse_continuation(stream):
    ret = []
    for line in stream:
        match = CONTINUE.match(line)
        if not match:
            stream.undo(line)
            return ret
        ret.append(match.group("value"))
    
def kw_definition(stream, kw):
    _no_subkeys(stream, "DEFINITION", kw)
    return kw["value"].strip().rstrip('.')

def kw_accession(stream, kw):
    _no_subkeys(stream, "ACCESSION", kw)
    return kw["value"].strip()

def kw_pid(stream, kw):
    _no_subkeys(stream, "PID", kw)
    return kw["value"].strip()

def kw_version(stream, kw):
    _no_subkeys(stream, "VERSION", kw)
    ret = gbobj.GBObj()
    ret["accessions"] = []
    for token in kw["value"].split():
        match = GI.match(token)
        if match:
            ret["gi"] = match.group("value")
        else:
            ret["accessions"].append(token)
    return ret

def kw_dbsource(self, kw):
    _no_subkeys(stream, "DBSOURCE", kw)
    return kw["value"].strip()

def kw_project(stream, kw):
    _no_subkeys(stream, "PROJECT", kw)
    return kw["value"].strip()

def kw_keywords(stream, kw):
    _no_subkeys(stream, "KEYWORDS", kw)
    return filter(None, [
        t.strip().replace("\n", " ")
        for t in kw["value"].strip().rstrip('.').split(';')
    ])

def kw_segment(stream, kw):
    _no_subkeys(stream, "SEGMENT", kw)
    match = POSITION.match(kw["value"].strip())
    if not match:
        stream.throw("Invalid SEGMENT format: '%s'" % kw["value"].strip())
    return gbobj.GBObj({
        "id": int(match.group("value"))-1,
        "total": int(match.group("total"))
    })

def kw_source(stream, kw):
    if len(kw["subkeys"]) == 0:
        stream.throw("Invalid SOURCE definition has no ORGANISM specified.")
    if kw["subkeys"][0]["name"] != "ORGANISM":
        stream.throw("Invalid SOURCE definition has no ORGANISM specified.")
    lines = kw["subkeys"][0]["value"].split("\n")
    return gbobj.GBObj({
        "name": kw["value"].strip().rstrip('.'),
        "organism": lines[0].strip(),
        "lineage": [
            t.strip()
            for t in ' '.join(lines[1:]).rstrip('.').split(';')
        ]
    })

def kw_reference(stream, kw):
    ret = []
    if not isinstance(kw, list):
        kw = [kw]
    for obj in kw:
        ref = gbobj.GBObj()
        match = REF_LOC.match(obj["value"])
        if match is not None:
            ref["start"] = int(match.group("start"))-1
            ref["end"] = int(match.group("end"))-1
        for sub in obj["subkeys"]:
            # If authors follows the Last,F.M., pattern, create an array of
            # authors. Otherwise, just keep the authors definition as a string.
            if sub["name"].lower() == "authors":
                valid = True
                authors = []
                tokens = sub["value"].split()
                for idx, auth in enumerate(tokens):
                    if idx == len(tokens) - 2 and auth.lower() == "and":
                        continue
                    if not AUTHOR.match(auth):
                        valid = False
                        break
                    authors.append(auth.rstrip(','))
                if valid:
                    ref["authors"] = authors
                else:
                    ref["authors"] = ' '.join(sub["value"].split())
            else:
                ref[sub["name"].lower()] = ' '.join(sub["value"].split())
        ret.append(ref)
    return ret

def kw_comment(stream, kw):
    _no_subkeys(stream, "COMMENT", kw)
    return ' '.join(kw["value"].split())

def kw_primary(stream, kw):
    lines = kw["value"].split("\n")
    match = HEADER.match(lines[0])
    if not match:
        stream.throw("Invalid PRIMARY header: '%s'" % lines[0].strip())
    rows = []
    for line in lines[1:]:
        match = ROW.match(line.strip())
        if not match:
            stream.throw("Invalid PRIMARY row: '%s'" % line.strip())
        rows.append({
            "refseq_span": {
                "from": int(match.group("rsfrom"))-1,
                "to": int(match.group("rsto"))-1
            },
            "ident": match.group("ident"),
            "primary_span": {
                "from": int(match.group("prfrom"))-1,
                "to": int(match.group("prto"))-1
            },
            "complement": (
                match.groupdict().has_key("comp")
                and match.group("comp") is not None
            )
        })
    return rows

def kw_contig(stream, kw):
    _no_subkeys(stream, "CONTIG", kw)
    return location.parse_str(''.join(kw["value"].split()))

def _counts(stream, kw):
    "Special casing for Python requirements of no spaces in names."
    _no_subkeys(stream, "BASE COUNTS", kw)
    match = BASE_COUNTS.match(kw["value"])
    if not match:
        stream.throw("Invalid base counts: %s" % kw["value"])
    return dict([(k, int(v or 0)) for k, v in match.groupdict().iteritems()])

def _no_subkeys(stream, kw, value):
    if len(value["subkeys"]):
        stream.throw("%s must not have sub-keywords." % kw)

__kw_parsers__ = dict(
    [(k, v) for (k, v) in globals().copy().iteritems() if k.startswith("kw_")]
)
__kw_parsers__["kw_base count"] = _counts

# Main
KEYWORD     = re.compile(r"^(?P<name>((BASE COUNT)|([A-Z]+)))\s+(?P<value>.*)$")
SUBKW       = re.compile(r"^\s{2,3}(?P<name>[A-Z]+)\s+(?P<value>.*)$")
CONTINUE    = re.compile(r"^\s{12}(?P<value>.*)$")

# Version
GI          = re.compile(r"^GI:(?P<value>\d+)$")

# Segment
POSITION    = re.compile(r"^(?P<value>\d+)\sof\s(?P<total>\d+)$")

# Reference
AUTHOR      = re.compile(r"^[^\s,]+,[^\s,]+,?$")
REF_LOC     = re.compile(r"""
                (?P<id>\d+)
                \s+
                \(
                    (bases|residues)
                    \s+
                    (?P<start>\d+)
                    \s+to\s+
                    (?P<end>\d+)
                \)
                $
            """, re.VERBOSE)

# Primary
HEADER      = re.compile(
                r"^REFSEQ_SPAN\s+PRIMARY_IDENTIFIER\s+PRIMARY_SPAN\s+COMP$"
            )
ROW         = re.compile(r"""
                ^
                (?P<rsfrom>\d+)-(?P<rsto>\d+) # RefSeq span
                \s+
                (?P<ident>[^\s]+) # Identifier
                \s+
                (?P<prfrom>\d+)-(?P<prto>\d+) # Primary Span
                (\s+(?P<comp>[^\s]+))? # Optional complement info
                $
            """, re.VERBOSE)

BASE_COUNTS = re.compile(r"""
                ^
                (?P<A>\d+)\s[aA]\s*
                (?P<C>\d+)\s[cC]\s*
                (?P<G>\d+)\s[gG]\s*
                (?P<T>\d+)\s[tT]
                (\s*(?P<others>\d+)\s[oO][tT][hH][eE][rR][sS])?
                $
            """, re.VERBOSE)