
class GenbankError(Exception):
    def __init__(self,filename=None, lineno=None, mesg='Parsing failed.'):
        self._fname = filename
        self._lineno = lineno
        self._mesg = mesg
    
    def __str__(self):
        ret = ["Genbank Error: "]
        if self._fname:
            ret.append(self._fname)
        if self._lineno:
            ret.append('(%s)' % self._lineno)
        if self._fname or self._lineno:
            ret.append(': ')
        ret.append(self._mesg)
        return ''.join(ret)

class LocationError(GenbankError):
    pass

def gb_check(self, cond, msg):
    if not cond:
        gb_raise(msg)
        
def gb_no_subkeys(self, kw, ktype):
        self._assert(len(kw["subkeys"]) == 0,
            "%s lines should not have subkeyword sections." % ktype)
    
def gb_raise(self, msg):
    raise GenbankError(
        filename=self._source.filename,
        lineno=self._source.lineno,
        mesg=msg
    )
