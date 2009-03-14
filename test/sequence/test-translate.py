# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

def test_single():
    t.eq(t.trans.translate("TGG"), "W")
    t.eq(t.trans.translate("CTG", table=11, replace_start=False), "L")

def test_alternate():
    t.eq(t.trans.translate("TGA"), "*")
    t.eq(t.trans.translate("TGA", table=2), "W")

def test_length_check():
    t.raises(ValueError, t.trans.translate, "AC")

def test_table_check():
    t.raises(ValueError, t.trans.translate, "TTGTTG", -1)

def test_start_codon_replace():
    t.eq(t.trans.translate("TTGTTG"), "ML")
