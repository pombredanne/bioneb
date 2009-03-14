# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t
def test_simple():
    t.eq(t.trans.revcomp("ACGT"), "ACGT")
    t.eq(t.trans.revcomp("TGGGGCCAA"), "TTGGCCCCA")
    t.eq(t.trans.revcomp("CCCCA"), "TGGGG")
    t.eq(t.trans.revcomp("MDggC"), "GccCK")

def test_degenerate():
    # This was a fun one to figure out.
    t.eq(t.trans.revcomp("W"), "W")
    t.eq(t.trans.revcomp("S"), "S")
