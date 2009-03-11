
import re

from errors import *
from patterns import *

class GBLocationParser(object):

    def parse(self, loc):
        return self._parse(loc, None)

    def _continuation(self):
        for line in self._source:
            match = LOC_CONT.match(line)
            if not match:
                self._source.undo()
                raise StopIteration
            yield match.group("value")

    def _parse(self, loc, curr):
        if curr is None:
            curr = {"strand": "forward"}
        loc = loc.strip()
        for re in LOC_FUNCS:
            match = re[1].match(loc)
            if match is not None:
                fn = getattr(self, '_%s' % re[0])
                return fn(loc, match, curr=curr)
        raise LocationError(
            filename=self._source.filename,
            lineno=self._source.lineno,
            mesg="Unable to parse location: '%s'" % loc
        )
    
    def _complement(self, loc, match, curr):
        args = self._split(match.group("args"))
        self._assert(len(args) == 1,
            "Invalid `complement` argument list: '%s'" % match.group("args"))
        curr["strand"] = "reverse"
        self._parse(args[0], curr)
        return curr

    def _join(self, loc, match, curr):
        args = self._split(match.group("args"))
        self._assert(len(args) > 1,
            "Invalid `join` argument list: '%s'" % match.group("args"))
        curr["type"] = "join"
        curr["args"] = map(self._parse, args)
        return curr

    def _order(self, loc, match, curr):
        args = self._split(match.group("args"))
        self._assert(len(args) > 1,
            "Invalid `order` argument list: '%s'" % match.group("args"))
        curr["type"] = "order"
        curr["args"] = map(self._parse, args)
        return curr

    def _bond(self, loc, match, curr):
        args = self._split(match.group("args"))
        self._assert(len(args) == 2,
            "Invalid `bond` argument list: '%s'" % match.group("args"))
        curr["type"] = "bond"
        curr["args"] = map(lambda a: int(a)-1, args)
        return curr
    
    def _gap(self, loc, match, curr):
        args = self._split(match.group("args"))
        self._assert(len(args) == 1,
                "Invalid `gap` argument list: '%s'" % match.group("args"))
        curr["type"] = "gap"
        curr["args"] = int(args[0])
        return curr
        
    def _ref(self, loc, match, curr):
        next = {"strand": curr.pop("strand")}
        curr["type"] = "reference"
        key = self._parse(match.group("acc"), None)
        val = self._parse(match.group("args"), next)
        curr["args"] = {key: val}
        return curr
    
    def _site(self, loc, match, curr):
        curr["type"] = "site"
        curr["args"] = [
            self._parse(match.group("start"), {}),
            self._parse(match.group("end"), {})
        ]
        return curr
    
    def _choice(self, loc, match, curr):
        curr["type"] = "choice"
        curr["args"] = [int(match.group("start"))-1, int(match.group("end"))-1]
        return curr
    
    def _span(self, loc, match, curr):
        curr["type"] = "span"
        curr["start"] = self._parse(match.group("start"), {})
        curr["end"] = self._parse(match.group("end"), {})
        return curr

    def _one_of(self, loc, match, curr):
        args = self._split(match.group("args"))
        self._assert(len(args) > 1,
                "Invalid `one-of` argument list: '%s'" % match.group("args"))
        curr["type"] = "one-of" 
        curr["args"] = map(lambda a: self._parse(a, {}), args)
        return curr
    
    def _accession(self, loc, match, curr):
        return loc

    def _single(self, loc, match, curr):
        curr["type"] = "single"
        if loc[:1] == "<":
            curr["fuzzy"] = "before"
            curr["coord"] = int(loc[1:])-1
        elif loc[:1] == ">":
            curr["fuzzy"] = "after"
            curr["coord"] = int(loc[1:])-1
        else:
            curr["fuzzy"] = False
            curr["coord"] = int(loc)-1
        return curr

    def _split(self, args):
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
            raise LocationError(
                filename=self._source.filename,
                lineno=self._source.lineno,
                mesg="Unbalanced parenthesis: '%s'" % args
            )
        ret.append(args[last:])
        return ret

