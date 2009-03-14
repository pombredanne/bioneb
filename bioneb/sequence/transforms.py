# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import string

__all__ = ["revcomp", "translate"]

COMPLEMENTS = [
    "ACGTUNRYMSWKVDHBacgtunrymswkvdhb",
    "TGCAANYRKWSMTCGAtgcaanyrkwsmtcga"
]
TRANSTABLE = string.maketrans(COMPLEMENTS[0], COMPLEMENTS[1])

def revcomp(seq):
    return seq.translate(TRANSTABLE)[::-1]

CODON_TABLES = {}
def translate(seq, table=1, replace_start=True):
    if table not in CODON_TABLES:
        raise ValueError("Unknown translation table: %s" % table)
    if len(seq) % 3 != 0:
        raise ValueError("Sequnce length is not a multiple of 3.")
    trans, starts = CODON_TABLES[table]
    if replace_start and starts[seq[:3]]:
        ret = ["M"]
    else:
        ret = [trans.get(seq[:3], "X")]
    for i in xrange(3, len(seq), 3):
        ret.append(trans.get(seq[i:i+3], "X"))
    return ''.join(ret)

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
    CODON_TABLES[tid] = (trans, starts)
