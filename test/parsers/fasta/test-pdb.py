# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.seq("pdb.fa", num=0)
def test_pdb_a(rec):
    t.eq(rec.ident, {"gi": "640096", "pdb": ["172D", "A"]})
    t.eq(rec.desc.startswith("Chain A"), True)
    t.eq(rec.seq, "GAAGCTTC")

@t.seq("pdb.fa", num=2)
def test_pdb_b(rec):
    t.eq(rec.ident, {"gi": "640098", "pdb": ["172D", "C"]})
    t.eq(rec.desc.startswith("Chain C"), True)
    t.eq(rec.seq, "GAAGCTTC")
