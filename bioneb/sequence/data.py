# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import string

DEGENERATES = {
    "A": "A",   "C": "C",   "G": "G",   "T": "T",   "U": "U",
    "W": "AT",  "S": "CG",  "M": "AC",  "K": "GT",  "R": "AG",  "Y": "CT",
    "B": "AGT", "D": "ACT", "H": "ACT", "V": "ACG", "N": "ACGT"
}

COMPLEMENTS = [
    "ACGTUNSWMKRYVDHBacgtunswmkryvdhb",
    "TGCAANSWKMYRBHDVtgcaanswkmyrbhdv"
]
TRANSTABLE = string.maketrans(COMPLEMENTS[0], COMPLEMENTS[1])

# Three letter codes
AMINO_ACID_TLC = {
    "ALA": "A",
    "ASX": "B",
    "CYS": "C",
    "ASP": "D",
    "GLU": "E",
    "PHE": "F",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LYS": "K",
    "LEU": "L",
    "MET": "M",
    "ASN": "N",
    "PYL": "O",
    "PRO": "P",
    "GLN": "Q",
    "ARG": "R",
    "SER": "S",
    "THR": "T",
    "SEC": "U",
    "VAL": "V",
    "TRP": "W",
    "XAA": "X",
    "TYR": "Y",
    "GLX": "Z",
    # Due to Genbank awesomeness
    "OTHER": "X", 
    "TERM": "*"
}

CODONS = ["%s%s%s" % (b1, b2, b3)
    for b1 in "TCAG" for b2 in "TCAG" for b3 in "TCAG"]

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