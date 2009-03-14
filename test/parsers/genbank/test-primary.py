# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

def mk_row(d):
    return {
        "refseq_span": {"from": d[0], "to": d[1]},
        "ident": d[2],
        "primary_span": {"from": d[3], "to": d[4]},
        "complement": d[5]
    }

def do_compare(gb, rows):
    t.eq(len(gb), len(rows))
    for idx, row in enumerate(rows):
        t.eq(gb[idx], mk_row(row))

@t.rec("primary-1.gb")
def test_primary_1(rec):
    rows = [
        [   0,   26, "DA002961.1",    0,   26, False],
        [  27,  975, "BC003555.1",    0,  948, False],
        [ 976,  983, "AW749585.1",   24,   31, False],
        [ 984, 1900, "BC003555.1",  957, 1873, False],
        [1901, 2300, "AK225239.1", 1856, 2255, False],
        [2301, 2694, "BC003555.1", 2274, 2667, False],
        [2695, 2788, "BX645732.1",  173,  266, False],
        [2789, 2816, "AK225239.1", 2738, 2765, False]
    ]
    do_compare(rec.info.primary, rows)

@t.rec("primary-2.gb")
def test_primary_2(rec):
    rows = [
        [   0,   56, "AC156026.3",  220161, 220217, False],
        [  57,  539, "AF548565.1",       0,    482, False],
        [ 540, 1136, "AK135814.1",     732,   1328, False],
        [1137, 3368, "AF548565.1",    1080,   3311, False],
        [3369, 5426, "AC115005.11",  42240,  44297, False]
    ]
    do_compare(rec.info.primary, rows)

@t.rec("primary-3.gb")
def test_primary_with_complement(rec):
    rows = [
        [   0,  634, "CF172065.1",     0,   634, False],
        [ 635, 2165, "AC138613.6", 85777, 87307, True],
        [2166, 2423, "AI839133.1",     0,   257, True]
    ]
    do_compare(rec.info.primary, rows)
