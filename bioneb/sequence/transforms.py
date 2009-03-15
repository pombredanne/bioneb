# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import string

__all__ = ["revcomp", "translate"]

COMPLEMENTS = [
    "ACGTUNSWMKRYVDHBacgtunswmkryvdhb",
    "TGCAANSWKMYRBHDVtgcaanswkmyrbhdv"
]
TRANSTABLE = string.maketrans(COMPLEMENTS[0], COMPLEMENTS[1])

def revcomp(seq):
    return seq.translate(TRANSTABLE)[::-1]

CODON_TABLES = {}
def translate(seq, table=1, replace_start=True):
    if table not in CODON_TABLES:
        raise ValueError("Unknown translation table: %s" % table)
    if len(seq) < 3:
        raise ValueError("Sequnce length is too short.")
    t = CODON_TABLES[table]
    (acid, is_start) = t.translate(seq[:3], len(seq) == 3)
    if replace_start and is_start:
        ret = ["M"]
    elif replace_start:
        ret = ["X"]
    else:
        ret = [acid]
    seqlen = len(seq)
    for i in xrange(3, seqlen-(seqlen%3), 3):
        ret.append(t.translate(seq[i:i+3], i == len(seq) - 3)[0])
    return ''.join(ret)

DEGENERATES = {
    "A": "A",   "C": "C",   "G": "G",   "T": "T",   "U": "U",
    "W": "AT",  "S": "CG",  "M": "AC",  "K": "GT",  "R": "AG",  "Y": "CT",
    "B": "AGT", "D": "ACT", "H": "ACT", "V": "ACG", "N": "ACGT"
}
class TranslationTable(object):
    def __init__(self, codons, starts):
        self.codons = codons
        self.starts = starts
    def translate(self, codon, is_stop):
        assert len(codon) == 3, "Invalid codon: %s" % codon
        degen = map(lambda b: DEGENERATES.get(b, b), codon)
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

CODON_TABLE_DATA = [
    """1
    FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    ---M---------------M---------------M----------------------------""",
    """2
    FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIMMTTTTNNKKSS**VVVVAAAADDEEGGGG
    --------------------------------MMMM---------------M------------""",
    """3
    FFLLSSSSYY**CCWWTTTTPPPPHHQQRRRRIIMMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    ----------------------------------MM----------------------------""",
    """4
    FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    --MM---------------M------------MMMM---------------M------------""",
    """5
    FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIMMTTTTNNKKSSSSVVVVAAAADDEEGGGG
    ---M----------------------------MMMM---------------M------------""",
    """6
    FFLLSSSSYYQQCC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    -----------------------------------M----------------------------""",
    """9
    FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIIMTTTTNNNKSSSSVVVVAAAADDEEGGGG
    -----------------------------------M---------------M------------""",
    """10
    FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    ---M---------------M------------MMMM---------------M------------""",
    """11
    FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    ---M---------------M------------MMMM---------------M------------""",
    """12
    FFLLSSSSYY**CC*WLLLSPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    -------------------M---------------M----------------------------""",
    """13
    FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIMMTTTTNNKKSSGGVVVVAAAADDEEGGGG
    ---M------------------------------MM---------------M------------""",
    """14
    FFLLSSSSYYY*CCWWLLLLPPPPHHQQRRRRIIIMTTTTNNNKSSSSVVVVAAAADDEEGGGG
    -----------------------------------M----------------------------""",
    """15
    FFLLSSSSYY*QCC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    -----------------------------------M----------------------------""",
    """16
    FFLLSSSSYY*LCC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    -----------------------------------M----------------------------""",
    """21
    FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIMMTTTTNNNKSSSSVVVVAAAADDEEGGGG
    -----------------------------------M---------------M------------""",
    """22
    FFLLSS*SYY*LCC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    -----------------------------------M----------------------------""",
    """23
    FF*LSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
    --------------------------------M--M---------------M------------"""
]
CODON_TABLE_DATA = [t.split() for t in CODON_TABLE_DATA]
CODONS = ["%s%s%s" % (b1, b2, b3)
    for b1 in "TCAG" for b2 in "TCAG" for b3 in "TCAG"]
for tbl in CODON_TABLE_DATA:
    tid = int(tbl[0])
    trans = dict(zip(CODONS, tbl[1]))
    starts = dict(zip(CODONS, map(lambda x: x == "M", tbl[2])))
    CODON_TABLES[tid] = TranslationTable(trans, starts)
