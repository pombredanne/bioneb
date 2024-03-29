# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

def test_single():
    t.eq(t.trans.translate("TGG", partial=True), "W")
    t.eq(t.trans.translate("CTG", table=11, partial=True), "L")

def test_alternate():
    t.eq(t.trans.translate("TGA", partial=True), "*")
    t.eq(t.trans.translate("TGA", table=2, partial=True), "W")

def test_length_check():
    t.raises(ValueError, t.trans.translate, "AC")

def test_table_check():
    t.raises(ValueError, t.trans.translate, "TTGTTG", -1)

def test_start_codon_replace():
    t.eq(t.trans.translate("TTGTTG"), "ML")

def test_simple_degenerate():
    t.eq(t.trans.translate("ACN", partial=True), "T")

def test_degenerate_causes_not_start():
    t.eq(t.trans.translate("GTG", table=2), "M")
    t.eq(t.trans.translate("GTG", table=2, partial=True), "V")
    t.eq(t.trans.translate("GTR", table=2), "X")
    t.eq(t.trans.translate("GTR", table=2, partial=True), "V")

def test_degnerate_to_X():
    t.eq(t.trans.translate("CAY", partial=True), "H")
    t.eq(t.trans.translate("CAR", partial=True), "Q")
    t.eq(t.trans.translate("CAN", partial=True), "X")

def test_degenerate_error():
    t.eq(t.trans.translate("ATG", table=11, partial=True), "M")
    t.eq(t.trans.translate("ATC", table=11, partial=True), "I")
    t.eq(t.trans.translate("ATS", table=11, partial=True), "X")

def test_degenerate_in_seq():
    seq = "CTGATCGTCATSTGTATCACC"
    t.eq(t.trans.translate(seq, table=11, partial=True), "LIVXCIT")

def test_degenerate_regresion():
    t.eq(t.trans.translate("GCGCCCAAKACGCAA", table=11, partial=True), "APXTQ")

