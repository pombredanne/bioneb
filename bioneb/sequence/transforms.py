# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import data

__all__ = ["revcomp", "translate"]

def revcomp(seq):
    return seq.translate(data.TRANSTABLE)[::-1]

CODON_TABLES = {}
def translate(seq, table=1, start=0, modifications=None, partial=False):
    if start > 0:
        seq = seq[start:]
    if modifications is None:
        modifications = []
    if isinstance(partial, bool):
        partial = (partial, partial)
    if table not in CODON_TABLES:
        raise ValueError("Unknown translation table: %s" % table)
    if len(seq) < 3:
        raise ValueError("Sequnce length is too short.")
    t = CODON_TABLES[table]
    (acid, is_start) = t.translate(seq[:3], len(seq) == 3)
    if not partial[0] and is_start:
        ret = ["M"]
    elif not partial[0] and start < 1:
        ret = ["X"]
    else:
        ret = [acid]
    seqlen = len(seq)
    for i in xrange(3, seqlen-(seqlen%3), 3):
        ret.append(t.translate(seq[i:i+3], i == len(seq) - 3)[0])
    ret = ''.join(ret)
    if not partial[1] and ret[-1:] == "*":
        ret = ret[:-1]
    for m in modifications:
        if m[0] % 3 != 0:
            raise ValueError("Invalid modification coordinate: %s" % m[0])
        idx = m[0]/3
        ret = "%s%s%s" % (ret[:idx], m[1], ret[idx+1:])
    return ret

class TranslationTable(object):
    def __init__(self, codons, starts):
        self.codons = codons
        self.starts = starts
    def translate(self, codon, is_stop):
        assert len(codon) == 3, "Invalid codon: %s" % codon
        degen = map(lambda b: data.DEGENERATES.get(b, b), codon)
        degencodons = [
            "%s%s%s" % (b1, b2, b3)
            for b1 in degen[0]
            for b2 in degen[1]
            for b3 in degen[2]
        ]
        acids = set(map(lambda x: self.codons.get(x, 'X'), degencodons))
        starts = set(map(lambda x: self.starts.get(x, False), degencodons))
        if len(acids) == 1 and acids == set("*") and not is_stop:
            acid = "X"
        elif len(acids) == 1:
            acid = acids.pop()
        elif acids == set("DN"):
            acid = "B"
        elif acids == set("EQ"):
            acid = "Z"
        elif acids == set("IL"):
            acid = "J"
        else:
            acid = "X"
        if len(starts) > 1:
            start = False
        else:
            start = starts.pop()
        return (acid, start)
 
for tbl in [t.split() for t in data.CODON_TABLE_DATA]:
    tid = int(tbl[0])
    trans = dict(zip(data.CODONS, tbl[1]))
    starts = dict(zip(data.CODONS, map(lambda x: x == "M", tbl[2])))
    CODON_TABLES[tid] = TranslationTable(trans, starts)
