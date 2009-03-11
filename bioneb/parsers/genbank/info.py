# Copyright 2008 New England Biolabs <davisp@neb.com>

from errors import *
from patterns import *

class GBInfo(object):
    def __init__(self):

class GBInfoParser(object):
    def __init__(self, stream):
        self.patterns = {
            "length": LENGTH,
            "type": TYPE,
            "molecule_type": MOL_TYPE,
            "strand_type": STRAND_TYPE,
            "division": DIVISION
        }

    def keys(self):
        """\
        Parse all keyword (LOCUS, REFERENCE, SOURCE...)
        sections in the record information.
        """
        for line in self._source:
            if not line.strip():
                continue
            match = KEYWORD.match(line)
            if not match or match.group("name") == "FEATURES":
                self._source.undo()
                raise StopIteration
            ret = {
                "name": match.group("name"),
                "value": ["%s\n" % match.group("value")],
                "subkeys": []
            }
            ret["value"].extend(self._continuation())
            ret["value"] = ''.join(ret["value"]).strip()
            ret["subkeys"].extend(self._subkeys())
            yield ret
    
    def subkeys(self):
        for line in self._source:
            match = SUBKW.match(line)
            if not match:
                self._source.undo()
                raise StopIteration
            ret = {
                "name": match.group("name"),
                "value": ["%s\n" % match.group("value")]
            }
            ret["value"].extend(self._continuation())
            ret["value"] = ''.join(ret["value"]).strip()
            yield ret
    
    def continuation(self):
        for line in self._source:
            match = CONTINUE.match(line)
            if not match:
                self._source.undo()
                raise StopIteration
            yield "%s\n" % match.group("value")
    
    def definition(self, kw, info):
        self._assert_no_subkeys(kw, "DEFINITION")
        info["definition"] = kw["value"].strip().rstrip('.')
    
    def accession(self, kw, info):
        self._assert_no_subkeys(kw, "ACCESSION")
        info["accession"] = kw["value"].strip()
    
    def pid(self, kw, info):
        self._assert_no_subkeys(kw, "PID")
        info["pid"] = kw["value"].strip()
    
    def version(self, kw, info):
        self._assert_no_subkeys(kw, "VERSION")
        info["versions"] = []
        for token in kw["value"].split():
            match = __regexp__["version"]["gi"].match(token)
            if match:
                info["gi"] = match.group("value")
            else:
                info["versions"].append(token)

    def dbsource(self, kw, info):
        self._assert_no_subkeys(kw, "DBSOURCE")
        info["db_source"] = kw["value"].strip()

    def project(self, kw, info):
        self._assert_no_subkeys(kw, "PROJECT")
        info["PROJECT"] = kw["value"].strip()
    
    def keywords(self, kw, info):
        self._assert_no_subkeys(kw, "KEYWORDS")
        kws = [
            t.strip().replace("\n", " ")
            for t in kw["value"].strip().rstrip('.').split(';')
        ]
        info["keywords"] = filter(None, kws)

    def segment(self, kw, info):
        self._assert_no_subkeys(kw, "SEGMENT")
        match = __regexp__["segment"]["position"].match(kw["value"].strip())
        self._assert(match,
                "Invalid SEGMENT format: '%s'" % kw["value"].strip())
        info["segment"] = {
            "id": int(match.group("value"))-1,
            "total": int(match.group("total"))
        }

    def source(self, kw, info):
        self._assert(len(kw["subkeys"]) == 1,
                "Invalid SOURCE definition has no ORGANISM specified.")
        self._assert(kw["subkeys"][0]["name"] == "ORGANISM",
                "Invalid SOURCE definition has no ORGANISM specified.")
        lines = kw["subkeys"][0]["value"].split("\n")
        info["source"] = {
            "name": kw["value"].strip().rstrip('.'),
            "organism": lines[0].strip(),
            "lineage": [
                t.strip()
                for t in ' '.join(lines[1:]).rstrip('.').split(';')
            ]
        }        

    def reference(self, kw, info):
        ref = {}
        match = __regexp__["reference"]["location"].match(kw["value"])
        if match is not None:
            ref["start"] = int(match.group("start"))-1
            ref["end"] = int(match.group("end"))-1
        for sub in kw["subkeys"]:
            # If authors follows the Last,F.M., pattern, create an array of
            # authors. Otherwise, just keep the authors definition as a string.
            if sub["name"] == "AUTHORS":
                valid = True
                authors = []
                tokens = sub["value"].split()
                for idx, auth in enumerate(tokens):
                    if idx == len(tokens) - 2 and auth.lower() == "and":
                        continue
                    if not __regexp__["reference"]["author"].match(auth):
                        valid = False
                        break
                    authors.append(auth.rstrip(','))
                if valid:
                    ref["authors"] = authors
                else:
                    ref["authors"] = ' '.join(sub["value"].split())
            else:
                ref[sub["name"].lower()] = ' '.join(sub["value"].split())
        info.setdefault("references", [])
        info["references"].append(ref)

    def comment(self, kw, info):
        self._assert_no_subkeys(kw, "COMMENT")
        info["comment"] = ' '.join(kw["value"].split())

    def primary(self, kw, info):
        lines = kw["value"].split("\n")
        match = __regexp__["primary"]["header"].match(lines[0])
        self._assert(match, "Invalid PRIMARY header: '%s'" % lines[0].strip())
        rows = []
        for line in lines[1:]:
            match = __regexp__["primary"]["row"].match(line.strip())
            self._assert(match, "Invalid PRIMARY row: '%s'" % line.strip())
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
        info["primary"] = rows
