# Copyright 2009 New England Biolabs <davisp@neb.com>
import t

@t.rec("bond.gb")
def test_bond(rec):
    expected = [[11, 62], [15, 35], [21, 45], [25, 47]]
    bonds = filter(lambda x: x["type"] == "bond", rec.features)
    for idx, bond in enumerate(bonds):
        t.eq(bond.location.type, "bond")
        t.eq(bond.location.sites, expected[idx])
